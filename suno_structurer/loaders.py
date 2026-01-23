"""
Suno Prompt Structurer - Configuration Loader
"""

import json
from pathlib import Path


class VocabLoader:
    """Loads vocabulary configurations from JSON files."""
    
    def __init__(self, vocab_dir: Path):
        self.vocab_dir = vocab_dir

    def load(self, name: str):
        """Load a vocabulary file by name."""
        with open(self.vocab_dir / f"{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
