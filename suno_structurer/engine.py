"""
Suno Prompt Structurer - Main Engine
"""

from pathlib import Path
from suno_structurer.models import SunoPrompt
from suno_structurer.loaders import VocabLoader
from suno_structurer.registry import DetectorRegistry
from suno_structurer.detectors import (
    GenreDetector,
    KeywordListDetector,
    LanguageDetector,
    BPMDetector,
    ThemeDetector,
    KeyDetector
)


class SunoPromptEngine:
    """Main engine for processing unstructured text into Suno prompts."""
    
    def __init__(self, vocab_dir="vocab"):
        loader = VocabLoader(Path(vocab_dir))
        self.registry = DetectorRegistry()

        # Register all detectors
        self.registry.register(GenreDetector(loader.load("genres")))
        self.registry.register(KeywordListDetector(loader.load("moods"), "mood"))
        self.registry.register(KeywordListDetector(loader.load("instruments"), "instruments"))
        self.registry.register(KeywordListDetector(loader.load("production"), "production"))
        self.registry.register(KeywordListDetector(loader.load("vocals"), "vocal_style"))
        self.registry.register(LanguageDetector(loader.load("languages")))
        self.registry.register(KeyDetector(loader.load("keys")))
        self.registry.register(BPMDetector())
        self.registry.register(ThemeDetector())

    def process(self, text: str) -> SunoPrompt:
        """Process input text and return a structured prompt."""
        text = text.lower()
        prompt = SunoPrompt()
        self.registry.run(text, prompt)
        return prompt
