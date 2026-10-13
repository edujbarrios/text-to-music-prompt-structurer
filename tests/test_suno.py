"""Suno-specific contract tests: fields, lyric safety, and CLI output."""

from __future__ import annotations

import json

import pytest

from text_to_music_prompt_structurer import (
    MusicPrompt,
    MusicPromptEngine,
    SunoSection,
    build_suno_prompt,
    format_for_suno,
)
from text_to_music_prompt_structurer.cli import main


def test_custom_fields_are_separate_from_analysis_labels() -> None:
    prompt = MusicPrompt(
        genre="Soul",
        subgenre="Neo Soul",
        mood=["Nostalgic"],
        bpm=92,
        key="D Minor",
        instruments=["Piano"],
        language="Spanish",
        voice_type=["Female Lead"],
        vocal_tone=["Breathy"],
        structure=["Verse", "Chorus"],
    )
    fields = build_suno_prompt(
        prompt,
        title="Luz de madrugada",
        lyrics="[Verse]\nDejé la luz encendida.\n\n[Chorus]\nSigo aquí.",
        exclude=["autotune", "distorted guitars"],
    )
    assert fields.title == "Luz de madrugada"
    assert fields.style_of_music.startswith("Neo Soul; Nostalgic mood; 92 BPM")
    assert "D Minor key" in fields.style_of_music
    assert "Piano" in fields.style_of_music
    assert "Spanish-language" in fields.style_of_music
    assert fields.lyrics == "[Verse]\nDejé la luz encendida.\n\n[Chorus]\nSigo aquí."
    assert fields.exclude == "autotune, distorted guitars"
    assert fields.vocal_gender == "Female"
    assert fields.to_dict()["style_of_music"] == fields.style_of_music
    rendered = format_for_suno(fields)
    assert "STYLE OF MUSIC\n" in rendered
    assert "LYRICS\n[Verse]" in rendered
    assert "EXCLUDE\nautotune" in rendered
    assert "MOOD:" not in rendered


def test_section_cues_are_attached_to_the_right_section() -> None:
    prompt = MusicPrompt(genre="Pop")
    fields = build_suno_prompt(
        prompt,
        sections=[
            SunoSection("Intro", cue="soft piano, no drums"),
            SunoSection("Verse 1", "La ciudad despierta", "intimate female lead"),
            SunoSection("Chorus", "Vuelvo a empezar", "full band, layered harmonies"),
            SunoSection("Verse 2", "La noche se aleja"),
            SunoSection("Final Chorus", "Vuelvo a empezar"),
            "Outro",
        ],
    )
    assert fields.lyrics == (
        "[Intro]\n[soft piano, no drums]\n\n"
        "[Verse 1]\n[intimate female lead]\nLa ciudad despierta\n\n"
        "[Chorus]\n[full band, layered harmonies]\nVuelvo a empezar\n\n"
        "[Verse 2]\nLa noche se aleja\n\n"
        "[Final Chorus]\nVuelvo a empezar\n\n[Outro]"
    )


def test_skeleton_uses_supported_detected_sections_only() -> None:
    prompt = MusicPrompt(structure=["Intro", "Riff", "Verse", "Chorus", "Outro"])
    fields = build_suno_prompt(prompt)
    assert fields.lyrics == "[Intro]\n\n[Verse]\n\n[Chorus]\n\n[Outro]"


def test_original_lyrics_never_rewritten_or_duplicated() -> None:
    lyrics = "[Verse 1]\nAún te espero...\n\n[Chorus]\n¡Vuelve! (oh-oh)"
    fields = build_suno_prompt(MusicPrompt(), lyrics=lyrics)
    assert fields.lyrics == lyrics


def test_invalid_section_and_cue_fail_fast() -> None:
    with pytest.raises(ValueError, match="Unsupported Suno section"):
        build_suno_prompt(MusicPrompt(), sections=["MysteriousTag"])
    with pytest.raises(ValueError, match="Section cues"):
        build_suno_prompt(
            MusicPrompt(), sections=[SunoSection("Verse", cue="first\n[Chorus]")]
        )
    with pytest.raises(ValueError, match="either complete lyrics"):
        build_suno_prompt(MusicPrompt(), lyrics="Hello", sections=["Verse"])


def test_instrumental_detection_and_conflicting_lyrics() -> None:
    fields = MusicPromptEngine().process_suno(
        "instrumental jazz with piano, 90 bpm",
        preserve_description=False,
    )
    assert fields.instrumental is True
    assert fields.lyrics == ""
    assert "Instrumental" in fields.style_of_music

    with pytest.raises(ValueError, match="Instrumental mode"):
        MusicPromptEngine().process_suno(
            "instrumental jazz with piano",
            lyrics="[Verse]\nSinging something",
        )


def test_lyric_brief_is_not_inserted_as_lyrics() -> None:
    fields = build_suno_prompt(
        MusicPrompt(theme="finding hope after a loss"), lyric_brief=None
    )
    assert fields.lyrics == ""
    assert fields.lyric_brief == "finding hope after a loss"
    assert "NOT the Lyrics field" in format_for_suno(fields)


def test_cli_suno_default_and_json_mode(capsys, tmp_path) -> None:
    main(["--title", "Medianoche", "--exclude", "autotune", "neo soul at 92 bpm"])
    result = capsys.readouterr().out
    assert "TITLE\nMedianoche" in result
    assert "STYLE OF MUSIC\n" in result
    assert "EXCLUDE\nautotune" in result
    assert "STYLE:" not in result

    lyric_file = tmp_path / "lyrics.txt"
    lyric_file.write_text("[Verse]\nTe recuerdo.\n", encoding="utf-8")
    main(["--format", "json", "--lyrics-file", str(lyric_file), "soul in spanish"])
    data = json.loads(capsys.readouterr().out)
    assert data["lyrics"] == "[Verse]\nTe recuerdo."
    assert data["instrumental"] is False


def test_cli_section_cue(capsys) -> None:
    main(
        [
            "--section", "Verse 1",
            "--cue", "Verse 1=whispered",
            "--section", "Chorus",
            "pop",
        ]
    )
    out = capsys.readouterr().out
    assert "LYRICS\n[Verse 1]\n[whispered]\n\n[Chorus]" in out


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
