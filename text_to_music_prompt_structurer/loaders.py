"""
Suno Prompt Structurer - Configuration Loader
"""

import json
import re
from pathlib import Path
from typing import Any


class VocabLoader:
    """Loads vocabulary configurations from JSON / JSONC files."""

    def __init__(self, vocab_dir: Path):
        self.vocab_dir = vocab_dir

    def load(self, name: str) -> Any:
        """
        Load a vocabulary file by name.
        Supports .json and .jsonc (JSON with comments).
        """
        path_json = self.vocab_dir / f"{name}.json"
        path_jsonc = self.vocab_dir / f"{name}.jsonc"

        if path_json.exists():
            return self._load_json(path_json)

        if path_jsonc.exists():
            return self._load_jsonc(path_jsonc)

        raise FileNotFoundError(
            f"Vocabulary file '{name}.json' or '{name}.jsonc' not found in {self.vocab_dir}"
        )

    def _load_json(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _load_jsonc(self, path: Path) -> Any:
        text = path.read_text(encoding="utf-8")

        # Remove // line comments
        text = re.sub(r"(?m)^\s*//.*$", "", text)

        # Remove /* block comments */
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)

        # Remove trailing commas (common in JSONC)
        text = re.sub(r",\s*([}\]])", r"\1", text)

        return json.loads(text)
