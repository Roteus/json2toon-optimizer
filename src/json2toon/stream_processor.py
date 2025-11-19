"""Streaming processor for very large JSON files"""

import json
import time
import tracemalloc
from pathlib import Path
from typing import Dict, Iterator, Any, Optional


def process_stream(
    input_file: str,
    output_dir: Optional[str] = None,
    chunk_size: int = 1000,
    delimiter: str = "comma",
    indent: int = 2,
    quiet: bool = False,
    verbose: bool = False
) -> Dict:
    """
    Process large JSON files using streaming to minimize memory usage
    
    Args:
        input_file: Input JSON file path
        output_dir: Output directory
        chunk_size: Number of items to process per chunk
        delimiter: Delimiter for arrays (comma/tab/pipe)
        indent: Indentation spaces
        quiet: Suppress output
        verbose: Show detailed progress
        
    Returns:
        Dictionary with streaming statistics
    """
    from .toon_converter import TOONEncoder, TokenCounter
    
    tracemalloc.start()
    start_time = time.time()
    
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Determine output file
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path / f"{input_path.stem}-min.toon"
    else:
        output_file = input_path.parent / f"{input_path.stem}-min.toon"
    
    # Convert delimiter name to character
    delimiter_map = {
        'comma': ',',
        'tab': '\t',
        'pipe': '|'
    }
    delimiter_char = delimiter_map.get(delimiter, ',')
    
    encoder = TOONEncoder(delimiter=delimiter_char, indent=indent)
    
    if not quiet:
        print(f"\n🔄 Streaming: {input_path.name}")
        if verbose:
            print(f"   Chunk size: {chunk_size}")
            print(f"   Output: {output_file}")
    
    try:
        # Try to stream as array
        items_processed, chunks_processed, estimated_json_tokens, estimated_toon_tokens = \
            _stream_json_array(input_path, output_file, encoder, chunk_size, verbose, quiet)
        
    except Exception as e:
        if verbose and not quiet:
            print(f"   ⚠️  Cannot stream as array, processing as single object: {e}")
        
        # Fallback: process as single large object
        items_processed, chunks_processed, estimated_json_tokens, estimated_toon_tokens = \
            _process_large_object(input_path, output_file, encoder, verbose, quiet)
    
    # Get memory statistics
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    processing_time = time.time() - start_time
    
    # Calculate results
    estimated_tokens_saved = estimated_json_tokens - estimated_toon_tokens
    estimated_savings_percent = (
        (estimated_tokens_saved / estimated_json_tokens * 100)
        if estimated_json_tokens > 0 else 0.0
    )
    
    result = {
        'input_file': str(input_path),
        'output_file': str(output_file),
        'chunks_processed': chunks_processed,
        'items_processed': items_processed,
        'estimated_tokens_saved': estimated_tokens_saved,
        'estimated_savings_percent': estimated_savings_percent,
        'processing_time': processing_time,
        'peak_memory_mb': peak / 1024 / 1024
    }
    
    if not quiet:
        print(f"\n✅ Streaming complete!")
        print(f"   Processed: {items_processed:,} items in {chunks_processed} chunks")
        print(f"   Peak memory: {result['peak_memory_mb']:.1f} MB")
    
    return result


def _stream_json_array(
    input_path: Path,
    output_file: Path,
    encoder,
    chunk_size: int,
    verbose: bool,
    quiet: bool
) -> tuple:
    """Stream process a JSON array file"""
    try:
        import ijson
    except ImportError:
        raise ImportError(
            "ijson is required for streaming. Install with: pip install ijson"
        )
    
    from .toon_converter import TokenCounter
    
    items_processed = 0
    chunks_processed = 0
    estimated_json_tokens = 0
    estimated_toon_tokens = 0
    
    with open(input_path, 'rb') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        # Write array header
        parser = ijson.items(f_in, 'item')
        
        chunk = []
        for item in parser:
            chunk.append(item)
            items_processed += 1
            
            if len(chunk) >= chunk_size:
                # Process chunk
                chunk_json = json.dumps(chunk, ensure_ascii=False, separators=(',', ':'))
                chunk_toon = encoder.encode(chunk)
                
                # Update token estimates
                estimated_json_tokens += TokenCounter.count_tokens(chunk_json)
                estimated_toon_tokens += TokenCounter.count_tokens(chunk_toon)
                
                # Write to output
                f_out.write(chunk_toon)
                f_out.write('\n')
                f_out.flush()
                
                chunks_processed += 1
                chunk = []
                
                if verbose and not quiet and chunks_processed % 10 == 0:
                    print(f"   Processed {items_processed:,} items ({chunks_processed} chunks)...")
        
        # Process remaining items
        if chunk:
            chunk_json = json.dumps(chunk, ensure_ascii=False, separators=(',', ':'))
            chunk_toon = encoder.encode(chunk)
            
            estimated_json_tokens += TokenCounter.count_tokens(chunk_json)
            estimated_toon_tokens += TokenCounter.count_tokens(chunk_toon)
            
            f_out.write(chunk_toon)
            f_out.flush()
            
            chunks_processed += 1
    
    return items_processed, chunks_processed, estimated_json_tokens, estimated_toon_tokens


def _process_large_object(
    input_path: Path,
    output_file: Path,
    encoder,
    verbose: bool,
    quiet: bool
) -> tuple:
    """Process a large JSON object (fallback when streaming fails)"""
    from .toon_converter import TokenCounter
    
    if verbose and not quiet:
        print("   Processing as single large object...")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Encode to TOON
    toon_content = encoder.encode(data)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(toon_content)
    
    # Calculate tokens
    json_minified = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    estimated_json_tokens = TokenCounter.count_tokens(json_minified)
    estimated_toon_tokens = TokenCounter.count_tokens(toon_content)
    
    return 1, 1, estimated_json_tokens, estimated_toon_tokens
