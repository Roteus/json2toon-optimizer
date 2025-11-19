"""
Example: Batch Processing Multiple JSON Files
Demonstrates how to process multiple files efficiently
"""

from json2toon import process_batch
from pathlib import Path
import json

# Example 1: Create sample JSON files
def create_sample_files():
    """Create sample JSON files for batch processing"""
    sample_dir = Path("batch_examples")
    sample_dir.mkdir(exist_ok=True)
    
    # Sample 1: User data
    users_data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25},
            {"id": 3, "name": "Carol", "email": "carol@example.com", "age": 35}
        ]
    }
    
    # Sample 2: Product catalog
    products_data = {
        "products": [
            {"sku": "A001", "name": "Widget", "price": 9.99, "stock": 100},
            {"sku": "A002", "name": "Gadget", "price": 14.99, "stock": 50},
            {"sku": "A003", "name": "Doohickey", "price": 24.99, "stock": 25}
        ]
    }
    
    # Sample 3: Analytics data
    analytics_data = {
        "metrics": {
            "pageviews": 15234,
            "unique_visitors": 3421,
            "bounce_rate": 0.42
        },
        "top_pages": [
            {"url": "/home", "views": 5421},
            {"url": "/products", "views": 3210},
            {"url": "/about", "views": 1876}
        ]
    }
    
    samples = [
        ("users.json", users_data),
        ("products.json", products_data),
        ("analytics.json", analytics_data)
    ]
    
    file_paths = []
    for filename, data in samples:
        file_path = sample_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        file_paths.append(file_path)
        print(f"✓ Created: {file_path}")
    
    return file_paths, sample_dir


# Example 2: Sequential batch processing
def example_sequential_batch():
    """Process files sequentially (one at a time)"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Sequential Batch Processing")
    print("="*60)
    
    file_paths, sample_dir = create_sample_files()
    output_dir = sample_dir / "output_sequential"
    output_dir.mkdir(exist_ok=True)
    
    result = process_batch(
        file_paths,
        output_dir=str(output_dir),
        parallel_workers=1,
        verbose=True
    )
    
    print(f"\n✅ Processed {result['successful']} files")
    print(f"💰 Total tokens saved: {result['total_tokens_saved']}")
    print(f"📊 Average savings: {result['average_savings']:.1f}%")


# Example 3: Parallel batch processing
def example_parallel_batch():
    """Process files in parallel (faster for many files)"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Parallel Batch Processing")
    print("="*60)
    
    file_paths, sample_dir = create_sample_files()
    output_dir = sample_dir / "output_parallel"
    output_dir.mkdir(exist_ok=True)
    
    result = process_batch(
        file_paths,
        output_dir=str(output_dir),
        parallel_workers=3,  # Use 3 workers
        verbose=True
    )
    
    print(f"\n⚡ Parallel processing complete!")
    print(f"⏱️  Time: {result['processing_time']:.2f}s")


# Example 4: Batch with custom format options
def example_custom_format():
    """Process files with custom format options"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Format Options")
    print("="*60)
    
    file_paths, sample_dir = create_sample_files()
    output_dir = sample_dir / "output_custom"
    output_dir.mkdir(exist_ok=True)
    
    result = process_batch(
        file_paths,
        output_dir=str(output_dir),
        delimiter='tab',      # Use tab delimiter
        indent=4,             # 4 spaces indentation
        format_choice='toon', # Prefer TOON format
        quiet=False,
        verbose=True
    )
    
    print(f"\n✅ Files processed with custom formatting")


# Example 5: Using glob patterns from command line
def example_cli_usage():
    """Show CLI usage examples"""
    print("\n" + "="*60)
    print("EXAMPLE 4: CLI Usage Examples")
    print("="*60)
    
    print("""
# Process all JSON files in a directory
json2toon examples/*.json --batch --stats

# Process recursively with pattern
json2toon examples/ --recursive --batch --pattern "*.json"

# Exclude test files
json2toon data/ --batch --exclude "test_*" --exclude "*_backup.json"

# Parallel processing with custom format
json2toon data/*.json --batch --parallel 4 --delimiter tab --indent 4

# Quiet mode (only show errors)
json2toon data/*.json --batch --quiet

# Verbose mode with statistics
json2toon data/*.json --batch --verbose --stats
    """)


if __name__ == "__main__":
    print("🚀 Batch Processing Examples for json2toon-optimizer")
    print("="*60)
    
    # Run examples
    example_sequential_batch()
    example_parallel_batch()
    example_custom_format()
    example_cli_usage()
    
    print("\n" + "="*60)
    print("✨ All examples completed!")
    print("="*60)
