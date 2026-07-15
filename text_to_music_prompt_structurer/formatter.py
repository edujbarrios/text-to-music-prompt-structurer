"""
Text-to-Music Prompt Structurer - Output Formatter
"""

from text_to_music_prompt_structurer.models import MusicPrompt


def format_prompt(p: MusicPrompt) -> str:
    """Format a music prompt as compact, labeled text."""
    lines = []

    if p.genre:
        style = p.genre
        if p.subgenre:
            style = f"{p.genre} / {p.subgenre}"
        lines.append(f"STYLE: {style}")
    if p.mood:
        lines.append(f"MOOD: {', '.join(p.mood)}")
    if p.energy:
        lines.append(f"ENERGY: {p.energy}")
    if p.bpm:
        lines.append(f"BPM: ~{p.bpm}")
    if p.tempo:
        lines.append(f"TEMPO: {p.tempo}")
    if p.rhythm:
        lines.append(f"RHYTHM: {', '.join(p.rhythm)}")
    if p.key:
        lines.append(f"KEY: {p.key}")
    if p.instruments:
        lines.append(f"INSTRUMENTS: {', '.join(p.instruments)}")
    if p.production:
        lines.append(f"PRODUCTION: {', '.join(p.production)}")
    if p.voice_type or p.vocal_tone or p.vocal_style or p.vocals or p.language:
        lines.append("VOCALS:")
        if p.language:
            lines.append(f"  LANGUAGE: {p.language}")
        if p.voice_type:
            lines.append(f"  VOICE TYPE: {', '.join(p.voice_type)}")
        if p.vocal_tone:
            lines.append(f"  TONE: {', '.join(p.vocal_tone)}")
        if p.vocal_style:
            lines.append(f"  STYLE: {', '.join(p.vocal_style)}")
        elif p.vocals:
            lines.append(f"  STYLE: {p.vocals}")
    if p.era:
        lines.append(f"ERA: {p.era}")
    if p.structure:
        lines.append(f"STRUCTURE: {', '.join(p.structure)}")
    if p.theme:
        lines.append(f"THEME: {p.theme}")

    return "\n".join(lines)


def format_for_suno(prompt: MusicPrompt) -> str:
    """Format a prompt using the Suno-compatible text representation."""
    return format_prompt(prompt)
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
