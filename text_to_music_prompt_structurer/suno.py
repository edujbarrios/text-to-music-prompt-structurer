"""Suno Custom/Advanced field builder.

Suno is not a text markup protocol. Its Custom/Advanced interface has separate
Style of Music, Lyrics, Exclude, Title and other controls. This module models
those inputs rather than pretending a labeled analysis block is a Suno prompt.

Unofficial integration; no Suno API is called.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from text_to_music_prompt_structurer.models import MusicPrompt


# Supported song-section names are intentionally conservative. They are guidance
# labels, not a claim that Suno provides a formal, guaranteed metatag language.
_SECTION_NAMES = (
    "Intro",
    "Verse",
    "Pre-Chorus",
    "Chorus",
    "Post-Chorus",
    "Bridge",
    "Outro",
    "Interlude",
    "Instrumental",
    "Instrumental Break",
    "Solo",
    "Breakdown",
    "Build",
    "Build-Up",
    "Drop",
    "Hook",
    "Refrain",
    "Final Chorus",
    "Coda",
)
_SECTION_PATTERN = re.compile(
    r"^(" + "|".join(re.escape(name) for name in sorted(_SECTION_NAMES, key=len, reverse=True))
    + r")(?:\s+([1-9][0-9]?))?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SunoSection:
    """A section label, optional non-vocal direction, and optional actual lyrics."""

    name: str
    lyrics: str = ""
    cue: str = ""


@dataclass(frozen=True)
class SunoFields:
    """Separate, paste-ready fields for Suno's Custom/Advanced create screen."""

    style_of_music: str
    lyrics: str = ""
    title: str = ""
    exclude: str = ""
    instrumental: bool = False
    vocal_gender: str | None = None
    lyric_brief: str = ""

    def to_dict(self) -> dict[str, str | bool | None]:
        """Serialize field values (including optional UI toggles) to JSON-ready data."""
        return asdict(self)


def _unique(items: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(item.strip() for item in items if item.strip()))


def _section_tag(name: str) -> str:
    match = _SECTION_PATTERN.fullmatch(name.strip())
    if not match:
        raise ValueError(f"Unsupported Suno section name: {name!r}")
    canonical = next(
        item for item in _SECTION_NAMES if item.lower() == match.group(1).lower()
    )
    return f"[{canonical}{' ' + match.group(2) if match.group(2) else ''}]"


def _render_sections(sections: Sequence[SunoSection | str]) -> str:
    rendered = []
    for section in sections:
        part = SunoSection(section) if isinstance(section, str) else section
        lines = [_section_tag(part.name)]
        if part.cue:
            cue = part.cue.strip()
            # A cue is a single direction tag, not an opportunity to inject
            # extra section headers or multiline lyric content.
            if not cue or any(character in cue for character in "[]\r\n"):
                raise ValueError("Section cues must be a single line without brackets")
            lines.append(f"[{cue}]")
        if part.lyrics.strip():
            lines.append(part.lyrics.strip("\n"))
        rendered.append("\n".join(lines))
    return "\n\n".join(rendered)


def _style_from_prompt(prompt: MusicPrompt, *, instrumental: bool, notes: str) -> str:
    clauses: list[str] = []

    genre = prompt.subgenre or prompt.genre
    if genre:
        clauses.append(genre)
    if prompt.mood:
        clauses.append(f"{', '.join(_unique(prompt.mood))} mood")
    if prompt.energy:
        clauses.append(f"{prompt.energy} energy")
    if prompt.bpm:
        clauses.append(f"{prompt.bpm} BPM")
    elif prompt.tempo:
        clauses.append(f"{prompt.tempo} tempo")
    if prompt.key:
        clauses.append(f"{prompt.key} key")
    if prompt.rhythm:
        clauses.append(f"Rhythm: {', '.join(_unique(prompt.rhythm))}")
    if prompt.instruments:
        clauses.append(f"Instrumentation: {', '.join(_unique(prompt.instruments))}")
    if prompt.era:
        clauses.append(f"Era: {prompt.era}")
    if prompt.production:
        clauses.append(f"Production: {', '.join(_unique(prompt.production))}")
    if instrumental:
        clauses.append("Instrumental, no sung vocals")
    else:
        vocal = []
        if prompt.language:
            vocal.append(f"{prompt.language}-language")
        vocal.extend(_unique(prompt.voice_type))
        vocal.extend(_unique(prompt.vocal_tone))
        vocal.extend(_unique(prompt.vocal_style))
        if prompt.vocals:
            vocal.append(prompt.vocals)
        if vocal:
            clauses.append(f"Vocals: {', '.join(_unique(vocal))}")
    if notes.strip():
        clauses.append(notes.strip())
    return "; ".join(clauses)


def build_suno_prompt(
    prompt: MusicPrompt,
    *,
    title: str = "",
    lyrics: str = "",
    sections: Sequence[SunoSection | str] | None = None,
    exclude: str | Sequence[str] = "",
    instrumental: bool = False,
    style_notes: str = "",
    lyric_brief: str | None = None,
) -> SunoFields:
    """Convert detected musical attributes into Suno Custom/Advanced fields.

    Use `lyrics` for complete user-written text (existing [Verse] tags are
    preserved verbatim), OR `sections` for a structured draft with optional
    per-section lyrics/cues. Neither path invents lyric lines.

    Without explicit lyrics or sections, any sections detected in `prompt`
    become an editable song skeleton. `lyric_brief` is *not* placed in the
    Lyrics field because Suno could sing prose instructions literally.
    """
    if instrumental and (lyrics.strip() or any(
        isinstance(section, SunoSection) and section.lyrics.strip()
        for section in (sections or ())
    )):
        raise ValueError("Instrumental mode cannot be combined with sung lyrics")
    if sections is not None and lyrics.strip():
        raise ValueError("Supply either complete lyrics or structured sections, not both")

    if sections is not None:
        lyric_text = _render_sections(sections)
    elif lyrics.strip():
        lyric_text = lyrics.strip("\n")
    elif prompt.structure and not instrumental:
        # Broad analysis vocab includes names that are not safe lyric tags.
        # Keep only recognized section markers in a Suno-facing skeleton.
        supported = [name for name in prompt.structure if _SECTION_PATTERN.fullmatch(name)]
        lyric_text = _render_sections(supported)
    else:
        lyric_text = ""

    excluded = exclude.strip() if isinstance(exclude, str) else ", ".join(_unique(exclude))

    genders = {
        gender for gender in ("Male", "Female")
        if any(re.search(rf"\b{gender}\b", value, re.IGNORECASE) for value in prompt.voice_type)
    }
    gender = next(iter(genders)) if len(genders) == 1 and not instrumental else None
    return SunoFields(
        title=title.strip(),
        style_of_music=_style_from_prompt(
            prompt, instrumental=instrumental, notes=style_notes
        ),
        lyrics=lyric_text,
        exclude=excluded,
        instrumental=instrumental,
        vocal_gender=gender,
        lyric_brief=(prompt.theme if lyric_brief is None else lyric_brief) or "",
    )


def render_suno_prompt(fields: SunoFields) -> str:
    """Human-readable separate-field presentation for copying to Suno.

    The section headings below are for humans, NOT tags to paste together into
    Suno's Lyrics field. Prefer `fields.to_dict()` for an app integration.
    """
    parts = []
    if fields.title:
        parts.append(f"TITLE\n{fields.title}")
    parts.append(f"STYLE OF MUSIC\n{fields.style_of_music}")
    if fields.lyrics:
        parts.append(f"LYRICS\n{fields.lyrics}")
    if fields.exclude:
        parts.append(f"EXCLUDE\n{fields.exclude}")
    if fields.instrumental:
        parts.append("INSTRUMENTAL\nOn")
    if fields.vocal_gender:
        parts.append(f"VOCAL GENDER\n{fields.vocal_gender}")
    if fields.lyric_brief:
        parts.append(
            "LYRIC BRIEF (for the lyric generator, NOT the Lyrics field)\n"
            + fields.lyric_brief
        )
    return "\n\n".join(parts)


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
