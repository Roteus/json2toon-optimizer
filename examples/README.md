# Examples

This directory contains example JSON files demonstrating different data structures and their conversion to TOON format.

## 📁 Directory Structure

### Simple Examples (`simple/`)

Basic data structures - good for learning the basics.

- `simple_numbers.json` - Simple key-value pairs with numbers

### Intermediate Examples (`intermediate/`)

Medium complexity data with nested objects and arrays.

- `sample_data.json` - Mixed data with nested objects and arrays
- `heterogeneous.json` - Mixed data types

### Complex Examples (`complex/`)

Advanced structures demonstrating maximum TOON efficiency.

- `employees.json` - Tabular data (arrays of uniform objects) - **Best TOON savings!**
- `products.json` - Product catalog with uniform structure
- `deeply_nested.json` - Deep nesting - **JSON wins this case!**
- `many_strings.json` - String-heavy data
- `long_array.json` - Long arrays of primitives

### Comparison Examples (`comparison/`)

Side-by-side examples showing when each format excels.

## 🎯 Try Them Out

```bash
# Simple example
toon-convert examples/simple/simple_numbers.json

# Best case for TOON (tabular data)
toon-convert examples/complex/employees.json

# Case where JSON is better
toon-convert examples/complex/deeply_nested.json
```

## 📊 Expected Results

| File                | JSON Tokens | TOON Tokens | Winner | Savings |
| ------------------- | ----------- | ----------- | ------ | ------- |
| simple_numbers.json | 7           | 7           | Tie    | 0%      |
| sample_data.json    | 107         | 86          | TOON   | 19.6%   |
| heterogeneous.json  | 76          | 55          | TOON   | 27.6%   |
| employees.json      | 214         | 92          | TOON   | 57.0%   |
| products.json       | 351         | 197         | TOON   | 43.9%   |
| deeply_nested.json  | 13          | 17          | JSON   | -30.8%  |
| many_strings.json   | 106         | 34          | TOON   | 67.9%   |
| long_array.json     | 73          | 32          | TOON   | 56.2%   |

## 💡 Key Insights

**TOON excels with:**

- Arrays of uniform objects (tabular data)
- Repetitive structures
- Data with consistent schemas

**JSON excels with:**

- Deeply nested structures (>5 levels)
- Very simple data
- Single-value objects

## 🔨 Creating Your Own Examples

1. Create a JSON file in the appropriate directory
2. Run the converter: `toon-convert your-file.json`
3. Compare the results!

## 📚 Learn More

- See [TOON_SPECIFICATION.md](../docs/TOON_SPECIFICATION.md) for format rules
- See [GUIDE.md](../docs/GUIDE.md) for usage patterns
- Run `python demo/demo.py` for interactive examples
