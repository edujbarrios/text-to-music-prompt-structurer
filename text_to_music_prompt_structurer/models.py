"""
Text-to-Music Prompt Structurer - Domain Models
"""

from dataclasses import dataclass, field


@dataclass
class MusicPrompt:
    """Structured musical prompt produced by the detection engine."""

    genre: str | None = None
    subgenre: str | None = None
    mood: list[str] = field(default_factory=list)
    energy: str | None = None
    tempo: str | None = None
    bpm: int | None = None
    key: str | None = None
    instruments: list[str] = field(default_factory=list)
    production: list[str] = field(default_factory=list)
    vocals: str | None = None
    vocal_style: list[str] = field(default_factory=list)
    language: str | None = None
    structure: list[str] = field(default_factory=list)
    rhythm: list[str] = field(default_factory=list)
    era: str | None = None
    theme: str | None = None
    notes: list[str] = field(default_factory=list)


SunoPrompt = MusicPrompt
"""Backward-compatible alias for :class:`MusicPrompt`."""
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
