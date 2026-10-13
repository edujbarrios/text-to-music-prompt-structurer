"""Command-line interface for Text-to-Music Prompt Structurer."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from text_to_music_prompt_structurer.engine import MusicPromptEngine
from text_to_music_prompt_structurer.formatter import format_prompt
from text_to_music_prompt_structurer.suno import SunoSection, render_suno_prompt


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
        metavar="SECTION=DIRECTION",
        help="non-sung bracketed direction for a named --section (repeatable)",
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

    cue_map = {}
    for cue in args.cue:
        name, separator, direction = cue.partition("=")
        if not separator or not name.strip() or not direction.strip():
            parser.error("--cue must be SECTION=DIRECTION")
        cue_map[name.strip().lower()] = direction.strip()
    if cue_map and not args.section:
        parser.error("--cue requires at least one --section")

    sections = None
    if args.section:
        sections = [
            SunoSection(name, cue=cue_map.get(name.lower(), ""))
            for name in args.section
        ]
        unknown = set(cue_map) - {name.lower() for name in args.section}
        if unknown:
            parser.error("--cue refers to missing --section: " + ", ".join(sorted(unknown)))

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
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    if args.format == "json":
        print(json.dumps(fields.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_suno_prompt(fields))
    return 0


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
