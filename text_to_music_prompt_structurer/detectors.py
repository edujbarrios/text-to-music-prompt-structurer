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
        # Resolve overlapping aliases (indie pop vs pop) by preferring
        # longer matches, while retaining distinct genre blends in source order.
        candidates = []
        for key, val in self.genres.items():
            for match in re.finditer(rf"(?<!\w){re.escape(key)}(?!\w)", text):
                candidates.append((match.start(), match.end(), val))
        candidates.sort(key=lambda hit: (hit[0], -(hit[1] - hit[0])))
        accepted = []
        for start, end, value in candidates:
            if not any(start < right and end > left for left, right, _ in accepted):
                accepted.append((start, end, value))
        if accepted:
            prompt.genre = accepted[0][2]["genre"]
            prompt.subgenre = accepted[0][2]["subgenre"]
            prompt.genres = list(dict.fromkeys(
                value["subgenre"] or value["genre"] for _, _, value in accepted
            ))

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


class VocalAttributeDetector(KeywordListDetector):
    """Detect a vocal attribute only when the prompt asks for a voice."""

    _vocal_context = re.compile(
        r"\b(?:vocal|vocals|voice|voices|singer|singers|singing|sung|choir|duet|"
        r"voz|voces|cantante|cantantes|cantado|cantada|coro|coros|susurrado|"
        r"susurrada|susurros|rasgada|rasgado)\b"
    )

    def detect(self, text, prompt):
        if self._vocal_context.search(text):
            super().detect(text, prompt)


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
    """Detect singing language from bounded, contextual phrases.

    A genre such as "Latin trap" should not become Latin-language singing;
    "Spanish guitar" should not become Spanish vocals by itself.
    """

    _vocal_context = re.compile(
        r"\b(?:vocals?|voice|singer|singing|sung|lyrics?|voices|"
        r"voz|voces|cantado|cantada|cantante|letra)\b"
    )
    _non_vocal_instrument = re.compile(
        r"^(?:guitar|horn|piano|bass|drums?|violin|strings?|trumpet)\b"
    )

    def __init__(self, languages):
        self.languages = dict(
            sorted(languages.items(), key=lambda item: len(item[0]), reverse=True)
        )

    def detect(self, text, prompt):
        has_vocals = bool(self._vocal_context.search(text))
        for key, val in self.languages.items():
            token = rf"(?<!\w){re.escape(key)}(?!\w)"
            # Explicit language instructions have priority over genre mentions.
            explicit = (
                rf"\b(?:in|en|sung\s+in|cantado\s+en|lyrics\s+in|letra\s+en)\s+{token}"
                rf"|{token}\s+(?:vocals?|lyrics?|voice|letra|voz|voces)"
            )
            if re.search(explicit, text):
                prompt.language = val
                return
            if key == "latin" or not has_vocals:
                continue
            for match in re.finditer(token, text):
                following = text[match.end():].lstrip()
                if self._non_vocal_instrument.match(following):
                    continue
                # Vocal context must be reasonably close, not a distant
                # reference elsewhere in a long free-form description.
                nearby = text[max(0, match.start() - 35):match.end() + 35]
                if self._vocal_context.search(nearby):
                    prompt.language = val
                    return


class BPMDetector(Detector):
    """Detects BPM (beats per minute) from text."""

    def detect(self, text, prompt):
        # Never match a substring of 1024 bpm, 2000 bpm or 120.5 bpm.
        # Stay within a conservative musical range instead of guessing.
        match = re.search(
            r"(?<![\w.])(\d{2,3})(?![\d.])\s*(?:bpm|beats per minute)\b", text
        )
        if match:
            value = int(match.group(1))
            if 30 <= value <= 300:
                prompt.bpm = value

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
    """Detect sections in source order, preserving repeats and numbered verses."""

    def __init__(self, structure_vocab):
        labels = {item["token"]: item["label"] for item in structure_vocab.get("tokens", [])}
        labels["final chorus"] = "Final Chorus"
        self.matchers = []
        for token, label in labels.items():
            pattern = rf"(?<!\w){re.escape(token)}(?!\w)"
            if label in {"Verse", "Chorus", "Bridge", "Interlude", "Solo"}:
                pattern += r"(?:\s+([1-9][0-9]?))?"
            self.matchers.append((re.compile(pattern), label))

    def detect(self, text, prompt):
        hits = []
        for pattern, label in self.matchers:
            for match in pattern.finditer(text):
                suffix = f" {match.group(1)}" if match.lastindex and match.group(1) else ""
                hits.append((match.start(), match.end(), label + suffix))
        # Longer matches at the same position take precedence:
        # Pre-Chorus beats Chorus, Final Chorus beats Chorus, etc.
        hits.sort(key=lambda item: (item[0], -(item[1] - item[0])))
        chosen = []
        last_end = -1
        for start, end, label in hits:
            if start >= last_end:
                chosen.append(label)
                last_end = end
        prompt.structure = chosen


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
