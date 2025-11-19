"""Configuration module and CLI for json2toon-optimizer"""

import sys
import argparse
from pathlib import Path


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="json2toon-optimizer - Converts JSON to TOON with token optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  json2toon data.json
  json2toon data.json --output ./results
  json2toon data.json --show-analysis
        """,
    )

    parser.add_argument(
        "input",
        help="Input JSON file",
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output directory (default: same as input)",
    )

    parser.add_argument(
        "-a",
        "--show-analysis",
        action="store_true",
        help="Show detailed token analysis",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 2.0.0",
    )

    args = parser.parse_args()

    # Import here to avoid circular import
    from .toon_converter import process_json_file

    try:
        result = process_json_file(args.input, args.output)

        if args.show_analysis:
            print("\n📊 Detailed Analysis:")
            print(f"   Chosen format: {result['chosen_format']}")
            print(f"   JSON tokens (minified): {result['json_tokens']}")
            print(f"   TOON tokens: {result['toon_tokens']}")
            print(f"   TOON tokens (compact): {result['toon_compact_tokens']}")
            print(f"   Savings: {result['savings_tokens']} tokens ({result['savings_percentage']:.1f}%)")
            print(f"   File saved: {result['output_file']}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
