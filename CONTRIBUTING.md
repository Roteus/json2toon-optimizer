# Contributing to json2toon-optimizer

Thank you for your interest in contributing to json2toon-optimizer! This document provides guidelines and instructions for contributing.

## ⚠️ Important: Branch Protection

**Direct commits to the `master` branch are not allowed.** All changes must go through Pull Requests and be approved by @Roteus before merging.

See [.github/BRANCH_PROTECTION.md](.github/BRANCH_PROTECTION.md) for complete details on branch protection rules.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/Roteus/json2toon-optimizer`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add: your feature description"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request to the `master` branch
9. **Wait for approval from @Roteus** before the PR can be merged

## 📋 Pull Request Guidelines

### ✅ Requirements

All Pull Requests **must**:
- Be reviewed and approved by **@Roteus** (code owner)
- Target the `master` branch (or other feature branches)
- Pass all required checks (if configured)

### Before Submitting

- [ ] Code follows the project's coding style
- [ ] All tests pass
- [ ] Documentation is updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] PR is ready for review by @Roteus

### PR Description Should Include

- **What**: Brief description of changes
- **Why**: Reason for the changes
- **How**: Explanation of implementation (if complex)
- **Testing**: How you tested the changes

### Review Process

1. Submit your Pull Request
2. @Roteus will review your changes
3. Address any feedback or requested changes
4. Once approved, your PR will be merged

## 🧪 Testing

```bash
# Run demo to test basic functionality
python demo/demo.py

# Test with example files
json2toon examples/simple/simple_numbers.json
json2toon examples/intermediate/sample_data.json
json2toon examples/complex/employees.json
```

## 📝 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Write docstrings for functions and classes

## 🐛 Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: Python version, OS, etc.
- **Sample Data**: Minimal JSON that reproduces the issue (if applicable)

## 💡 Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists or is planned
- Describe the feature clearly
- Explain the use case
- Provide examples if possible

## 📚 Documentation

Good documentation helps everyone. Contributions to docs are highly valued:

- Fix typos or unclear explanations
- Add examples
- Improve existing documentation
- Translate documentation (if multilingual support is added)

## 🎯 Areas for Contribution

### Easy

- Fix typos in documentation
- Add more example files
- Improve error messages
- Add unit tests

### Medium

- Optimize token counting
- Add new output formats
- Improve CLI interface
- Add configuration file support

### Advanced

- TOON → JSON decoder
- Performance optimizations
- Support for streaming large files
- Add format validation

## 🤝 Code Review Process

1. Maintainers will review your PR
2. Feedback may be provided for improvements
3. Once approved, your PR will be merged
4. Your contribution will be credited

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

Feel free to open an issue for questions or discussions.

---

Thank you for contributing to json2toon-optimizer! 🎉
