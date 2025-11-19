# 📦 json2toon-optimizer Installation

## Installation Options

### 1️⃣ Quick Installation (Recommended with tiktoken)

```powershell
# Clone or copy
git clone <repo>
cd json2toon-optimizer

# Install with tiktoken (accurate token counting)
pip install -e ".[full]"
```

**What is installed:**

- `tiktoken>=0.7.0` — cl100k_base tokenizer (recommended)
- CLI Script: `json2toon`

### 2️⃣ Minimal Installation (No dependencies)

```powershell
# Clone or copy
git clone <repo>
cd json2toon-optimizer

# Install only the script (without tiktoken)
pip install -e .
```

**What is installed:**

- CLI Script: `json2toon`
- No external dependencies (uses fallback ⌈chars/4⌉)

### 3️⃣ Development Installation

```powershell
# Install with all dependencies (dev, test, lint)
pip install -e ".[dev]"
```

**Includes:**

- `tiktoken>=0.7.0` — tokenizer
- `pytest`, `pytest-cov` — tests
- `black`, `flake8` — linting
- `mypy` — type checking

---

## Via PyPI (When Published)

```powershell
# Install stable version from PyPI
pip install json2toon-optimizer

# Or with tiktoken
pip install json2toon-optimizer[full]
```

---

## Verify Installation

```powershell
# Check if json2toon is available
json2toon --version

# Or use via Python
python -c "from src.toon_converter import TokenCounter; print('✅ Installed!')"
```

---

## Post-Installation

### Use the CLI

```powershell
# Process JSON file
json2toon your_file.json

# Specify output directory
json2toon your_file.json --output ./results
```

### Use as Library

```python
from toon_converter import TokenCounter, TOONEncoder, process_json_file

# Count tokens
tokens = TokenCounter.count_tokens("your text here")
print(f"Tokens: {tokens}")

# Process file
result = process_json_file("data.json")
print(f"Chosen format: {result['chosen_format']}")
```

---

## Uninstallation

```powershell
pip uninstall json2toon-optimizer
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'toon_converter'"

Make sure you installed correctly:

```powershell
pip install -e .
```

### "tiktoken not found"

If you want to use accurate token counting, install tiktoken:

```powershell
pip install -e ".[full]"
# or
pip install tiktoken
```

### "Command 'json2toon' not found"

The CLI might be in the virtualenv PATH. Try:

```powershell
python -m toon_converter.src.toon_converter your_file.json
```

---

## Installation Structure

```
site-packages/
└── toon_converter/
    ├── __init__.py
    ├── src/
    │   └── toon_converter.py      # Main script
    ├── demo/
    │   └── demo.py                # Interactive examples
    ├── docs/
    │   └── ...                    # Documentation
    ├── examples/
    │   └── ...                    # Example data
    └── analysis/
        └── ...                    # Analysis
```

---

## Next Steps

1. Read [README.md](../README.md) for overview
2. Run `json2toon examples/complex/employees.json` to test
3. Explore examples in `examples/` to learn
4. See documentation in `docs/` for technical details

---

**Version:** 2.0.0  
**Date:** November 2025  
**Status:** ✅ Complete Documentation
