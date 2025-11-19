#!/usr/bin/env python
"""
Interactive demo script for json2toon-optimizer
Shows step-by-step examples of conversion rules
"""

import json
from json2toon import TOONEncoder, TokenCounter


def print_section(title: str):
    """Prints a formatted section title"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_example(title: str, json_data: dict, description: str = ""):
    """Demonstrates a conversion example"""
    print(f"\n📌 {title}")
    if description:
        print(f"   {description}")
    
    # Original JSON
    json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
    print("\n   JSON:")
    for line in json_str.split('\n'):
        print(f"   {line}")
    
    # JSON token analysis
    json_tokens = TokenCounter.count_tokens(json_str)
    json_chars = len(json_str)
    
    # Convert to TOON
    encoder = TOONEncoder()
    toon_str = encoder.encode(json_data)
    
    # TOON token analysis
    toon_tokens = TokenCounter.count_tokens(toon_str)
    toon_chars = len(toon_str)
    
    print("\n   TOON:")
    for line in toon_str.split('\n'):
        print(f"   {line}")
    
    # Comparison
    savings = json_tokens - toon_tokens
    savings_pct = (savings / json_tokens * 100) if json_tokens > 0 else 0
    
    print(f"\n   📊 Tokens: JSON={json_tokens} ({json_chars} chars) → TOON={toon_tokens} ({toon_chars} chars)")
    print(f"   💰 Savings: {savings} tokens ({savings_pct:.1f}%)")


def main():
    """Runs demonstrations"""
    print_section("DEMO - json2toon-optimizer in Python")
    
    print("""
    This script demonstrates JSON → TOON conversion rules
    with automatic token savings calculation.
    
    Each example shows:
    • Original JSON data
    • Conversion to TOON format
    • Token analysis (characters ÷ 4)
    • Percentage savings
    """)
    
    # Example 1: Simple Object
    demo_example(
        "Example 1: Simple Object",
        {
            "id": 123,
            "name": "Ada",
            "active": True
        },
        "Simple key-value without nested structures"
    )
    
    # Example 2: Nested Object
    demo_example(
        "Example 2: Nested Object",
        {
            "user": {
                "id": 123,
                "name": "Ada Lovelace"
            }
        },
        "Nested objects save with efficient indentation"
    )
    
    # Example 3: Array of Primitives
    demo_example(
        "Example 3: Array of Primitives (inline)",
        {
            "tags": ["admin", "ops", "dev"]
        },
        "Arrays of primitives in a single line"
    )
    
    # Example 4: Array of Uniform Objects (MAX SAVINGS!)
    demo_example(
        "Example 4: Array of Uniform Objects (TABULAR)",
        {
            "items": [
                {"sku": "A1", "qty": 2, "price": 9.99},
                {"sku": "B2", "qty": 1, "price": 14.5}
            ]
        },
        "❗ Maximum savings! Keys are not repeated in each line."
    )
    
    # Example 5: Mixed Array
    demo_example(
        "Example 5: Mixed Array (list format)",
        {
            "items": [1, {"a": 1}, "text"]
        },
        "Mixed arrays use list format with hyphen (-)"
    )
    
    # Example 6: Array of Arrays
    demo_example(
        "Example 6: Array of Arrays",
        {
            "pairs": [[1, 2], [3, 4]]
        },
        "Nested arrays maintain clear structure"
    )
    
    # Example 7: Root Array
    demo_example(
        "Example 7: Root Array",
        {"root_array": ["x", "y", "z"]},
        "Arrays at the top of the structure without named field"
    )
    
    # Example 8: Complex and Realistic Data
    demo_example(
        "Example 8: Realistic Data (Combination)",
        {
            "company": "TechCorp",
            "employees": [
                {"id": 1, "name": "Alice", "salary": 95000},
                {"id": 2, "name": "Bob", "salary": 85000},
                {"id": 3, "name": "Carol", "salary": 90000}
            ],
            "summary": {
                "count": 3,
                "avg_salary": 90000
            }
        },
        "Combination of different structures with tabular"
    )
    
    # Summary
    print_section("📚 Rules Summary")
    
    print("""
    1. SIMPLE OBJECTS
       {"id": 1, "name": "Ada"} → id: 1 / name: Ada
    
    2. NESTED OBJECTS
       {"user": {"id": 1}} → user: / (space) id: 1
    
    3. ARRAYS OF PRIMITIVES
       {"tags": ["a", "b"]} → tags[2]: a,b
    
    4. TABULAR ARRAYS ⭐ (Maximum savings!)
       {"items": [{"id": 1, "qty": 5}, {"id": 2, "qty": 3}]}
       →
       items[2]{id,qty}:
         1,5
         2,3
    
    5. MIXED ARRAYS
       {"items": [1, "x", null]} → items[3]: / - 1 / - x / - null
    
    6. TOKENS
       Estimate: ceil(characters / 4)
       Typical savings: 30-50% in structured data
    """)
    
    print_section("💡 Final Tip")
    print("""
    For maximum savings, structure your data with arrays of
    uniform objects. Each field is not repeated, saving
    up to 50% or more in tokens!
    """)


if __name__ == '__main__':
    main()
