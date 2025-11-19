# 🏗️ json2toon-optimizer v2 Architecture

## Overview

json2toon-optimizer v2 is a Python application that implements JSON ↔ TOON conversion with intelligent token counting via `tiktoken` (cl100k_base) with automatic fallback.

```
┌─────────────────────────────────────┐
│          Input JSON File            │
│   (examples/{simple,intermediate}/) │
└──────────────┬──────────────────────┘
               │
               ▼
       ┌──────────────────┐
       │ TokenCounter.py  │
       │  analyze(json)   │  ◄─ Counts minified JSON tokens
       └────────┬─────────┘
                │
       ┌────────▼──────────┐
       │ TOONEncoder.py    │
       │  encode(json)     │  ◄─ Converts to TOON
       └────────┬──────────┘
                │
       ┌────────▼──────────────┐
       │ TokenCounter.py       │
       │ analyze(toon)         │  ◄─ Counts TOON tokens
       └────────┬──────────────┘
                │
       ┌────────▼──────────────────────┐
       │      Token Comparison         │
       │       (JSON vs TOON)          │
       └────────┬─────────────┬────────┘
                │             │
         ┌──────▼────┐   ┌────▼──────┐
         │  TOON <   │   │  JSON <=  │
         │  Wins     │   │  Wins     │
         │  (Best)   │   │  (Best)   │
         └──────┬────┘   └────┬──────┘
                │             │
         ┌──────▼─┐      ┌────▼──────┐
         │ Saves  │      │ Minifies  │
         │ TOON   │      │ JSON      │
         │Formatted│     │  -min.json│
         │-min.toon│     └────┬──────┘
         └──────┬─┘           │
                │      ┌──────▼──────┐
                │      │   Saves     │
                │      │  min JSON   │
                │      │-min.json    │
                │      └──────┬──────┘
                │             │
                └─────┬───────┘
                      ▼
           ┌──────────────────────┐
           │    Optimized File    │
           │     (optimized/)     │
           │  -min.toon or .json  │
           └──────────────────────┘
```

---

## Main Components

### 1️⃣ TokenCounter

**Location:** `src/json2toon/toon_converter.py` (lines ~30-80)

**Responsibility:** Calculate tokens using tiktoken (cl100k_base) or fallback

```python
class TokenCounter:
    _use_tiktoken = False
    _encoding = None

    # Tries to initialize tiktoken on import
    try:
        import tiktoken
        _encoding = tiktoken.get_encoding("cl100k_base")
        _use_tiktoken = True
    except Exception:
        _use_tiktoken = False
        _encoding = None

    @staticmethod
    def count_tokens(text: str) -> int:
        """Preference 1: tiktoken | Preference 2: ceil(chars/4)"""
        if TokenCounter._use_tiktoken and TokenCounter._encoding is not None:
            try:
                token_ids = TokenCounter._encoding.encode(text)
                return len(token_ids)
            except Exception:
                return math.ceil(len(text) / 4)
        return math.ceil(len(text) / 4)

    @staticmethod
    def analyze(text: str) -> dict:
        """Returns full analysis with used tokenizer"""
        return {
            'characters': len(text),
            'lines': text.count('\n') + 1,
            'words': len(text.split()),
            'tokens': TokenCounter.count_tokens(text),
            'tokenizer': 'cl100k_base' if TokenCounter._use_tiktoken else 'fallback'
        }
```

**Methods:**

1. **Preferred (when `tiktoken` is installed):**

   ```python
   import tiktoken
   encoding = tiktoken.get_encoding("cl100k_base")
   tokens = len(encoding.encode(text))
   ```

   - ✅ Exact count (compatible with GPT-4, Claude)
   - ✅ Industry standard
   - ⚠️ Requires: `pip install tiktoken`

2. **Fallback (without tiktoken):**
   ```python
   tokens = math.ceil(len(text) / 4)
   ```
   - ✅ Conservative estimate
   - ✅ Compatible with original TOON specification
   - ✅ No dependencies

---

### 2️⃣ TOONEncoder

**Location:** `src/json2toon/toon_converter.py` (lines ~50-350)

**Responsibility:** Convert JSON to TOON following all rules

#### Encoding Flow

```python
TOONEncoder.encode(value)
    │
    ├─► Type: dict
    │   └─► _encode_object()
    │       └─► For each key-value:
    │           ├─► Simple value → "key: value"
    │           └─► Complex value → "key:\n  ..."
    │
    ├─► Type: list
    │   └─► _encode_array()
    │       ├─► Primitives? → _encode_primitive_array() [inline]
    │       ├─► Tabular? → _encode_tabular_array() [max compression]
    │       └─► Mixed? → _encode_list_array() [list format]
    │
    └─► Type: str, int, bool, None
        └─► _encode_primitive() → formatted value
```

#### Main Methods

| Method                      | Input         | Output                  | Example                  |
| --------------------------- | ------------- | ----------------------- | ------------------------ |
| `encode()`                  | JSON          | TOON                    | `{"a":1}` → `a: 1`       |
| `_encode_object()`          | dict          | TOON object             | `{'id':1}` → `id: 1`     |
| `_encode_array()`           | list          | TOON array              | Detects type and formats |
| `_encode_primitive_array()` | list[int/str] | `[3]: a,b,c`            |                          |
| `_encode_tabular_array()`   | list[dict]    | `items[2]{k1,k2}:\n...` | **50-66% savings!**      |
| `_encode_list_array()`      | mixed list    | `[3]:\n- a\n- b`        |                          |
| `_quote_string()`           | string        | quoted string           | `"hello world"`          |

---

### 3️⃣ process_json_file()

**Location:** `src/json2toon/toon_converter.py` (lines ~350-410)

**Responsibility:** Orchestrate the entire conversion flow

```python
def process_json_file(input_file, output_dir=None):
    """
    1. Reads JSON
    2. Minifies JSON
    3. Counts minified JSON tokens
    4. Converts to TOON
    5. Counts TOON tokens
    6. Compares and saves the best
    """
```

**Steps:**

1. ✅ Reads JSON file
2. ✅ Minifies with `separators=(',', ':')`
3. ✅ Counts minified JSON tokens
4. ✅ Converts to TOON
5. ✅ Counts TOON tokens
6. ✅ Compares: JSON vs TOON
7. ✅ Saves: `{name}-min.toon` or `{name}-min.json`

---

## Detailed Processing Flow

### Example: `sample_data.json`

```json
{
  "name": "John",
  "items": [
    { "id": 1, "qty": 5 },
    { "id": 2, "qty": 3 }
  ]
}
```

#### Step 1: Minify JSON

```json
{
  "name": "John",
  "items": [
    { "id": 1, "qty": 5 },
    { "id": 2, "qty": 3 }
  ]
}
```

- Original: 73 characters
- Minified: 56 characters
- Tokens: 56 ÷ 4 = **14 tokens**

#### Step 2: Count Tokens

```python
TokenCounter.analyze(minified_json)
# {'characters': 56, 'tokens': 14}
```

#### Step 3: Encode to TOON

```
name: John
items[2]{id,qty}:
  1,5
  2,3
```

- Characters: 39
- Tokens: 39 ÷ 4 = **10 tokens**

#### Step 4: Compare

```
JSON:  14 tokens
TOON:  10 tokens (better!)
Savings: 4 tokens (28.6%)
```

#### Step 5: Save

```
✅ Saved in TOON format: sample_data-min.toon
```

---

## Decision: JSON vs TOON

### Selection Criteria

```python
if toon_tokens < json_tokens:
    # TOON is better
    save as: {name}-min.toon (formatted)
else:
    # JSON is better (or tie)
    save as: {name}-min.json (minified)
```

### When TOON Wins

✅ Arrays of uniform objects (tabular data)
✅ Many repeated key-values
✅ Nested structures with little depth

**Example:** Data table with 10 columns

- JSON: 1000 characters
- TOON: 400 characters (60% savings!)

### When JSON Wins

✅ Very deep structures (7+ levels)
✅ Simple heterogeneous data
✅ Few data, much depth

**Example:** Deep nested structure

- JSON: 49 characters
- TOON: 68 characters (JSON is 27% better!)

---

## Folder Structure

```
toonTools/
│
├─ src/
│  └─ json2toon/
│     ├─ toon_converter.py       ← Project Core
│     └─ cli.py                  ← CLI Entry Point
│
├─ examples/                      ← Test Data
│  ├─ simple/
│  ├─ intermediate/
│  └─ complex/
│
├─ optimized/                     ← Results
│  ├─ *-min.toon                 ← When TOON wins
│  └─ *-min.json                 ← When JSON wins
│
├─ docs/                          ← Technical Documentation
│  ├─ TOON_SPECIFICATION.md
│  └─ ARCHITECTURE.md             ← This file
│
├─ analysis/                      ← Analysis and benchmarks
│  ├─ BENCHMARK.md
│  ├─ RESULTS_SUMMARY.md
│  └─ WHEN_JSON_WINS.md
│
└─ demo/                          ← Interactive examples
   ├─ demo.py
   └─ QUICKSTART.sh
```

---

## Conversion Rules

### Objects

```json
// Input
{ "id": 1, "name": "Ada" }

// Output (TOON)
id: 1
name: Ada
```

### Nested Objects

```json
// Input
{ "user": { "id": 1, "name": "Ada" } }

// Output (TOON)
user:
  id: 1
  name: Ada
```

### Arrays of Primitives

```json
// Input
["apple", "banana", "orange"]

// Output (TOON)
[3]: apple,banana,orange
```

### Tabular Arrays (Max Savings!)

```json
// Input
[
  { "id": 1, "qty": 5 },
  { "id": 2, "qty": 3 }
]

// Output (TOON)
[2]{id,qty}:
  1,5
  2,3
```

**Savings: 50-66%** because it doesn't repeat keys!

### Mixed Arrays

```json
// Input
[1, "hello", true, null]

// Output (TOON)
[4]:
  - 1
  - hello world
  - true
  - null
```

---

## Performance

### Processing Time

| Size   | Characters | Time     |
| ------ | ---------- | -------- |
| Small  | <1KB       | <10ms    |
| Medium | 1-10KB     | 10-50ms  |
| Large  | 10-100KB   | 50-200ms |

### Token Savings (Average)

| Data Type | Savings | Cases            |
| --------- | ------- | ---------------- |
| Tabular   | 50-66%  | Uniform arrays   |
| Simple    | 30-40%  | Objects + arrays |
| Complex   | 20-30%  | Mixed structures |

---

## Extension Points

### Delimiter Customization

```python
encoder = TOONEncoder(delimiter='|')  # Instead of ','
```

### Disable Key Folding

```python
encoder = TOONEncoder(key_folding='off')
```

### Configure Indentation

```python
encoder = TOONEncoder(indent=4)  # Instead of 2
```

---

## Tests

### Quick Test

```bash
python src/json2toon/toon_converter.py examples/simple/simple_numbers.json
```

### Full Test

```bash
python src/json2toon/toon_converter.py examples/complex/employees.json
python src/json2toon/toon_converter.py examples/complex/deeply_nested.json
```

### Interactive Demo

```bash
python demo/demo.py
```

---

## Future Improvements

- [ ] TOON → JSON decoder (round-trip)
- [ ] CLI with arguments (--output, --delimiter)
- [ ] Batch processing of multiple files
- [ ] Streaming support for very large files
- [ ] API Integration

---

**Version:** 1.1  
**Date:** November 2025  
**Status:** ✅ Complete
