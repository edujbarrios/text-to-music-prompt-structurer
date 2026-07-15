"""Tests for formatting, compatibility, and command-line behavior."""

from __future__ import annotations

from importlib.metadata import version

import text_to_music_prompt_structurer
from text_to_music_prompt_structurer import (
    MusicPrompt,
    MusicPromptEngine,
    SunoPrompt,
    SunoPromptEngine,
    format_for_suno,
    format_prompt,
)
from text_to_music_prompt_structurer.cli import main


def test_formatter_renders_detected_fields() -> None:
    prompt = MusicPrompt(
        genre="Jazz",
        mood=["Mysterious"],
        bpm=90,
        key="C# Minor",
        instruments=["Piano", "Saxophone"],
    )

    assert format_prompt(prompt) == (
        "STYLE: Jazz\nMOOD: Mysterious\nBPM: ~90\nKEY: C# Minor\nINSTRUMENTS: Piano, Saxophone"
    )


def test_formatter_groups_vocal_controls_and_language() -> None:
    prompt = MusicPrompt(
        language="Spanish",
        voice_type=["Female Lead", "Alto"],
        vocal_tone=["Warm", "Breathy"],
        vocal_style=["Melismatic vocals"],
    )

    assert format_prompt(prompt) == (
        "VOCALS:\n"
        "  LANGUAGE: Spanish\n"
        "  VOICE TYPE: Female Lead, Alto\n"
        "  TONE: Warm, Breathy\n"
        "  STYLE: Melismatic vocals"
    )


def test_suno_names_remain_compatible() -> None:
    assert SunoPrompt is MusicPrompt
    assert SunoPromptEngine is MusicPromptEngine
    prompt = SunoPromptEngine().process("dreamy jazz")
    assert format_for_suno(prompt) == format_prompt(prompt)


def test_runtime_version_matches_distribution_metadata() -> None:
    assert text_to_music_prompt_structurer.__version__ == version("text-to-music-prompt-structurer")


def test_cli_prints_formatted_prompt(capsys) -> None:
    exit_code = main(["latin", "trap", "90", "bpm", "with", "808"])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert "STYLE: Latin Trap" in output
    assert "BPM: ~90" in output
    assert "INSTRUMENTS: 808 Bass" in output
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
