"""
Example: Advanced CLI Usage
Demonstrates all CLI features and options
"""

from pathlib import Path
import json

def create_example_data():
    """Create example JSON files for demonstrations"""
    examples_dir = Path("cli_examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Simple user data
    users = {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"}
        ]
    }
    
    # E-commerce data
    orders = {
        "orders": [
            {"order_id": "A001", "customer": "Alice", "total": 99.99, "items": 3},
            {"order_id": "A002", "customer": "Bob", "total": 149.50, "items": 5}
        ]
    }
    
    # Analytics data
    analytics = {
        "pageviews": 15234,
        "visitors": {
            "unique": 3421,
            "returning": 1876
        },
        "top_pages": [
            {"url": "/home", "views": 5421},
            {"url": "/products", "views": 3210}
        ]
    }
    
    files = [
        ("users.json", users),
        ("orders.json", orders),
        ("analytics.json", analytics)
    ]
    
    for filename, data in files:
        filepath = examples_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    print(f"✓ Created example files in {examples_dir}/")
    return examples_dir


def print_section(title):
    """Print formatted section title"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def example_basic_usage():
    """Basic CLI usage examples"""
    print_section("1. BASIC USAGE")
    
    print("""
# Convert single file (auto-detect best format)
json2toon data.json

# Specify output directory
json2toon data.json --output ./results

# Show detailed statistics
json2toon data.json --stats

# Quiet mode (no output except errors)
json2toon data.json --quiet

# Verbose mode (detailed progress)
json2toon data.json --verbose
    """)


def example_format_options():
    """Format customization examples"""
    print_section("2. FORMAT OPTIONS")
    
    print("""
# Use tab delimiter instead of comma
json2toon data.json --delimiter tab

# Use pipe delimiter
json2toon data.json --delimiter pipe

# Custom indentation (4 spaces)
json2toon data.json --indent 4

# Force TOON format (even if JSON is better)
json2toon data.json --format toon --force

# Force JSON output
json2toon data.json --format json --force

# Force compact TOON format
json2toon data.json --format compact --force

# Combine options
json2toon data.json --delimiter tab --indent 4 --format toon
    """)


def example_batch_processing():
    """Batch processing examples"""
    print_section("3. BATCH PROCESSING")
    
    print("""
# Process all JSON files in directory
json2toon data/*.json --batch

# Process recursively
json2toon data/ --recursive --batch

# Custom file pattern
json2toon data/ --recursive --batch --pattern "user_*.json"

# Exclude files
json2toon data/ --batch --exclude "test_*" --exclude "*_backup.json"

# Parallel processing (4 workers)
json2toon data/*.json --batch --parallel 4

# Batch with statistics
json2toon data/*.json --batch --stats

# Batch with verbose output
json2toon data/*.json --batch --verbose
    """)


def example_streaming():
    """Streaming examples"""
    print_section("4. STREAMING (Large Files)")
    
    print("""
# Stream large file (minimal memory)
json2toon large_dataset.json --stream

# Custom chunk size (items per chunk)
json2toon large_dataset.json --stream --chunk-size 5000

# Streaming with format options
json2toon large_dataset.json --stream --delimiter tab --indent 4

# Streaming with statistics
json2toon large_dataset.json --stream --stats --verbose

# When to use streaming:
  - Files larger than 500 MB
  - Files that don't fit in RAM
  - JSON arrays with many items
    """)


def example_combined_workflows():
    """Combined workflow examples"""
    print_section("5. COMBINED WORKFLOWS")
    
    print("""
# Batch + Parallel + Custom Format
json2toon data/*.json \\
  --batch \\
  --parallel 4 \\
  --delimiter tab \\
  --indent 4 \\
  --stats

# Batch + Exclude + Force Format
json2toon data/ \\
  --recursive \\
  --batch \\
  --exclude "test_*" \\
  --exclude "*_temp.json" \\
  --format toon \\
  --force \\
  --verbose

# Stream + Custom Format + Stats
json2toon huge_file.json \\
  --stream \\
  --chunk-size 10000 \\
  --delimiter pipe \\
  --stats \\
  --verbose
    """)


def example_use_cases():
    """Real-world use case examples"""
    print_section("6. REAL-WORLD USE CASES")
    
    print("""
# Use Case 1: Optimize API responses for LLM context
json2toon api_responses/*.json --batch --parallel 4 --stats
# → Reduces token usage by ~40% on average

# Use Case 2: Process database export
json2toon db_export.json --stream --chunk-size 5000
# → Handles multi-GB files with constant memory

# Use Case 3: Prepare training data for AI
json2toon training_data/*.json \\
  --batch \\
  --recursive \\
  --format toon \\
  --force \\
  --delimiter tab
# → Consistent format, optimal for tokenization

# Use Case 4: Migrate configuration files
json2toon configs/ \\
  --recursive \\
  --batch \\
  --pattern "*.config.json" \\
  --output ./migrated
# → Batch convert all config files

# Use Case 5: Analyze token costs
json2toon prompts/ --recursive --batch --stats --verbose
# → See detailed token savings per file
    """)


def example_troubleshooting():
    """Troubleshooting and tips"""
    print_section("7. TROUBLESHOOTING")
    
    print("""
# Problem: "Command 'json2toon' not found"
# Solution: Ensure package is installed
pip install -e .
# or
python -m json2toon.cli data.json

# Problem: Out of memory with large files
# Solution: Use streaming mode
json2toon large.json --stream --chunk-size 1000

# Problem: Slow batch processing
# Solution: Use parallel processing
json2toon data/*.json --batch --parallel 4

# Problem: Want to see what's happening
# Solution: Use verbose mode
json2toon data.json --verbose

# Problem: Need to test without saving
# Solution: Use --quiet to suppress output
json2toon data.json --quiet

# Problem: Streaming not available
# Solution: Install ijson
pip install ijson
# or
pip install -e ".[stream]"
    """)


def example_comparison_table():
    """Show comparison table of processing modes"""
    print_section("8. PROCESSING MODES COMPARISON")
    
    print("""
+----------------+-------------+-------------+-------------+
| Feature        | Single      | Batch       | Streaming   |
+----------------+-------------+-------------+-------------+
| File size      | < 100 MB    | Any         | > 500 MB    |
| Speed          | Fast        | Fast        | Medium      |
| Memory usage   | Moderate    | Moderate    | Low         |
| Parallel       | No          | Yes         | No          |
| Progress       | Basic       | Detailed    | Incremental |
| Best for       | Quick tests | Production  | Huge files  |
+----------------+-------------+-------------+-------------+

RECOMMENDATIONS:

1. Single file < 100 MB:
   json2toon file.json --stats

2. Multiple files (total < 10 GB):
   json2toon files/*.json --batch --parallel 4 --stats

3. Single file > 500 MB:
   json2toon huge.json --stream --chunk-size 5000

4. Mixed workload:
   json2toon data/ --recursive --batch --parallel 4
    """)


if __name__ == "__main__":
    print("🚀 Advanced CLI Usage Examples")
    print("json2toon-optimizer v2.0.0")
    print("="*70)
    
    # Create example data
    examples_dir = create_example_data()
    
    # Show all examples
    example_basic_usage()
    example_format_options()
    example_batch_processing()
    example_streaming()
    example_combined_workflows()
    example_use_cases()
    example_troubleshooting()
    example_comparison_table()
    
    print(f"\n{'='*70}")
    print("✨ CLI Examples Complete!")
    print(f"{'='*70}")
    print(f"\n📁 Try the examples with files in: {examples_dir}/")
    print("\nFor more help: json2toon --help")
