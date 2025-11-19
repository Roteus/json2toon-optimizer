"""
TOON Format Converter - JSON ↔ TOON with token estimation
Based on: https://github.com/toon-format/toon

Token estimation rule: ~1 token per 4 characters
(4 characters per token is OpenAI's guideline)
"""

import json
import re
import math
from pathlib import Path
from typing import Any, Dict, List, Union, Tuple


class TokenCounter:
    """Token counter.

    Calculation priority:
    1. If the `tiktoken` package is available, uses `cl100k_base` encoding to count tokens
       (recommended — matches the tokenizer used by modern models).
    2. Otherwise, uses approximate fallback: ceil(len(text) / 4).

    Note: using `tiktoken` provides counts exactly compatible with CL100K tokenizers
    (more accurate for billing and model limits). The fallback is a conservative estimate.
    """

    _use_tiktoken = False
    _encoding = None

    # Try to initialize tiktoken on import (if available)
    try:
        import tiktoken  # type: ignore
        _encoding = tiktoken.get_encoding("cl100k_base")
        _use_tiktoken = True
    except Exception:
        _use_tiktoken = False
        _encoding = None

    @staticmethod
    def count_tokens(text: str) -> int:
        """Counts tokens using tiktoken/cl100k_base when available, otherwise uses fallback (ceil(chars/4))."""
        if TokenCounter._use_tiktoken and TokenCounter._encoding is not None:
            try:
                # tiktoken Encoding has encode() that returns list of token ids
                token_ids = TokenCounter._encoding.encode(text)
                return len(token_ids)
            except Exception:
                # In case of unexpected error with tiktoken, use fallback
                return math.ceil(len(text) / 4)
        # Conservative fallback
        return math.ceil(len(text) / 4)

    @staticmethod
    def analyze(text: str) -> Dict[str, Union[int, str]]:
        """Returns complete text analysis (characters, tokens, lines, etc)

        Includes a `tokenizer` field indicating whether `cl100k_base` or `fallback` was used.
        """
        lines = text.split('\n')
        words = text.split()
        tokens = TokenCounter.count_tokens(text)
        tokenizer = 'cl100k_base' if TokenCounter._use_tiktoken and TokenCounter._encoding is not None else 'fallback'

        return {
            'characters': len(text),
            'lines': len(lines),
            'words': len(words),
            'tokens': tokens,
            'tokenizer': tokenizer
        }


class CompactTOONEncoder:
    """JSON → Compact TOON encoder (schema + flattened values)
    
    Format: {schema}:flattened,values
    Example: {nome,age,itens[2]{id,qty}}:Ana,25,A1,5,B2,10
    """
    
    def encode(self, value: Any) -> str:
        """Converts JSON to compact TOON"""
        schema = self._build_schema(value)
        values = self._flatten_values(value)
        
        if not values:
            return schema + ':'
        
        return f"{schema}:{','.join(values)}"
    
    def _build_schema(self, value: Any, parent_key: str = '') -> str:
        """Builds the schema (structure) of the data"""
        if isinstance(value, dict):
            if not value:
                return '{}'
            keys = ','.join(self._build_schema(v, k) if isinstance(v, (dict, list)) else k 
                          for k, v in value.items())
            return f"{{{keys}}}" if not parent_key else f"{parent_key}{{{keys}}}"
        
        elif isinstance(value, list):
            if not value:
                return '[]'
            count = len(value)
            # All items have the same structure (assuming homogeneity)
            if value and isinstance(value[0], (dict, list)):
                item_schema = self._build_schema(value[0])
                return f"[{count}]{item_schema}" if not parent_key else f"{parent_key}[{count}]{item_schema}"
            else:
                # Array of primitives
                return f"[{count}]" if not parent_key else f"{parent_key}[{count}]"
        
        else:
            # Primitive
            return parent_key if parent_key else str(value)
    
    def _flatten_values(self, value: Any) -> List[str]:
        """Flattens all values into a linear list"""
        result = []
        
        if isinstance(value, dict):
            for v in value.values():
                result.extend(self._flatten_values(v))
        
        elif isinstance(value, list):
            for item in value:
                result.extend(self._flatten_values(item))
        
        else:
            # Primitive
            result.append(self._format_primitive(value))
        
        return result
    
    def _format_primitive(self, value: Any) -> str:
        """Formats a primitive value"""
        if value is None or value == '':
            return ''
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            # If contains comma or special characters, needs quotes
            if ',' in value or ':' in value or '{' in value or '}' in value or '[' in value or ']' in value:
                return f'"{value}"'
            return value
        return str(value)


class TOONEncoder:
    """JSON → TOON Encoder"""
    
    def __init__(self, indent: int = 2, delimiter: str = ',', 
                 key_folding: str = 'off', flatten_depth: float = float('inf')):
        self.indent = indent
        self.delimiter = delimiter
        self.key_folding = key_folding
        self.flatten_depth = flatten_depth
    
    def encode(self, value: Any) -> str:
        """Converts a JSON value to TOON format"""
        if value is None or value == {} or value == []:
            result = self._encode_value(value, depth=0)
            # Empty root objects return empty string
            if value == {} and result == '':
                return ''
            return result
        
        result = self._encode_value(value, depth=0)
        return result
    
    def _encode_value(self, value: Any, depth: int = 0) -> str:
        """Generic encoder that identifies the type and calls the appropriate method"""
        if isinstance(value, dict):
            return self._encode_object(value, depth)
        elif isinstance(value, list):
            return self._encode_array(value, depth)
        else:
            return self._encode_primitive(value)
    
    def _encode_primitive(self, value: Any) -> str:
        """Encodes primitive values (string, number, boolean, null)"""
        if value is None:
            return 'null'
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, str):
            return self._quote_string(value)
        if isinstance(value, float):
            if math.isnan(value) or math.isinf(value):
                return 'null'
            if value == int(value):
                return str(int(value))
            return str(value)
        if isinstance(value, int):
            return str(value)
        # Handle other types by converting to null
        return 'null'
    
    def _quote_string(self, s: str) -> str:
        """Determines if a string needs quotes and encodes it"""
        # Rules for when NOT to quote:
        # - Empty string needs quotes
        if s == '':
            return '""'
        
        # - Space at beginning or end
        if s != s.strip():
            return f'"{self._escape_string(s)}"'
        
        # - Contains special characters
        if any(c in s for c in [self.delimiter, ':', '"', '\\', '\n', '\r', '\t']):
            return f'"{self._escape_string(s)}"'
        
        # - Looks like boolean, number or null
        if s in ('true', 'false', 'null'):
            return f'"{s}"'
        if re.match(r'^-?\d+(\.\d+)?([eE][+-]?\d+)?$', s):
            return f'"{s}"'
        if s.startswith('0') and len(s) > 1 and s[1].isdigit():
            return f'"{s}"'
        
        # - Starts with "- " (list item)
        if s.startswith('- '):
            return f'"{self._escape_string(s)}"'
        
        # - Looks like structural token
        if re.match(r'^\[\d\w*\]', s) or re.match(r'^\{.*\}', s):
            return f'"{self._escape_string(s)}"'
        
        # If no rule applies, return without quotes
        return s
    
    def _escape_string(self, s: str) -> str:
        """Escapes special characters in strings"""
        s = s.replace('\\', '\\\\')
        s = s.replace('"', '\\"')
        s = s.replace('\n', '\\n')
        s = s.replace('\r', '\\r')
        s = s.replace('\t', '\\t')
        return s
    
    def _is_valid_identifier(self, key: str) -> bool:
        """Checks if a key is a valid identifier (without quotes)"""
        if not key:
            return False
        if key[0] not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
            return False
        for c in key[1:]:
            if c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.':
                return False
        return True
    
    def _format_key(self, key: str) -> str:
        """Formats a key with or without quotes as needed"""
        if self._is_valid_identifier(key):
            return key
        return f'"{self._escape_string(key)}"'
    
    def _encode_object(self, obj: Dict, depth: int = 0) -> str:
        """Encodes an object"""
        if not obj:  # Empty object
            return ''
        
        lines = []
        
        for key, val in obj.items():
            formatted_key = self._format_key(key)
            
            if isinstance(val, dict):
                lines.append(self._encode_dict_field(formatted_key, val, depth))
            elif isinstance(val, list):
                lines.append(self._encode_list_field(formatted_key, val, depth))
            else:
                val_str = self._encode_primitive(val)
                lines.append(f'{formatted_key}: {val_str}')
        
        return '\n'.join(lines)
    
    def _encode_dict_field(self, key: str, val: Dict, depth: int) -> str:
        """Encodes an object field within an object"""
        if not val:  # Empty object
            return f'{key}:'
        
        nested = self._encode_object(val, depth + 1)
        nested_lines = nested.split('\n')
        lines = [f'{key}:']
        
        for nested_line in nested_lines:
            if nested_line:
                lines.append(' ' * self.indent + nested_line)
        
        return '\n'.join(lines)
    
    def _encode_list_field(self, key: str, val: List, depth: int) -> str:
        """Encodes an array field within an object"""
        array_str = self._encode_array(val, depth + 1)
        
        if '\n' in array_str:
            array_lines = array_str.split('\n')
            lines = [f'{key}{array_lines[0]}']
            for array_line in array_lines[1:]:
                if array_line:
                    lines.append(' ' * self.indent + array_line)
            return '\n'.join(lines)
        else:
            return f'{key}{array_str}'
    
    def _is_uniform_object_array(self, arr: List) -> bool:
        """Checks if the array consists of uniform objects (same keys, primitive values)"""
        if not arr or not isinstance(arr[0], dict):
            return False
        
        # All elements must be dicts
        for item in arr:
            if not isinstance(item, dict):
                return False
        
        # All dicts must have the same keys
        first_keys = set(arr[0].keys())
        for item in arr[1:]:
            if set(item.keys()) != first_keys:
                return False
        
        # All values must be primitives
        for item in arr:
            for val in item.values():
                if isinstance(val, (dict, list)):
                    return False
        
        return True
    
    def _encode_array(self, arr: List, depth: int = 0) -> str:
        """Encodes an array"""
        length = len(arr)
        
        # Empty array
        if length == 0:
            return '[0]:'
        
        # Array of primitives (inline)
        if all(not isinstance(item, (dict, list)) for item in arr):
            values = [self._encode_primitive(item) for item in arr]
            return f'[{length}]: {self.delimiter.join(values)}'
        
        # Array of uniform objects (tabular)
        if self._is_uniform_object_array(arr):
            return self._encode_tabular_array(arr, depth)
        
        # Mixed or non-uniform array (list)
        return self._encode_list_array(arr, depth)
    
    def _encode_tabular_array(self, arr: List[Dict], depth: int = 0) -> str:
        """Encodes array of uniform objects in tabular format"""
        if not arr:
            return '[0]:'
        
        # Get keys from first object
        keys = list(arr[0].keys())
        delimiter_in_header = self.delimiter if self.delimiter != ',' else ''
        
        # Header
        header = f'[{len(arr)}{delimiter_in_header}]{{{self.delimiter.join(keys)}}}'
        
        # Lines
        lines = [header]
        indent_str = ' ' * (depth * self.indent)
        
        for obj in arr:
            values = [self._encode_primitive(obj[key]) for key in keys]
            line = indent_str + self.delimiter.join(values)
            lines.append(line)
        
        return '\n'.join(lines)
    
    def _encode_list_array(self, arr: List, depth: int = 0) -> str:
        """Encodes mixed/non-uniform array in list format"""
        lines = [f'[{len(arr)}]:']
        indent_str = ' ' * ((depth + 1) * self.indent)
        
        for item in arr:
            if isinstance(item, dict):
                lines.append(self._encode_list_item_dict(item, indent_str, depth))
            elif isinstance(item, list):
                arr_str = self._encode_array(item, depth + 2)
                lines.append(f'{indent_str}- {arr_str}')
            else:
                val_str = self._encode_primitive(item)
                lines.append(f'{indent_str}- {val_str}')
        
        return '\n'.join(lines)
    
    def _encode_list_item_dict(self, obj: Dict, indent_str: str, depth: int) -> str:
        """Encodes an object within a list item"""
        if not obj:
            return f'{indent_str}- '
        
        obj_str = self._encode_object(obj, depth + 1)
        obj_lines = obj_str.split('\n')
        result = [f'{indent_str}- {obj_lines[0]}']
        
        for obj_line in obj_lines[1:]:
            if obj_line:
                result.append(indent_str + obj_line)
        
        return '\n'.join(result)


def process_json_file(input_file: str, output_dir: str = None) -> Dict[str, Any]:
    """
    Processes a JSON file:
    1. Reads the JSON
    2. Calculates JSON tokens
    3. Converts to TOON
    4. Calculates TOON tokens
    5. Saves the format with fewer tokens
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_file}")
    
    if output_dir is None:
        output_dir = str(input_path.parent)
    else:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Read JSON
    print(f"\n📖 Reading file: {input_file}")
    with open(input_path, 'r', encoding='utf-8') as f:
        json_content = f.read()
    
    json_data = json.loads(json_content)
    
    # Minify JSON first (so we count tokens of what will actually be saved)
    minified_json = json.dumps(json_data, ensure_ascii=False, separators=(',', ':'))
    
    # Count tokens of minified JSON (what will actually be saved)
    json_analysis = TokenCounter.analyze(minified_json)
    print(f"   JSON (minified): {json_analysis['characters']} characters → {json_analysis['tokens']} tokens")
    
    # Convert to TOON
    print("\nConverting to TOON...")
    encoder = TOONEncoder()
    toon_content = encoder.encode(json_data)
    
    # Count TOON tokens
    toon_analysis = TokenCounter.analyze(toon_content)
    print(f"   TOON: {toon_analysis['characters']} characters → {toon_analysis['tokens']} tokens")
    
    # Convert to TOON Compact
    compact_encoder = CompactTOONEncoder()
    toon_compact = compact_encoder.encode(json_data)
    
    # Count TOON Compact tokens
    toon_compact_analysis = TokenCounter.analyze(toon_compact)
    print(f"   TOON (compact): {toon_compact_analysis['characters']} characters → {toon_compact_analysis['tokens']} tokens")
    
    # Comparison between 3 formats
    print("\nComparison:")
    print(f"   JSON tokens (minified):  {json_analysis['tokens']}")
    print(f"   TOON tokens:             {toon_analysis['tokens']}")
    print(f"   TOON tokens (compact):   {toon_compact_analysis['tokens']}")
    
    # Determine the most economical format
    formats = [
        ('JSON', json_analysis['tokens'], minified_json, '.json'),
        ('TOON', toon_analysis['tokens'], toon_content, '.toon'),
        ('TOON-COMPACT', toon_compact_analysis['tokens'], toon_compact, '.toon')
    ]
    
    # Sort by tokens (smallest first)
    formats.sort(key=lambda x: x[1])
    chosen_format_name, chosen_tokens, chosen_content, _ = formats[0]
    
    # Calculate savings vs JSON
    savings = json_analysis['tokens'] - chosen_tokens
    savings_pct = (savings / json_analysis['tokens'] * 100) if json_analysis['tokens'] > 0 else 0
    
    print(f"\n🏆 Best format: {chosen_format_name}")
    print(f"   Savings vs JSON: {savings} tokens ({savings_pct:.1f}%)")
    
    # Save the most economical format
    stem = input_path.stem
    
    if chosen_format_name == 'JSON':
        output_file = Path(output_dir) / f"{stem}-min.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chosen_content)
        print(f"\n✅ Saved in minified JSON format: {output_file}")
    elif chosen_format_name == 'TOON-COMPACT':
        output_file = Path(output_dir) / f"{stem}-min-compact.toon"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chosen_content)
        print(f"\n✅ Saved in compact TOON format: {output_file}")
    else:  # TOON
        output_file = Path(output_dir) / f"{stem}-min.toon"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chosen_content)
        print(f"\n✅ Saved in TOON format: {output_file}")
    
    return {
        'input_file': str(input_path),
        'output_file': str(output_file),
        'json_tokens': json_analysis['tokens'],
        'toon_tokens': toon_analysis['tokens'],
        'toon_compact_tokens': toon_compact_analysis['tokens'],
        'savings_tokens': savings,
        'savings_percentage': savings_pct,
        'chosen_format': chosen_format_name,
        'chosen_tokens': chosen_tokens,
        'json_content': json_content,
        'toon_content': toon_content,
        'toon_compact': toon_compact
    }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python toon_converter.py <file.json> [output_directory]")
        print("\nExample:")
        print("  python toon_converter.py data.json")
        print("  python toon_converter.py data.json ./output")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = process_json_file(input_file, output_dir)
        print(f"\n{'='*60}")
        print(f"Final result: {result['chosen_format']} ({result['chosen_tokens']} tokens)")
        print(f"{'='*60}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
