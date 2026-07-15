"""
Text-to-Music Prompt Structurer - Configuration Loader
"""

import json
import re
from typing import Any, Protocol


class VocabPath(Protocol):
    """Path behavior required by the vocabulary loader."""

    def __truediv__(self, child: str) -> "VocabPath": ...
    def exists(self) -> bool: ...
    def open(self, mode: str = "r", encoding: str | None = None): ...
    def read_text(self, encoding: str | None = None) -> str: ...


class VocabLoader:
    """Loads vocabulary configurations from JSON / JSONC files."""

    def __init__(self, vocab_dir: VocabPath):
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

    def _load_json(self, path: VocabPath) -> Any:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _load_jsonc(self, path: VocabPath) -> Any:
        text = path.read_text(encoding="utf-8")

        # Remove // line comments
        text = re.sub(r"(?m)^\s*//.*$", "", text)

        # Remove /* block comments */
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)

        # Remove trailing commas (common in JSONC)
        text = re.sub(r",\s*([}\]])", r"\1", text)

        return json.loads(text)
