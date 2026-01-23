"""
Suno Prompt Structurer - Detection Strategies
"""

import re
from suno_structurer.models import SunoPrompt


class Detector:
    """Base class for all detectors."""
    
    def detect(self, text: str, prompt: SunoPrompt):
        raise NotImplementedError


class GenreDetector(Detector):
    """Detects musical genres from text."""
    
    def __init__(self, genres):
        self.genres = genres

    def detect(self, text, prompt):
        for key, val in self.genres.items():
            if key in text:
                prompt.genre = val["genre"]
                prompt.subgenre = val["subgenre"]
                return


class KeywordListDetector(Detector):
    """Generic detector for keyword-based attributes."""
    
    def __init__(self, source, target_attr):
        self.source = source
        self.target_attr = target_attr

    def detect(self, text, prompt):
        hits = []
        for key, val in self.source.items():
            if re.search(rf"\b{re.escape(key)}\b", text):
                hits.append(val)
        setattr(prompt, self.target_attr, list(dict.fromkeys(hits)))


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
