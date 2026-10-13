"""
Text-to-Music Prompt Structurer - Main Engine
"""

import re
from collections.abc import Sequence
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
from text_to_music_prompt_structurer.exclusions import extract_negative_constraints
from text_to_music_prompt_structurer.loaders import VocabLoader
from text_to_music_prompt_structurer.models import MusicPrompt
from text_to_music_prompt_structurer.registry import DetectorRegistry
from text_to_music_prompt_structurer.suno import SunoFields, SunoSection, build_suno_prompt


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

    def process_suno(
        self,
        text: str,
        *,
        title: str = "",
        lyrics: str = "",
        sections: Sequence[SunoSection | str] | None = None,
        exclude: str | Sequence[str] = "",
        instrumental: bool | None = None,
        style_notes: str = "",
        preserve_description: bool = True,
        auto_exclude: bool = True,
    ) -> SunoFields:
        """Build Suno's actual Custom/Advanced input fields from a description.

        Preserving the source description by default retains production and
        arrangement nuances that keyword detectors do not understand yet.
        Disable it to generate a shorter vocabulary-only style prompt.
        """
        negatives = extract_negative_constraints(text) if auto_exclude else None
        prompt = self.process(negatives.cleaned_description if negatives else text)
        if instrumental is None:
            instrumental = bool(
                re.search(
                    r"\b(?:instrumental(?!\s+(?:break|section|solo))"
                    r"|no vocals|without vocals|no singing|sin voz|sin voces|sin letra)\b",
                    text,
                    re.IGNORECASE,
                )
            )
        notes = style_notes.strip()
        if preserve_description:
            # Keep nuanced, unknown creative details, but do NOT append
            # negated instruments back into the positive Style of Music field.
            creative = negatives.cleaned_description if negatives else text
            creative = re.sub(r"\\s+([,;])", r"\\1", creative)
            creative = re.sub(r"[,;]\\s*[,;]+", ",", creative).strip().strip(",;").strip()
            if creative:
                original = "Creative direction: " + creative
                notes = f"{notes}; {original}" if notes else original
        explicit = (
            [item.strip() for item in exclude.split(",") if item.strip()]
            if isinstance(exclude, str)
            else list(exclude)
        )
        auto = list(negatives.excludes) if negatives else []
        combined_exclude: list[str] = []
        seen_exclusions: set[str] = set()
        for value in [*explicit, *auto]:
            item = value.strip()
            if item and item.casefold() not in seen_exclusions:
                combined_exclude.append(item)
                seen_exclusions.add(item.casefold())
        return build_suno_prompt(
            prompt,
            title=title,
            lyrics=lyrics,
            sections=sections,
            exclude=combined_exclude,
            instrumental=instrumental,
            style_notes=notes,
        )


SunoPromptEngine = MusicPromptEngine
"""Backward-compatible alias for :class:`MusicPromptEngine`."""
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
