"""Quality-oriented prompting tests for v0.3.0."""

from __future__ import annotations

import json

import pytest

from text_to_music_prompt_structurer import (
    MusicPromptEngine,
    SunoFields,
    SunoSection,
    extract_negative_constraints,
    validate_suno_prompt,
)
from text_to_music_prompt_structurer.cli import main


@pytest.mark.parametrize(
    ("description", "expected"),
    [
        ("soul pop without drums with piano", ["Drums"]),
        ("neo soul sin batería y con piano", ["Drums"]),
        ("synthwave no autotune, without guitar", ["Autotune", "Guitar"]),
        ("jazz avoid reverb, exclude distortion", ["Reverb", "Distortion"]),
    ],
)
def test_exclusion_detection(description: str, expected: list[str]) -> None:
    negatives = extract_negative_constraints(description)
    assert list(negatives.excludes) == expected


def test_no_false_exclusions_from_unrelated_language() -> None:
    negatives = extract_negative_constraints("no strings attached, without you, solo piano")
    assert negatives.excludes == ()
    assert negatives.cleaned_description == "no strings attached, without you, solo piano"


def test_suno_exclude_masks_negative_instrument_from_positive_style() -> None:
    fields = MusicPromptEngine().process_suno(
        "neo soul, 92 bpm, no drums, warm piano, without autotune",
        preserve_description=False,
    )
    assert fields.exclude == "Drums, Autotune"
    assert "Instrumentation: Piano" in fields.style_of_music
    assert "Drums" not in fields.style_of_music
    assert "Autotune" not in fields.style_of_music


def test_explicit_excludes_are_deduplicated_without_losing_order() -> None:
    fields = MusicPromptEngine().process_suno(
        "neo soul with no drums, without autotune",
        exclude=["drums", "Vocoder"],
        preserve_description=False,
    )
    assert fields.exclude == "drums, Vocoder, Autotune"


def test_auto_exclude_opt_out() -> None:
    fields = MusicPromptEngine().process_suno(
        "neo soul no drums",
        auto_exclude=False,
        preserve_description=False,
    )
    assert fields.exclude == ""


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("latin trap with male vocals", None),
        ("spanish guitar with soulful vocals", None),
        ("soulful female vocals in Spanish", "Spanish"),
        ("jazz sung in Latin", "Latin"),
        ("neo soul en español con voz femenina", "Spanish"),
        ("future garage female vocals in English", "English"),
    ],
)
def test_language_detection_respects_singing_context(
    text: str, expected: str | None
) -> None:
    assert MusicPromptEngine().process(text).language == expected


def test_suno_validator_flags_missing_lyrics_but_does_not_mutate() -> None:
    fields = SunoFields(style_of_music="Neo Soul", lyrics="")
    issues = validate_suno_prompt(fields)
    assert [issue.code for issue in issues] == ["no_lyrics"]
    assert fields.lyrics == ""


def test_suno_validator_detects_conflict_and_budgets() -> None:
    fields = SunoFields(
        style_of_music="Neo Soul with dreamy piano",
        lyrics="[Verse]\\nSing this line.",
        instrumental=True,
        vocal_gender="Female",
    )
    issues = validate_suno_prompt(fields, max_style_chars=10, max_lyrics_chars=5)
    assert {issue.code for issue in issues} == {
        "instrumental_lyrics_conflict",
        "instrumental_gender_conflict",
        "style_budget",
        "lyrics_budget",
    }
    assert all(issue.severity in ("warning", "error") for issue in issues)


def test_section_skeleton_warning() -> None:
    fields = MusicPromptEngine().process_suno(
        "neo soul", sections=[SunoSection("Verse 1"), "Chorus"]
    )
    assert "section_skeleton" in [issue.code for issue in validate_suno_prompt(fields)]


@pytest.mark.parametrize("kwargs", [{"max_style_chars": 0}, {"max_lyrics_chars": -1}])
def test_invalid_budgets_raise(kwargs: dict[str, int]) -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        validate_suno_prompt(SunoFields(style_of_music="Music"), **kwargs)


def test_cli_check_warnings_to_stderr_without_polluting_json(capsys) -> None:
    assert main(["--format", "json", "--check", "neo soul without drums"]) == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["exclude"] == "Drums"
    assert "WARNING [no_lyrics]" in captured.err


def test_cli_no_auto_exclude(capsys) -> None:
    assert main(["--format", "json", "--no-auto-exclude", "pop without drums"]) == 0
    assert json.loads(capsys.readouterr().out)["exclude"] == ""


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
