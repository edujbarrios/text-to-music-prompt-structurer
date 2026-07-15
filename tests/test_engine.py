"""Tests for prompt detection and bundled resources."""

from __future__ import annotations

import shutil
from importlib import resources

import pytest

from text_to_music_prompt_structurer import MusicPromptEngine


def test_engine_detects_core_musical_fields() -> None:
    prompt = MusicPromptEngine().process(
        "indie pop with acoustic guitar in d minor, sad and nostalgic, 120 bpm"
    )

    assert prompt.genre == "Indie Pop"
    assert prompt.mood == ["Sad", "Nostalgic"]
    assert prompt.bpm == 120
    assert prompt.key == "D Minor"
    assert "Acoustic Guitar" in prompt.instruments


def test_bundled_vocabularies_load_outside_project_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    prompt = MusicPromptEngine().process("dark jazz at 90 bpm")

    assert prompt.genre == "Jazz"
    assert prompt.mood == ["Dark"]
    assert prompt.bpm == 90


@pytest.mark.parametrize(
    ("description", "genre", "subgenre"),
    [
        ("hypnotic techno with a pulsing bassline", "Electronic", "Hypnotic Techno"),
        ("a hazy future garage track", "Electronic", "Future Garage"),
        ("aggressive jersey drill", "Hip-Hop", "Jersey Drill"),
        ("lush quiet storm ballad", "R&B", "Quiet Storm"),
        ("atmospheric black metal with tremolo guitars", "Metal", "Atmospheric Black Metal"),
        ("meditative spiritual jazz", "Jazz", "Spiritual Jazz"),
        ("strict renaissance counterpoint", "Classical", "Renaissance"),
        ("rustic appalachian folk", "Folk", "Appalachian Folk"),
        ("brassy regional mexican celebration", "Latin", "Regional Mexican"),
        ("fast baile funk for a street party", "Latin", "Baile Funk"),
        ("minimal south african gqom", "African", "Gqom"),
        ("ceremonial japanese gagaku", "Japanese", "Gagaku"),
    ],
)
def test_engine_recognizes_expanded_genre_vocabulary(
    description: str, genre: str, subgenre: str
) -> None:
    prompt = MusicPromptEngine().process(description)

    assert prompt.genre == genre
    assert prompt.subgenre == subgenre


def test_genre_detection_does_not_match_inside_words() -> None:
    prompt = MusicPromptEngine().process("popular and emotional songwriting")

    assert prompt.genre is None
    assert prompt.subgenre is None


def test_custom_vocabulary_directory_is_supported(tmp_path) -> None:
    bundled = resources.files("text_to_music_prompt_structurer").joinpath("vocab")
    vocab_dir = tmp_path / "vocab"
    shutil.copytree(bundled, vocab_dir)
    genres = vocab_dir / "genres.json"
    genres.write_text(
        genres.read_text(encoding="utf-8").replace(
            '"indie pop": {',
            '"custom genre": {"genre": "Custom Genre", "subgenre": null},\n  "indie pop": {',
        ),
        encoding="utf-8",
    )

    prompt = MusicPromptEngine(vocab_dir=vocab_dir).process("custom genre")

    assert prompt.genre == "Custom Genre"
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
