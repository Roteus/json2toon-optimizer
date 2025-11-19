#!/usr/bin/env python
"""
Setup script for json2toon-optimizer (compatibility with old setuptools)

Recommended usage: pip install -e . (or -e ".[full]" for tiktoken)

Alternatives:
  pip install .                    # Install
  pip install -e .                # Install in development mode
  pip install -e ".[full]"        # With tiktoken for accurate token counting
  pip install -e ".[dev]"         # With development dependencies
"""

from setuptools import setup, find_packages

setup(
    name="json2toon-optimizer",
    version="2.0.0",
    description="JSON ↔ TOON optimizer and converter with token estimation",
    author="json2toon-optimizer Contributors",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "full": ["tiktoken>=0.7.0"],
        "stream": ["ijson>=3.2.0"],
        "all": ["tiktoken>=0.7.0", "ijson>=3.2.0"],
        "dev": [
            "tiktoken>=0.7.0",
            "ijson>=3.2.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "json2toon=json2toon.cli:main",
        ],
    },
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Roteus/json2toon-optimizer",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
