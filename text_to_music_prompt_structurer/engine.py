"""
Text-to-Music Prompt Structurer - Main Engine
"""

from importlib import resources
from pathlib import Path

from text_to_music_prompt_structurer.detectors import (
    BPMDetector,
    EnergyDetector,
    EraDetector,
    GenreDetector,
    KeyDetector,
    KeywordListDetector,
    LanguageDetector,
    RhythmDetector,
    SingleKeywordDetector,
    StructureDetector,
    ThemeDetector,
    VocalAttributeDetector,
)
from text_to_music_prompt_structurer.loaders import VocabLoader
from text_to_music_prompt_structurer.models import MusicPrompt
from text_to_music_prompt_structurer.registry import DetectorRegistry


class MusicPromptEngine:
    """Process unstructured text into structured musical prompts."""

    def __init__(self, vocab_dir: str | Path | None = None):
        vocab_root = (
            resources.files("text_to_music_prompt_structurer").joinpath("vocab")
            if vocab_dir is None
            else Path(vocab_dir)
        )
        loader = VocabLoader(vocab_root)
        self.registry = DetectorRegistry()

        # Register all detectors
        self.registry.register(GenreDetector(loader.load("genres")))
        self.registry.register(KeywordListDetector(loader.load("moods"), "mood"))
        self.registry.register(KeywordListDetector(loader.load("instruments"), "instruments"))
        self.registry.register(KeywordListDetector(loader.load("production"), "production"))
        self.registry.register(VocalAttributeDetector(loader.load("voice_types"), "voice_type"))
        self.registry.register(VocalAttributeDetector(loader.load("vocal_tones"), "vocal_tone"))
        self.registry.register(VocalAttributeDetector(loader.load("vocals"), "vocal_style"))
        self.registry.register(LanguageDetector(loader.load("languages")))
        self.registry.register(KeyDetector(loader.load("keys")))
        self.registry.register(BPMDetector())
        self.registry.register(SingleKeywordDetector(loader.load("tempo")["descriptors"], "tempo"))
        self.registry.register(EnergyDetector(loader.load("energy")))
        self.registry.register(StructureDetector(loader.load("structure")))
        self.registry.register(RhythmDetector(loader.load("rhythm")))
        self.registry.register(EraDetector(loader.load("era")))
        self.registry.register(ThemeDetector())

    def process(self, text: str) -> MusicPrompt:
        """Process input text and return a structured prompt."""
        text = text.lower()
        prompt = MusicPrompt()
        self.registry.run(text, prompt)
        return prompt


SunoPromptEngine = MusicPromptEngine
"""Backward-compatible alias for :class:`MusicPromptEngine`."""
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
