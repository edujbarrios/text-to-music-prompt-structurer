"""Command-line interface for Text-to-Music Prompt Structurer."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from text_to_music_prompt_structurer.engine import MusicPromptEngine
from text_to_music_prompt_structurer.formatter import format_prompt
from text_to_music_prompt_structurer.suno import (
    SunoSection,
    render_suno_prompt,
    validate_suno_prompt,
)


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="text-to-music-prompt",
        description="Turn a musical idea into ready-to-paste Suno Custom/Advanced fields.",
    )
    parser.add_argument("description", nargs="+", help="free-form musical description")
    parser.add_argument(
        "--format",
        choices=("suno", "json", "legacy"),
        default="suno",
        help="output format (default: suno; legacy preserves the old STYLE/MOOD format)",
    )
    parser.add_argument("--title", default="", help="song title")
    parser.add_argument(
        "--lyrics-file", type=Path, help="UTF-8 file with complete lyrics and any section tags"
    )
    parser.add_argument(
        "--section", action="append", help="section tag for a lyric skeleton (repeatable)"
    )
    parser.add_argument(
        "--cue",
        action="append",
        default=[],
        metavar="SECTION[#N]=DIRECTION",
        help="non-sung cue for a section occurrence, e.g. Chorus#2=big drums",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="element to exclude using Suno's Exclude field (repeatable)",
    )
    parser.add_argument(
        "--instrumental",
        action="store_true",
        default=None,
        help="enable Instrumental (auto-detected from the description otherwise)",
    )
    parser.add_argument(
        "--style-notes", default="", help="additional musical/arrangement direction"
    )
    parser.add_argument(
        "--no-original",
        action="store_true",
        help="omit the original description from Style of Music (more concise)",
    )
    parser.add_argument(
        "--no-auto-exclude",
        action="store_true",
        help="disable extraction of explicit negatives such as no drums/sin batería",
    )
    parser.add_argument(
        "--check", action="store_true", help="show non-destructive preflight findings on stderr"
    )
    parser.add_argument(
        "--max-style-chars", type=int,
        help="optional self-imposed character budget for Style of Music",
    )
    parser.add_argument(
        "--max-lyrics-chars", type=int,
        help="optional self-imposed character budget for Lyrics",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)
    text = " ".join(args.description)
    engine = MusicPromptEngine()
    if args.format == "legacy":
        print(format_prompt(engine.process(text)))
        return 0

    if args.lyrics_file and args.section:
        parser.error("--lyrics-file and --section cannot be used together")

    # Bind cues to occurrences, not just names. Repeated Chorus sections can
    # each have their own direction; #2 explicitly addresses occurrence two.
    section_names = [name.strip() for name in (args.section or [])]
    by_name: dict[str, list[int]] = {}
    for index, name in enumerate(section_names):
        by_name.setdefault(name.casefold(), []).append(index)
    cues_by_index: dict[int, str] = {}
    for cue in args.cue:
        raw_name, separator, direction = cue.partition("=")
        name = raw_name.strip()
        if not separator or not name or not direction.strip():
            parser.error("--cue must be SECTION[#N]=DIRECTION")
        if "#" in name:
            name, _, ordinal = name.rpartition("#")
            name = name.strip()
            if not ordinal.isdigit() or int(ordinal) < 1:
                parser.error("--cue occurrence must be a positive number")
            occurrence = int(ordinal) - 1
        else:
            occurrence = None
        positions = by_name.get(name.casefold(), [])
        if not positions:
            parser.error("--cue refers to missing --section: " + name)
        if occurrence is not None:
            if occurrence >= len(positions):
                parser.error("--cue occurrence not found: " + raw_name)
            target = positions[occurrence]
        else:
            remaining = [idx for idx in positions if idx not in cues_by_index]
            if not remaining:
                parser.error("--cue has more directions than section occurrences: " + name)
            target = remaining[0]
        if target in cues_by_index:
            parser.error("--cue repeats direction for the same section: " + raw_name)
        cues_by_index[target] = direction.strip()
    sections = (
        [
            SunoSection(name, cue=cues_by_index.get(index, ""))
            for index, name in enumerate(section_names)
        ]
        if args.section
        else None
    )
    try:
        lyrics = args.lyrics_file.read_text(encoding="utf-8") if args.lyrics_file else ""
        fields = engine.process_suno(
            text,
            title=args.title,
            lyrics=lyrics,
            sections=sections,
            exclude=args.exclude,
            instrumental=args.instrumental,
            style_notes=args.style_notes,
            preserve_description=not args.no_original,
            auto_exclude=not args.no_auto_exclude,
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    if args.check:
        try:
            issues = validate_suno_prompt(
                fields,
                max_style_chars=args.max_style_chars,
                max_lyrics_chars=args.max_lyrics_chars,
            )
        except ValueError as error:
            parser.error(str(error))
        for issue in issues:
            print(f"{issue.severity.upper()} [{issue.code}]: {issue.message}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(fields.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_suno_prompt(fields))
    return 0


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
