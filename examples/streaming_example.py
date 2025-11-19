"""
Example: Streaming Large JSON Files
Demonstrates how to process very large files with minimal memory usage
"""

import json
from pathlib import Path

try:
    from json2toon import process_stream
    STREAMING_AVAILABLE = True
except ImportError:
    print("⚠️  Streaming requires 'ijson'. Install with: pip install ijson")
    STREAMING_AVAILABLE = False


# Example 1: Create a large JSON array file
def create_large_json_array():
    """Create a large JSON array file for testing"""
    output_file = Path("large_dataset.json")
    
    print("Creating large JSON array file (this may take a moment)...")
    
    # Create 10,000 records
    data = []
    for i in range(10000):
        record = {
            "id": i,
            "user_id": f"user_{i % 1000}",
            "timestamp": f"2025-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00Z",
            "event": ["click", "view", "purchase", "search"][i % 4],
            "value": round((i * 3.14) % 100, 2),
            "metadata": {
                "browser": ["chrome", "firefox", "safari"][i % 3],
                "device": ["desktop", "mobile", "tablet"][i % 3],
                "country": ["US", "UK", "DE", "FR", "JP"][i % 5]
            }
        }
        data.append(record)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    size_mb = output_file.stat().st_size / 1024 / 1024
    print(f"✓ Created: {output_file} ({size_mb:.2f} MB, {len(data):,} records)")
    
    return output_file


# Example 2: Stream process the large file
def example_stream_large_file():
    """Stream process a large file with minimal memory usage"""
    if not STREAMING_AVAILABLE:
        return
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Streaming Large JSON Array")
    print("="*60)
    
    input_file = create_large_json_array()
    output_dir = Path("streaming_output")
    output_dir.mkdir(exist_ok=True)
    
    print("\n🔄 Processing with streaming (low memory usage)...")
    
    result = process_stream(
        str(input_file),
        output_dir=str(output_dir),
        chunk_size=1000,  # Process 1000 records at a time
        verbose=True
    )
    
    print(f"\n✅ Streaming complete!")
    print(f"   Items processed: {result['items_processed']:,}")
    print(f"   Chunks: {result['chunks_processed']}")
    print(f"   Peak memory: {result['peak_memory_mb']:.1f} MB")
    print(f"   Time: {result['processing_time']:.2f}s")
    print(f"   Estimated savings: {result['estimated_savings_percent']:.1f}%")


# Example 3: Compare streaming vs regular processing
def example_memory_comparison():
    """Compare memory usage between streaming and regular processing"""
    if not STREAMING_AVAILABLE:
        return
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Memory Usage Comparison")
    print("="*60)
    
    print("""
Streaming Mode:
  ✅ Constant memory usage (~100-200 MB)
  ✅ Can process files larger than available RAM
  ✅ Ideal for files > 1 GB
  ⚠️  Slightly slower due to incremental processing
  ⚠️  Only works with JSON arrays at root level

Regular Mode:
  ✅ Faster processing
  ✅ Works with any JSON structure
  ⚠️  Loads entire file into memory
  ⚠️  May fail with very large files (> available RAM)

Recommendation:
  - Use streaming for files > 500 MB
  - Use regular mode for files < 500 MB
    """)


# Example 4: Streaming with custom options
def example_streaming_options():
    """Demonstrate different streaming options"""
    if not STREAMING_AVAILABLE:
        return
    
    print("\n" + "="*60)
    print("EXAMPLE 3: Streaming with Custom Options")
    print("="*60)
    
    input_file = create_large_json_array()
    output_dir = Path("streaming_custom")
    output_dir.mkdir(exist_ok=True)
    
    print("\n📊 Processing with custom chunk size...")
    
    result = process_stream(
        str(input_file),
        output_dir=str(output_dir),
        chunk_size=5000,     # Larger chunks (faster but more memory)
        delimiter='tab',      # Use tab delimiter
        indent=4,             # 4 spaces indentation
        quiet=False,
        verbose=True
    )
    
    print(f"\n✅ Custom streaming complete!")
    print(f"   Chunk size: 5000 items")
    print(f"   Total chunks: {result['chunks_processed']}")


# Example 5: CLI usage for streaming
def example_cli_streaming():
    """Show CLI usage examples for streaming"""
    print("\n" + "="*60)
    print("EXAMPLE 4: CLI Streaming Usage")
    print("="*60)
    
    print("""
# Basic streaming
json2toon large_file.json --stream

# Custom chunk size
json2toon large_file.json --stream --chunk-size 10000

# Streaming with custom format
json2toon large_file.json --stream --delimiter tab --indent 4

# Streaming with statistics
json2toon large_file.json --stream --stats --verbose

# Quiet mode (only show errors)
json2toon large_file.json --stream --quiet

Note: Streaming mode automatically detects if the JSON file contains
an array at the root level. If not, it will fallback to regular
processing mode.
    """)


# Example 6: Best practices
def example_best_practices():
    """Show best practices for streaming"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Streaming Best Practices")
    print("="*60)
    
    print("""
1. CHUNK SIZE SELECTION:
   - Small files (<10K items): chunk_size=1000
   - Medium files (10K-100K): chunk_size=5000
   - Large files (>100K): chunk_size=10000
   
   Trade-off: Larger chunks = faster but more memory

2. MEMORY MONITORING:
   - Use --verbose to see peak memory usage
   - Peak memory should stay < 500 MB
   - If memory exceeds 1 GB, reduce chunk_size

3. FILE FORMAT:
   - Streaming works best with:
     [{"item": 1}, {"item": 2}, ...]
   
   - Streaming may fallback for:
     {"data": [{"item": 1}, ...]}
     
4. PERFORMANCE:
   - Streaming: ~5-10 MB/s (depends on data structure)
   - Regular: ~20-50 MB/s
   - Use streaming only when necessary (files > 500 MB)

5. ERROR HANDLING:
   - Streaming processes incrementally
   - Errors affect only current chunk
   - Partial results are saved
    """)


if __name__ == "__main__":
    print("🚀 Streaming Examples for json2toon-optimizer")
    print("="*60)
    
    if not STREAMING_AVAILABLE:
        print("\n⚠️  Streaming functionality not available!")
        print("Install with: pip install ijson")
        print("or: pip install -e '.[stream]'")
    else:
        # Run examples
        example_stream_large_file()
        example_memory_comparison()
        example_streaming_options()
        example_cli_streaming()
        example_best_practices()
        
        print("\n" + "="*60)
        print("✨ All streaming examples completed!")
        print("="*60)
        
        # Cleanup
        print("\nCleanup: Remove example files? (y/n)")
        # Note: In production, you'd use input() here
