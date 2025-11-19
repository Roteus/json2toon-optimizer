"""json2toon-optimizer: JSON ↔ TOON converter with token optimization"""

from .toon_converter import (
    TokenCounter,
    TOONEncoder,
    CompactTOONEncoder,
    process_json_file,
)
from .batch_processor import process_batch
from .stream_processor import process_stream

__version__ = "2.0.0"

__all__ = [
    "TokenCounter",
    "TOONEncoder",
    "CompactTOONEncoder",
    "process_json_file",
    "process_batch",
    "process_stream",
]
