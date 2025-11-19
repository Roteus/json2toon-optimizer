"""Configuration module and CLI for json2toon-optimizer"""

import sys
import argparse
import glob
from pathlib import Path
from typing import List


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="json2toon-optimizer - Converts JSON to TOON with token optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file
  json2toon data.json
  json2toon data.json --output ./results
  
  # Batch processing
  json2toon examples/*.json --batch
  json2toon examples/ --recursive --batch
  
  # Custom format options
  json2toon data.json --delimiter tab --indent 4
  json2toon data.json --format toon --force
  
  # Streaming large files
  json2toon huge_data.json --stream --chunk-size 10000
  
  # Analysis
  json2toon data.json --stats
        """,
    )

    parser.add_argument(
        "input",
        nargs="+",
        help="Input JSON file(s) or directory. Supports glob patterns (*.json)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory (default: same as input)",
    )

    # Format options
    format_group = parser.add_argument_group("format options")
    
    format_group.add_argument(
        "--delimiter",
        choices=["comma", "tab", "pipe"],
        default="comma",
        help="Delimiter for arrays and tabular data (default: comma)",
    )

    format_group.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Number of spaces for indentation (default: 2)",
    )

    format_group.add_argument(
        "--format",
        choices=["auto", "toon", "json", "compact"],
        default="auto",
        help="Output format: auto (best), toon, json, or compact (default: auto)",
    )

    format_group.add_argument(
        "--force",
        action="store_true",
        help="Force the specified format even if not optimal",
    )

    # Batch processing options
    batch_group = parser.add_argument_group("batch processing")
    
    batch_group.add_argument(
        "--batch",
        action="store_true",
        help="Enable batch processing for multiple files",
    )

    batch_group.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Process directories recursively",
    )

    batch_group.add_argument(
        "--pattern",
        default="*.json",
        help="File pattern for batch processing (default: *.json)",
    )

    batch_group.add_argument(
        "--exclude",
        action="append",
        help="Exclude files matching pattern (can be used multiple times)",
    )

    batch_group.add_argument(
        "--parallel",
        type=int,
        default=1,
        metavar="N",
        help="Number of parallel workers for batch processing (default: 1)",
    )

    # Streaming options
    stream_group = parser.add_argument_group("streaming options")
    
    stream_group.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming mode for very large files",
    )

    stream_group.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Number of items per chunk in streaming mode (default: 1000)",
    )

    # Analysis options
    analysis_group = parser.add_argument_group("analysis options")
    
    analysis_group.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="Show detailed statistics",
    )

    analysis_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress all output except errors",
    )

    analysis_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose output with progress",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0",
    )

    args = parser.parse_args()

    # Import here to avoid circular import
    from .toon_converter import process_json_file
    from .batch_processor import process_batch
    from .stream_processor import process_stream

    try:
        # Determine processing mode
        input_paths = _resolve_input_paths(args.input, args.recursive, args.pattern, args.exclude)
        
        if args.stream:
            # Streaming mode for large files
            if len(input_paths) > 1:
                print("⚠️  Warning: Streaming mode only supports single file. Processing first file only.", file=sys.stderr)
                input_paths = [input_paths[0]]
            
            result = process_stream(
                input_paths[0],
                output_dir=args.output,
                chunk_size=args.chunk_size,
                delimiter=args.delimiter,
                indent=args.indent,
                quiet=args.quiet,
                verbose=args.verbose
            )
            
            if args.stats and not args.quiet:
                _print_stream_stats(result)
        
        elif args.batch or len(input_paths) > 1:
            # Batch processing mode
            results = process_batch(
                input_paths,
                output_dir=args.output,
                delimiter=args.delimiter,
                indent=args.indent,
                format_choice=args.format,
                force_format=args.force,
                parallel_workers=args.parallel,
                quiet=args.quiet,
                verbose=args.verbose
            )
            
            if args.stats and not args.quiet:
                _print_batch_stats(results)
        
        else:
            # Single file processing (original mode)
            result = process_json_file(
                input_paths[0],
                args.output,
                delimiter=args.delimiter,
                indent=args.indent,
                format_choice=args.format,
                force_format=args.force
            )

            if not args.quiet:
                if args.stats:
                    _print_single_stats(result)
                else:
                    print(f"✅ Saved: {result['output_file']}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _resolve_input_paths(inputs: List[str], recursive: bool, pattern: str, exclude: List[str]) -> List[Path]:
    """Resolve input paths with glob patterns and directory traversal"""
    paths = []
    exclude = exclude or []
    
    for input_str in inputs:
        input_path = Path(input_str)
        
        if input_path.is_file():
            paths.append(input_path)
        elif input_path.is_dir():
            if recursive:
                found = list(input_path.rglob(pattern))
            else:
                found = list(input_path.glob(pattern))
            paths.extend(found)
        else:
            # Try glob pattern
            found = glob.glob(input_str, recursive=recursive)
            paths.extend([Path(p) for p in found])
    
    # Filter out excluded patterns
    filtered_paths = []
    for path in paths:
        excluded = False
        for exclude_pattern in exclude:
            if path.match(exclude_pattern):
                excluded = True
                break
        if not excluded and path.suffix == '.json':
            filtered_paths.append(path)
    
    if not filtered_paths:
        raise FileNotFoundError(f"No JSON files found matching the input pattern")
    
    return filtered_paths


def _print_single_stats(result: dict):
    """Print statistics for single file processing"""
    print("\n" + "="*60)
    print("📊 CONVERSION STATISTICS")
    print("="*60)
    print(f"Input file:      {result['input_file']}")
    print(f"Output file:     {result['output_file']}")
    print(f"Chosen format:   {result['chosen_format']}")
    print(f"\nToken Analysis:")
    print(f"  JSON (minified):  {result['json_tokens']:,} tokens")
    print(f"  TOON (standard):  {result['toon_tokens']:,} tokens")
    print(f"  TOON (compact):   {result['toon_compact_tokens']:,} tokens")
    print(f"\n💰 Savings:        {result['savings_tokens']:,} tokens ({result['savings_percentage']:.1f}%)")
    print("="*60)


def _print_batch_stats(results: dict):
    """Print statistics for batch processing"""
    print("\n" + "="*60)
    print("📊 BATCH PROCESSING SUMMARY")
    print("="*60)
    print(f"Total files processed: {results['total_files']}")
    print(f"Successful:            {results['successful']}")
    print(f"Failed:                {results['failed']}")
    print(f"\nFormat Distribution:")
    print(f"  TOON format:         {results['toon_count']} files")
    print(f"  JSON format:         {results['json_count']} files")
    print(f"  Compact format:      {results['compact_count']} files")
    print(f"\n💰 Total Savings:")
    print(f"  Tokens saved:        {results['total_tokens_saved']:,}")
    print(f"  Average savings:     {results['average_savings']:.1f}%")
    print(f"\n⏱️  Processing time:    {results['processing_time']:.2f}s")
    print(f"📁 Output directory:   {results['output_directory']}")
    print("="*60)


def _print_stream_stats(result: dict):
    """Print statistics for streaming processing"""
    print("\n" + "="*60)
    print("📊 STREAMING PROCESSING SUMMARY")
    print("="*60)
    print(f"Input file:           {result['input_file']}")
    print(f"Output file:          {result['output_file']}")
    print(f"Chunks processed:     {result['chunks_processed']}")
    print(f"Items processed:      {result['items_processed']:,}")
    print(f"\n💰 Estimated Savings:")
    print(f"  Tokens saved:       ~{result['estimated_tokens_saved']:,}")
    print(f"  Average savings:    ~{result['estimated_savings_percent']:.1f}%")
    print(f"\n⏱️  Processing time:   {result['processing_time']:.2f}s")
    print(f"💾 Peak memory:        {result['peak_memory_mb']:.1f} MB")
    print("="*60)


if __name__ == "__main__":
    main()
