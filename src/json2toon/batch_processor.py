"""Batch processing for multiple JSON files"""

import time
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed


def process_batch(
    input_paths: List[Path],
    output_dir: Optional[str] = None,
    delimiter: str = "comma",
    indent: int = 2,
    format_choice: str = "auto",
    force_format: bool = False,
    parallel_workers: int = 1,
    quiet: bool = False,
    verbose: bool = False
) -> Dict:
    """
    Process multiple JSON files in batch mode
    
    Args:
        input_paths: List of input file paths
        output_dir: Output directory for converted files
        delimiter: Delimiter for arrays (comma/tab/pipe)
        indent: Indentation spaces
        format_choice: Output format (auto/toon/json/compact)
        force_format: Force specified format even if not optimal
        parallel_workers: Number of parallel workers
        quiet: Suppress output
        verbose: Show detailed progress
        
    Returns:
        Dictionary with batch processing statistics
    """
    from .toon_converter import process_json_file
    
    start_time = time.time()
    
    results = {
        'total_files': len(input_paths),
        'successful': 0,
        'failed': 0,
        'toon_count': 0,
        'json_count': 0,
        'compact_count': 0,
        'total_tokens_saved': 0,
        'total_json_tokens': 0,
        'total_output_tokens': 0,
        'files': [],
        'errors': []
    }
    
    if not quiet:
        print(f"\n🔄 Processing {len(input_paths)} files...")
        if verbose:
            print(f"   Workers: {parallel_workers}")
            print(f"   Output: {output_dir or 'same as input'}")
    
    # Convert delimiter name to character
    delimiter_map = {
        'comma': ',',
        'tab': '\t',
        'pipe': '|'
    }
    delimiter_char = delimiter_map.get(delimiter, ',')
    
    if parallel_workers > 1:
        # Parallel processing
        try:
            with ProcessPoolExecutor(max_workers=parallel_workers) as executor:
                futures = {
                    executor.submit(
                        _process_single_file,
                        path,
                        output_dir,
                        delimiter_char,
                        indent,
                        format_choice,
                        force_format
                    ): path for path in input_paths
                }
                
                for i, future in enumerate(as_completed(futures), 1):
                    path = futures[future]
                    try:
                        result = future.result()
                        _update_results(results, result, path)
                        
                        if verbose and not quiet:
                            print(f"   [{i}/{len(input_paths)}] ✅ {path.name}")
                            
                    except Exception as e:
                        results['failed'] += 1
                        results['errors'].append({'file': str(path), 'error': str(e)})
                        
                        if verbose and not quiet:
                            print(f"   [{i}/{len(input_paths)}] ❌ {path.name}: {e}")
        except Exception as pool_error:
            # Fallback to sequential if parallel fails
            if not quiet:
                print(f"   ⚠️  Parallel processing failed, falling back to sequential: {pool_error}")
            # Execute sequential processing as fallback
            for i, path in enumerate(input_paths, 1):
                try:
                    result = _process_single_file(
                        path,
                        output_dir,
                        delimiter_char,
                        indent,
                        format_choice,
                        force_format
                    )
                    _update_results(results, result, path)
                    
                    if verbose and not quiet:
                        print(f"   [{i}/{len(input_paths)}] ✅ {path.name}")
                        
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append({'file': str(path), 'error': str(e)})
                    
                    if verbose and not quiet:
                        print(f"   [{i}/{len(input_paths)}] ❌ {path.name}: {e}")
    elif parallel_workers == 1:
        # Sequential processing
        for i, path in enumerate(input_paths, 1):
            try:
                result = _process_single_file(
                    path,
                    output_dir,
                    delimiter_char,
                    indent,
                    format_choice,
                    force_format
                )
                _update_results(results, result, path)
                
                if verbose and not quiet:
                    print(f"   [{i}/{len(input_paths)}] ✅ {path.name}")
                    
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({'file': str(path), 'error': str(e)})
                
                if verbose and not quiet:
                    print(f"   [{i}/{len(input_paths)}] ❌ {path.name}: {e}")
    
    # Calculate final statistics
    results['processing_time'] = time.time() - start_time
    results['output_directory'] = output_dir or "same as input files"
    
    if results['total_json_tokens'] > 0:
        results['average_savings'] = (
            results['total_tokens_saved'] / results['total_json_tokens'] * 100
        )
    else:
        results['average_savings'] = 0.0
    
    if not quiet:
        print(f"\n✅ Batch processing complete!")
        print(f"   Successful: {results['successful']}/{results['total_files']}")
        if results['failed'] > 0:
            print(f"   ⚠️  Failed: {results['failed']}")
    
    return results


def _process_single_file(
    path: Path,
    output_dir: Optional[str],
    delimiter: str,
    indent: int,
    format_choice: str,
    force_format: bool
) -> Dict:
    """Process a single file (used for parallel execution)"""
    from .toon_converter import process_json_file
    
    return process_json_file(
        str(path),
        output_dir,
        delimiter=delimiter,
        indent=indent,
        format_choice=format_choice,
        force_format=force_format
    )


def _update_results(results: Dict, file_result: Dict, path: Path):
    """Update batch results with single file result"""
    results['successful'] += 1
    results['files'].append({
        'input': str(path),
        'output': file_result['output_file'],
        'format': file_result['chosen_format'],
        'savings': file_result['savings_percentage']
    })
    
    # Update format counts
    format_name = file_result['chosen_format'].lower()
    if 'toon' in format_name and 'compact' not in format_name:
        results['toon_count'] += 1
    elif 'compact' in format_name:
        results['compact_count'] += 1
    else:
        results['json_count'] += 1
    
    # Update token statistics
    results['total_json_tokens'] += file_result['json_tokens']
    results['total_output_tokens'] += file_result['chosen_tokens']
    results['total_tokens_saved'] += file_result['savings_tokens']
