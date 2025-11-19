# 📖 Project Navigation Guide

Welcome! This file helps you navigate the json2toon-optimizer project.

---

## 🎯 Start Here

### I'm New to the Project

1. **Read:** [README.md](../README.md) (5 min)
2. **Run:** `json2toon examples/simple/simple_numbers.json`
3. **Explore:** `optimized/` folder to see results
4. **Learn:** [docs/TOON_SPECIFICATION.md](TOON_SPECIFICATION.md) (reference)

### I Want to Use the Converter

```bash
# Go to folder
cd json2toon-optimizer

# Process your JSON
json2toon your_file.json

# View result
cat optimized/your_file-min.toon  # or .json
```

**[More details →](../README.md#-quick-start)**

### I Want to Understand How It Works

1. **[Architecture](ARCHITECTURE.md)** - Diagrams and flow
2. **[TOON Specification](TOON_SPECIFICATION.md)** - Conversion rules
3. **[How Token Counting Works](TOKEN_COUNTING.md)** - Math

### I Want to See Results and Benchmarks

1. **[Full Benchmark](../analysis/BENCHMARK.md)** - Performance
2. **[Cases Where JSON Wins](../analysis/WHEN_JSON_WINS.md)** - Exceptions
3. **[Results Summary](../analysis/RESULTS_SUMMARY.md)** - Statistics

### I Have a Question / Problem

👉 **[Troubleshooting](TROUBLESHOOTING.md)** - FAQ and solutions

---

## 📁 Folder Structure

### `src/` - Main Code

```
src/
└── toon_converter.py
    ├── TokenCounter          (calculates tokens)
    ├── TOONEncoder           (converts JSON → TOON)
    └── process_json_file()   (orchestrates everything)
```

**Start here to understand the code!**

### `examples/` - Test Files

```
examples/
├── simple/
│   └── simple_numbers.json      (simple data)
│
├── intermediate/
│   ├── sample_data.json         (normal data)
│   └── heterogeneous.json       (mixed data)
│
└── complex/
    ├── employees.json           (tabular arrays)
    ├── products.json            (complex structure)
    ├── deeply_nested.json       (very deep - JSON wins!)
    ├── many_strings.json        (many strings)
    └── long_array.json          (large array)
```

### `optimized/` - Results

```
optimized/
├── simple_numbers-min.toon
├── sample_data-min.toon
├── heterogeneous-min.toon
├── employees-min.toon
├── products-min.toon
├── many_strings-min.toon
├── long_array-min.toon
└── deeply_nested-min.json       ← Special example (JSON wins!)
```

### `docs/` - Technical Documentation

```
docs/
├── TOON_SPECIFICATION.md        (complete reference)
├── ARCHITECTURE.md              (internal design)
├── TOKEN_COUNTING.md            (how to calculate tokens)
├── TROUBLESHOOTING.md           (FAQ)
├── INDEX.txt                    (topic index)
└── ... (this file)
```

### `analysis/` - Detailed Analysis

```
analysis/
├── BENCHMARK.md                 (performance comparison)
├── RESULTS_SUMMARY.md           (summary of all tests)
├── TOKEN_COUNTING_FIX.md        (technical details of the fix)
├── WHEN_JSON_WINS.md            (special cases)
├── JSON_MINIFICATION.md         (how JSON is minified)
└── UPDATE_JSON_MINIFICATION.md  (optimization history)
```

### `demo/` - Interactive Examples

```
demo/
├── demo.py                      (8 examples with output)
└── QUICKSTART.sh                (start script)
```

---

## 🚀 Start by Task

### Task: Convert My JSON

```bash
# 1. Put your file in examples/
cp your_file.json examples/complex/

# 2. Run the converter
json2toon examples/complex/your_file.json

# 3. View the result
cat optimized/your_file-min.toon   # or -min.json
```

### Task: Understand TOON Rules

1. Read: [TOON_SPECIFICATION.md](TOON_SPECIFICATION.md)
2. See examples in: `examples/`
3. Compare inputs/outputs in: `optimized/`

### Task: Analyze Performance

1. Open: [BENCHMARK.md](../analysis/BENCHMARK.md)
2. Tables show:
   - Input/output characters
   - Input/output tokens
   - Savings percentage

### Task: Run Demo

```bash
# Interactive demo with 8 examples
python demo/demo.py

# Or run a specific example
json2toon examples/simple/simple_numbers.json
```

### Task: Understand the Code

1. **Classes:** [ARCHITECTURE.md](ARCHITECTURE.md) - Overview
2. **Flow:** Diagram in [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Code:** `src/toon_converter.py` - Real implementation

---

## 📊 Quick Reference Matrix

| I want...             | File                        | What to Do                      |
| --------------------- | --------------------------- | ------------------------------- |
| **Use the converter** | README.md                   | Section "Quick Start"           |
| **Learn TOON**        | TOON_SPECIFICATION.md       | Read and compare examples       |
| **View results**      | analysis/BENCHMARK.md       | See comparison tables           |
| **Understand code**   | docs/ARCHITECTURE.md        | Diagrams and pseudocódigo       |
| **Run examples**      | demo/demo.py                | Run `python demo/demo.py`       |
| **My problem**        | TROUBLESHOOTING.md          | Search by keyword               |
| **Convert my file**   | README.md                   | Section "How to Use the Script" |
| **View savings**      | analysis/RESULTS_SUMMARY.md | Statistics tables               |

---

## 🔗 Quick Links

### Technical Documentation

- 📘 [Complete TOON Specification](TOON_SPECIFICATION.md)
- 🏗️ [Project Architecture](ARCHITECTURE.md)
- 🔢 [How to Calculate Tokens](TOKEN_COUNTING.md)

### Results and Analysis

- 📊 [Performance Benchmark](../analysis/BENCHMARK.md)
- 📈 [When JSON is Better](../analysis/WHEN_JSON_WINS.md)
- 📋 [Results Summary](../analysis/RESULTS_SUMMARY.md)

### Examples

- 🔵 [Simple Examples](../examples/simple/)
- 🟡 [Intermediate Examples](../examples/intermediate/)
- 🔴 [Complex Examples](../examples/complex/)
- 🟢 [Optimized Results](../optimized/)

---

## ❓ Frequently Asked Questions

**Q: Where do I start?**
A: Read [README.md](../README.md) and run `json2toon examples/simple/simple_numbers.json`

**Q: How does token counting work?**
A: Tokens = ⌈characters / 4⌉. See [TOKEN_COUNTING.md](TOKEN_COUNTING.md)

**Q: When is JSON better than TOON?**
A: With very deep structures. See example in `examples/complex/deeply_nested.json`

**Q: How do I use my own file?**
A: `json2toon your_file.json`

**Q: Do I need to install anything?**
A: No! Just Python 3.7+

---

## 📈 Recommended Learning Flow

```
1. README.md (5 min)
   ↓
2. Run an example (2 min)
   ↓
3. View result in optimized/ (1 min)
   ↓
4. TOON_SPECIFICATION.md (10 min)
   ↓
5. ARCHITECTURE.md (15 min)
   ↓
6. Analyze BENCHMARK.md (10 min)
   ↓
7. Code in src/toon_converter.py (30+ min)
```

Total: ~1 hour for complete understanding

---

## 🎓 Reference Material

### Beginners

- [README.md](../README.md)
- [Quick Start](#-start-by-task)

### Users

- [How to Use the Script](../README.md#-how-to-use-the-script)
- [Examples](../examples/)

### Developers

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [TOON_SPECIFICATION.md](TOON_SPECIFICATION.md)
- [src/toon_converter.py](../src/toon_converter.py)

### Analysts

- [BENCHMARK.md](../analysis/BENCHMARK.md)
- [RESULTS_SUMMARY.md](../analysis/RESULTS_SUMMARY.md)
- [WHEN_JSON_WINS.md](../analysis/WHEN_JSON_WINS.md)

---

## 📝 Notes

- All paths in this file are relative to the `docs/` folder
- To run scripts, go to the project root (`json2toon-optimizer/`)
- Always run `python -V` to confirm you have Python 3.7+

---

**Last updated:** November 2025  
**Version:** 1.1  
**Status:** ✅ Updated
