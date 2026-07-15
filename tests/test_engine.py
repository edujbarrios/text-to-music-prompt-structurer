"""Tests for prompt detection and bundled resources."""

from __future__ import annotations

import shutil
from importlib import resources

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
