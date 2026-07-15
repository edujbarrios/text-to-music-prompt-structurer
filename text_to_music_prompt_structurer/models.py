"""
Text-to-Music Prompt Structurer - Domain Models
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MusicPrompt:
    """Structured musical prompt produced by the detection engine."""
    genre: Optional[str] = None
    subgenre: Optional[str] = None
    mood: List[str] = field(default_factory=list)
    energy: Optional[str] = None
    tempo: Optional[str] = None
    bpm: Optional[int] = None
    key: Optional[str] = None
    instruments: List[str] = field(default_factory=list)
    production: List[str] = field(default_factory=list)
    vocals: Optional[str] = None
    vocal_style: List[str] = field(default_factory=list)
    language: Optional[str] = None
    structure: List[str] = field(default_factory=list)
    rhythm: List[str] = field(default_factory=list)
    era: Optional[str] = None
    theme: Optional[str] = None
    notes: List[str] = field(default_factory=list)


SunoPrompt = MusicPrompt
"""Backward-compatible alias for :class:`MusicPrompt`."""
