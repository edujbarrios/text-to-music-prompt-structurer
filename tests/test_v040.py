"""Regression coverage for v0.4.0: scoped constraints and complex music prompts."""

from __future__ import annotations

import json

import pytest

from text_to_music_prompt_structurer import (
    MusicPromptEngine,
    extract_negative_constraints,
)
from text_to_music_prompt_structurer.cli import main


@pytest.mark.parametrize("bpm", ["1024 bpm", "2000 bpm", "999 bpm", "120.5 bpm", "12 bpm"])
def test_invalid_or_partial_bpm_is_not_detected(bpm: str) -> None:
    assert MusicPromptEngine().process("cinematic ambient " + bpm).bpm is None


@pytest.mark.parametrize("bpm", ["30 bpm", "105 BPM", "300 beats per minute"])
def test_valid_bpm(bpm: str) -> None:
    assert MusicPromptEngine().process(bpm).bpm == int(bpm.split()[0])


@pytest.mark.parametrize(
    "description",
    [
        "no drums in the intro, drums in the chorus",
        "without guitar during the verse, guitar in the chorus",
        "sin batería en el verso, batería en el estribillo",
        "intro without drums, full drums after intro",
        "no drums until chorus, then heavy drums",
    ],
)
def test_local_exclusions_do_not_become_global(description: str) -> None:
    result = extract_negative_constraints(description)
    assert result.excludes == ()
    assert result.cleaned_description == description
    assert "no drums" not in result.detection_description


def test_mixed_local_and_global_negations() -> None:
    fields = MusicPromptEngine().process_suno(
        "no drums in intro; drums in chorus; no autotune, warm piano"
    )
    assert fields.exclude == "Autotune"
    assert "no drums in intro" in fields.style_of_music
    assert "Instrumentation:" in fields.style_of_music


def test_local_negative_does_not_become_positive_instrument() -> None:
    fields = MusicPromptEngine().process_suno("no drums in intro, warm piano")
    assert fields.exclude == ""
    assert "Instrumentation: Piano" in fields.style_of_music
    assert "Instrumentation: Drums" not in fields.style_of_music


def test_whitespace_normalization_in_style_summary() -> None:
    fields = MusicPromptEngine().process_suno(
        "neo soul, no drums, piano without autotune"
    )
    assert fields.exclude == "Drums, Autotune"
    assert "  ," not in fields.style_of_music
    assert " , " not in fields.style_of_music
    assert "without autotune" not in fields.style_of_music.lower()


def test_multigenre_in_source_order_with_overlap_suppression() -> None:
    prompt = MusicPromptEngine().process("indie pop meets jazz and neo soul")
    assert prompt.genre == "Indie Pop"
    assert prompt.genres == ["Indie Pop", "Jazz", "Neo Soul"]
    fields = MusicPromptEngine().process_suno(
        "indie pop meets jazz and neo soul", preserve_description=False
    )
    assert "Genre blend: Indie Pop + Jazz + Neo Soul" in fields.style_of_music


def test_single_genre_remains_backwards_compatible() -> None:
    prompt = MusicPromptEngine().process("hypnotic techno at 122 bpm")
    assert prompt.genre == "Electronic"
    assert prompt.subgenre == "Hypnotic Techno"
    assert prompt.genres == ["Hypnotic Techno"]


@pytest.mark.parametrize(
    ("description", "voice", "tone", "delivery"),
    [
        ("voz femenina rasgada", "Female Lead", "Raspy", None),
        ("voz masculina susurrada", "Male Lead", None, "Whispered delivery"),
        ("voz rasgada y coros", None, "Raspy", "Backing vocals"),
        ("cantante femenina con voz cálida", "Female Lead", "Warm", None),
    ],
)
def test_spanish_voice_terms(
    description: str, voice: str | None, tone: str | None, delivery: str | None
) -> None:
    prompt = MusicPromptEngine().process(description)
    if voice:
        assert voice in prompt.voice_type
    if tone:
        assert tone in prompt.vocal_tone
    if delivery:
        assert delivery in prompt.vocal_style


def test_cli_repeated_named_sections_use_ordered_cues(capsys) -> None:
    assert main([
        "--section", "Chorus", "--section", "Verse 2", "--section", "Chorus",
        "--cue", "Chorus=restrained harmony",
        "--cue", "Chorus=full choir",
        "rock",
    ]) == 0
    output = capsys.readouterr().out
    assert "[Chorus]\n[restrained harmony]\n\n[Verse 2]\n\n[Chorus]\n[full choir]" in output


def test_cli_indexed_section_cues(capsys) -> None:
    assert main([
        "--section", "Chorus", "--section", "Chorus",
        "--cue", "Chorus#2=big finale",
        "--cue", "Chorus#1=quiet refrain",
        "soul",
    ]) == 0
    output = capsys.readouterr().out
    assert "[Chorus]\n[quiet refrain]\n\n[Chorus]\n[big finale]" in output


@pytest.mark.parametrize(
    "cue_args",
    [
        ["--cue", "Chorus#3=no drums"],
        ["--cue", "Chorus#0=invalid"],
        ["--cue", "Chorus=soft", "--cue", "Chorus=big"],
        ["--cue", "Verse=unknown"],
    ],
)
def test_cli_invalid_or_redundant_cues_error(cue_args: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["--section", "Chorus", *cue_args, "pop"])
    assert error.value.code == 2


def test_multigenre_json_remains_separate_from_suno_output(capsys) -> None:
    assert main(["--format", "json", "latin trap with jazz, no autotune"]) == 0
    fields = json.loads(capsys.readouterr().out)
    assert fields["exclude"] == "Autotune"
    assert "Genre blend" in fields["style_of_music"]


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
