"""
Text-to-Music Prompt Structurer - Detection Strategies
"""

import re

from text_to_music_prompt_structurer.models import MusicPrompt


class Detector:
    """Base class for all detectors."""

    def detect(self, text: str, prompt: MusicPrompt):
        raise NotImplementedError


class GenreDetector(Detector):
    """Detects musical genres from text."""

    def __init__(self, genres):
        # Sort by key length descending so specific subgenres are matched before
        # their parent genre keywords (e.g. "bebop" before "jazz").
        self.genres = dict(sorted(genres.items(), key=lambda x: len(x[0]), reverse=True))

    def detect(self, text, prompt):
        for key, val in self.genres.items():
            if key in text:
                prompt.genre = val["genre"]
                prompt.subgenre = val["subgenre"]
                return


class KeywordListDetector(Detector):
    """Generic detector for keyword-based list attributes."""

    def __init__(self, source, target_attr):
        self.source = source
        self.target_attr = target_attr

    def detect(self, text, prompt):
        hits = []
        for key, val in self.source.items():
            if re.search(rf"\b{re.escape(key)}\b", text):
                hits.append(val)
        setattr(prompt, self.target_attr, list(dict.fromkeys(hits)))


class SingleKeywordDetector(Detector):
    """Detector for single-value keyword attributes (sets the first match)."""

    def __init__(self, source, target_attr):
        self.source = source
        self.target_attr = target_attr

    def detect(self, text, prompt):
        for key, val in self.source.items():
            if re.search(rf"\b{re.escape(key)}\b", text):
                setattr(prompt, self.target_attr, val)
                return


class LanguageDetector(Detector):
    """Detects language from text."""

    def __init__(self, languages):
        self.languages = languages

    def detect(self, text, prompt):
        for key, val in self.languages.items():
            if key in text:
                prompt.language = val
                return


class BPMDetector(Detector):
    """Detects BPM (beats per minute) from text."""

    def detect(self, text, prompt):
        m = re.search(r"(\d{2,3})\s*bpm", text)
        if m:
            prompt.bpm = int(m.group(1))


class ThemeDetector(Detector):
    """Detects song theme from text."""

    def detect(self, text, prompt):
        m = re.search(r"about\s+(.+)", text)
        if m:
            prompt.theme = m.group(1).strip()[:120]


class KeyDetector(Detector):
    """Detects musical key/tonality from text."""

    def __init__(self, keys):
        self.keys = keys

    def detect(self, text, prompt):
        # Sort keys by length (descending) to match longer patterns first
        # This prevents "c major" from being matched as just "c" if "c#" exists
        sorted_keys = sorted(self.keys.items(), key=lambda x: len(x[0]), reverse=True)

        for key, val in sorted_keys:
            # Use word boundary matching for better accuracy
            if re.search(rf"\b{re.escape(key)}\b", text):
                prompt.key = val
                return


class EnergyDetector(Detector):
    """Detects energy level from the energy vocabulary (phrases + keywords)."""

    def __init__(self, energy_vocab):
        self.phrases = energy_vocab.get("phrases", {})
        self.keywords = energy_vocab.get("keywords", {})

    def detect(self, text, prompt):
        # Check multi-word phrases first (more specific)
        for key, val in self.phrases.items():
            if key in text:
                prompt.energy = val
                return
        # Fall back to single keywords
        for key, val in self.keywords.items():
            if re.search(rf"\b{re.escape(key)}\b", text):
                prompt.energy = val
                return


class StructureDetector(Detector):
    """Detects song-structure sections (intro, verse, chorus, …) from text."""

    def __init__(self, structure_vocab):
        self.tokens = {item["token"]: item["label"] for item in structure_vocab.get("tokens", [])}

    def detect(self, text, prompt):
        hits = []
        for token, label in self.tokens.items():
            if re.search(rf"\b{re.escape(token)}\b", text):
                hits.append(label)
        prompt.structure = list(dict.fromkeys(hits))


class RhythmDetector(Detector):
    """Detects rhythm patterns and time signatures from text."""

    def __init__(self, rhythm_vocab):
        self.time_signatures = rhythm_vocab.get("time_signatures", {})
        self.patterns = rhythm_vocab.get("patterns", {})

    def detect(self, text, prompt):
        hits = []
        # Time signatures may include "/" so use plain substring match
        for key, val in self.time_signatures.items():
            if key in text:
                hits.append(val)
        for key, val in self.patterns.items():
            if re.search(rf"\b{re.escape(key)}\b", text):
                hits.append(val)
        prompt.rhythm = list(dict.fromkeys(hits))


class EraDetector(Detector):
    """Detects music era / decade references from text."""

    def __init__(self, era_vocab):
        self.eras = era_vocab

    def detect(self, text, prompt):
        for key, val in self.eras.items():
            if key in text:
                prompt.era = val
                return
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
