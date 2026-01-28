"""
Suno Prompt Structurer - Output Formatter
"""

from suno_structurer.models import SunoPrompt


def format_for_suno(p: SunoPrompt) -> str:
    """Format a SunoPrompt object into a readable string."""
    lines = []

    if p.genre:
        lines.append(f"STYLE: {p.genre}")
    if p.mood:
        lines.append(f"MOOD: {', '.join(p.mood)}")
    if p.bpm:
        lines.append(f"TEMPO: ~{p.bpm} BPM")
    if p.key:
        lines.append(f"KEY: {p.key}")
    if p.instruments:
        lines.append(f"INSTRUMENTS: {', '.join(p.instruments)}")
    if p.production:
        lines.append(f"PRODUCTION: {', '.join(p.production)}")
    if p.vocals:
        lines.append(f"VOCALS: {p.vocals}")
    if p.language:
        lines.append(f"LANGUAGE: {p.language}")
    if p.theme:
        lines.append(f"THEME: {p.theme}")

    return "\n".join(lines)
