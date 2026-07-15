"""Command-line interface for Text-to-Music Prompt Structurer."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from text_to_music_prompt_structurer.engine import SunoPromptEngine
from text_to_music_prompt_structurer.formatter import format_for_suno


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="text-to-music-prompt",
        description="Turn a musical idea into a structured text-to-music prompt.",
    )
    parser.add_argument("description", nargs="+", help="free-form musical description")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    args = build_parser().parse_args(argv)
    prompt = SunoPromptEngine().process(" ".join(args.description))
    print(format_for_suno(prompt))
    return 0

