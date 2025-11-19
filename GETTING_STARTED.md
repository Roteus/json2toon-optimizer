# 🚀 Getting Started with json2toon-optimizer

Welcome! This guide will get you up and running in **5 minutes**.

---

## ⚡ 5 Minute Setup

### Prerequisites

✅ Python 3.7 or higher

```bash
python --version  # Should show Python 3.7+
```

### Installation

```bash
# Option 1: Install from PyPI (when published)
pip install json2toon-optimizer

# Option 2: Install from source
git clone https://github.com/Roteus/json2toon-optimizer
cd json2toon-optimizer
pip install -e .
```

### Optional Dependencies

For exact token counting (recommended):

```bash
pip install tiktoken
```

Without `tiktoken` the converter uses an approximate estimate (⌈chars/4⌉).

---

## 🎯 First Example (2 minutes)

### Run

```bash
# Using installed CLI
json2toon examples/simple/simple_numbers.json

# Or using Python module
python -m src.toon_converter examples/simple/simple_numbers.json
```

### Result

```
📖 Reading file: simple_numbers.json
   JSON (minified): 28 characters → 7 tokens

Converting to TOON...
   TOON: 26 characters → 7 tokens

Comparison:
   JSON tokens:  7
   TOON tokens:  7
   Savings:      0 tokens (0.0%)

✅ Saved in minified JSON format: simple_numbers-min.json
```

### View Result

```bash
# View optimized file
cat optimized/simple_numbers-min.json
```

---

## 📖 Second Example (2 minutes)

### Run with Larger Data

```bash
json2toon examples/intermediate/sample_data.json
```

### Result

```
📖 Reading file: sample_data.json
   JSON (minified): 428 characters → 107 tokens

Converting to TOON...
   TOON: 342 characters → 86 tokens

Comparison:
   JSON tokens:  107
   TOON tokens:  86
   Savings:      21 tokens (19.6%)

✅ Saved in TOON format: sample_data-min.toon
```

**See? TOON saves 21 tokens (19.6%)!**

---

## 📊 Third Example (1 minute)

### The Special Case - JSON Wins!

```bash
json2toon examples/complex/deeply_nested.json
```

### Result

```
📖 Reading file: deeply_nested.json
   JSON (minified): 49 characters → 13 tokens

Converting to TOON...
   TOON: 68 characters → 17 tokens

Comparison:
   JSON tokens:  13
   TOON tokens:  17
   Savings:      -4 tokens (-30.8%)

✅ Saved in minified JSON format: deeply_nested-min.json
```

**Interesting! In this case JSON is better than TOON!**

---

## 🎓 Next Steps

### Want to Learn More?

1. **See all examples:**

   ```bash
   python demo/demo.py
   ```

   Shows 8 examples with detailed output

2. **Read the documentation:**

   - [README.md](README.md) - Main guide
   - [docs/GUIDE.md](docs/GUIDE.md) - User guide
   - [docs/TOON_SPECIFICATION.md](docs/TOON_SPECIFICATION.md) - Technical reference

3. **Explore the examples:**
   - `examples/simple/` - Basic examples
   - `examples/intermediate/` - Medium complexity
   - `examples/complex/` - Advanced examples

### Want to Use with Your Data?

```bash
# 1. Run the converter on your file
json2toon your_file.json

# 2. Specify output directory (optional)
json2toon your_file.json -o ./output

# 3. View the result
cat your_file-min.toon   # or .json
```

---

## 📁 Where Everything Is

| What              | Where       | How to Access                                            |
| ----------------- | ----------- | -------------------------------------------------------- |
| **Main Script**   | `src/`      | `json2toon` or `python -m src.toon_converter`            |
| **Test Data**     | `examples/` | See in `examples/simple/`, `/intermediate/`, `/complex/` |
| **Documentation** | `docs/`     | `docs/GUIDE.md` for navigation                           |
| **Demo**          | `demo/`     | `python demo/demo.py`                                    |

---

## 🔍 What to Do Now

### If You Want to Understand Quickly

```
1. Read: README.md (5 min)
2. Run: 3 examples above (5 min)
3. See: docs/TOON_SPECIFICATION.md (10 min)
```

Total: 20 minutes ⏱️

### If You Want to Explore Everything

```
1. Read: README.md + PROJECT_STRUCTURE.md
2. Run: python demo/demo.py
3. Explore: analysis/BENCHMARK.md
4. Learn: docs/ARCHITECTURE.md
5. Study: src/toon_converter.py
```

Total: 1-2 hours 🎓

### If You Just Want to Use

```
1. json2toon your_file.json
2. View result: your_file-min.toon (or .json)
3. Ready!
```

Total: 2 minutes ⚡

---

## ❓ Common Questions

**Q: Do I need to install anything?**
A: No! Python 3.7+ is all you need.

**Q: How does it work?**
A: Calculates minified JSON vs TOON tokens and saves the most efficient.

**Q: Which format is better?**
A: Depends on the data! TOON wins in 90% of cases (tabular arrays). JSON wins in deep structures.

**Q: Can I customize?**
A: Yes! Edit `src/toon_converter.py` to adjust delimiters, indentation, etc.

**Q: Works with which Python versions?**
A: Python 3.7+ (no need for Python 2)

---

## 🎯 Start Checklist

- [ ] Confirmed I have Python 3.7+ (`python --version`)
- [ ] Installed the package (`pip install json2toon-optimizer` or from source)
- [ ] Executed: `json2toon examples/simple/simple_numbers.json`
- [ ] Saw the result file created
- [ ] Read this file to the end
- [ ] Executed `python demo/demo.py`
- [ ] Read `README.md`

---

## 🔗 Quick References

**Documentation**

- 📄 [README.md](README.md) - Main guide
- 📚 [docs/GUIDE.md](docs/GUIDE.md) - User guide
- 🏗️ [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- 🔢 [docs/TOKEN_COUNTING.md](docs/TOKEN_COUNTING.md) - Token details

**Examples**

- 🟢 [Simple](examples/simple/) → Basic examples
- 🟡 [Intermediate](examples/intermediate/) → Medium complexity
- 🔴 [Complex](examples/complex/) → Advanced cases
- ⭐ [Comparison](examples/comparison/) → Format comparisons

---

## 💡 Tip

Each file in the project has a purpose:

- **Run code?** → Use `json2toon` CLI
- **Understand rules?** → Read `docs/TOON_SPECIFICATION.md`
- **See examples?** → Explore `examples/`
- **Learn design?** → Study `docs/ARCHITECTURE.md`
- **Need help?** → Consult `docs/GUIDE.md`

---

## 🎉 Ready!

You now know:

- ✅ How to run the converter
- ✅ Where to find examples
- ✅ Where to view results
- ✅ Where to learn more

**Next step?** Choose a path above and have fun! 🚀

---

**Version:** 1.1  
**Date:** November 2025  
**Status:** ✅ Updated
