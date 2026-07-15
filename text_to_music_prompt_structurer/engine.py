"""
Suno Prompt Structurer - Main Engine
"""

from pathlib import Path
from text_to_music_prompt_structurer.models import SunoPrompt
from text_to_music_prompt_structurer.loaders import VocabLoader
from text_to_music_prompt_structurer.registry import DetectorRegistry
from text_to_music_prompt_structurer.detectors import (
    GenreDetector,
    KeywordListDetector,
    SingleKeywordDetector,
    LanguageDetector,
    BPMDetector,
    ThemeDetector,
    KeyDetector,
    EnergyDetector,
    StructureDetector,
    RhythmDetector,
    EraDetector,
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
        self.registry.register(SingleKeywordDetector(loader.load("tempo")["descriptors"], "tempo"))
        self.registry.register(EnergyDetector(loader.load("energy")))
        self.registry.register(StructureDetector(loader.load("structure")))
        self.registry.register(RhythmDetector(loader.load("rhythm")))
        self.registry.register(EraDetector(loader.load("era")))
        self.registry.register(ThemeDetector())

    def process(self, text: str) -> SunoPrompt:
        """Process input text and return a structured prompt."""
        text = text.lower()
        prompt = SunoPrompt()
        self.registry.run(text, prompt)
        return prompt
