# Text-to-Music Prompt Structurer

[![PyPI version](https://img.shields.io/pypi/v/text-to-music-prompt-structurer?style=for-the-badge&logo=pypi&logoColor=white&label=PyPI&color=3775A9&cacheSeconds=300)](https://pypi.org/project/text-to-music-prompt-structurer/)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-orange.svg?style=for-the-badge)](LICENSE)
[![CI](https://github.com/edujbarrios/text-to-music-prompt-structurer/actions/workflows/ci.yml/badge.svg)](https://github.com/edujbarrios/text-to-music-prompt-structurer/actions/workflows/ci.yml)

**Convert a musical idea into separate, paste-ready Suno Custom/Advanced fields**, not
just a generic analysis of genres and instruments.

The engine is deterministic, offline, dependency-free and compatible with Python 3.10+.
It detects known musical characteristics from free-form text and preserves the original
creative direction by default so unfamiliar arrangement details are not silently lost.

> Unofficial project. Suno does not publish a strict metatag grammar, and
> generated audio is probabilistic. These are *input conventions* and sensible
> guidelines, not guaranteed commands or an official Suno API integration.

## Install

```bash
python -m pip install --upgrade "text-to-music-prompt-structurer>=0.2.0"
```

Version **0.2.0** introduces the Suno-specific output. Existing installs of 0.1.x
still use the old analysis format; upgrade to use the examples below.

## Get Suno-ready fields (default CLI output)

```bash
text-to-music-prompt --title "Luz de madrugada" \
  --exclude "autotune" \
  --section "Intro" --cue "Intro=soft piano, no drums" \
  --section "Verse 1" --cue "Verse 1=intimate, breathy lead" \
  --section "Chorus" --cue "Chorus=full band, layered backing harmonies" \
  --section "Bridge" --section "Final Chorus" --section "Outro" \
  "neo soul with piano, nostalgic female vocals in spanish, d minor, 92 bpm"
```

The command prints a **readable report of separate values** for Suno's creation fields.
The headings are not Suno metatags:

```text
TITLE
Luz de madrugada

STYLE OF MUSIC
Neo Soul; Nostalgic mood; 92 BPM; D Minor key; Instrumentation: Piano; Vocals: Spanish-language, Female Lead; Creative direction: neo soul with piano, nostalgic female vocals in spanish, d minor, 92 bpm

LYRICS
[Intro]
[soft piano, no drums]

[Verse 1]
[intimate, breathy lead]

[Chorus]
[full band, layered backing harmonies]

[Bridge]

[Final Chorus]

[Outro]

EXCLUDE
autotune

VOCAL GENDER
Female
```

**Copy the value under each heading into its matching Suno field.**
Do **not** paste the combined report into the Lyrics box.
Bracketed section labels such as `[Verse 1]` and `[Chorus]` are common
guidance markers; performance cues such as `[full band]` are best-effort
directions, not guaranteed engine instructions.

The skeleton above intentionally contains **no invented lyrics**. An empty section
is an editable template, **not a finished song lyric**.
Write your own lines under the tags, supply a lyric file, or use Suno's
own lyric-writing tools.

## Complete custom lyrics

```bash
text-to-music-prompt \
  --lyrics-file lyrics.txt \
  --title "Luz de madrugada" \
  --exclude "electric guitar" \
  "warm neo soul, 92 bpm, female vocals in Spanish"
```

A UTF-8 `lyrics.txt` can contain existing section labels and lyrics:

```text
[Verse 1]
La calle aún respira.
Tu nombre en el cristal.

[Chorus]
Volverá la luz.
Volverá la luz.
```

Its lyrics and section labels retain their exact wording (leading and trailing
blank newlines are stripped); they are **not translated, summarized or rewritten**. Use either `--lyrics-file`
or `--section`, not both.

## Python API — complex sectional control

```python
from text_to_music_prompt_structurer import (
    MusicPromptEngine,
    SunoSection,
    format_for_suno,
)

engine = MusicPromptEngine()
fields = engine.process_suno(
    "cinematic neo soul in d minor, 92 bpm, warm female vocals in spanish",
    title="Luz de madrugada",
    exclude=["autotune", "distorted guitars"],
    sections=[
        SunoSection("Intro", cue="solo electric piano, restrained ambience"),
        SunoSection("Verse 1", "La calle aún respira.", cue="intimate breathy lead"),
        SunoSection("Pre-Chorus", "Todo empieza a brillar.", cue="rising strings"),
        SunoSection("Chorus", "Volverá la luz.", cue="wide harmonies, full drums"),
        SunoSection("Bridge", "Una voz en la ciudad.", cue="half-time feel"),
        SunoSection("Final Chorus", "Volverá la luz.", cue="maximum emotional lift"),
        SunoSection("Outro", cue="piano resolves softly"),
    ],
)

print(fields.style_of_music)      # paste into Style of Music
print(fields.lyrics)              # paste into Lyrics
print(fields.exclude)             # paste into Advanced > Exclude
print(fields.vocal_gender)        # optional Vocal Gender UI control
print(format_for_suno(fields))    # readable combined presentation
payload = fields.to_dict()        # JSON-compatible values for your own app
```

For instrumental tracks, use `--instrumental`, or describe the track
as instrumental and let `process_suno()` detect it. Instrumental mode
rejects nonempty lyric lines rather than generating a contradictory request.

### CLI options

| Option | Purpose |
|---|---|
| `--format suno` | Separate Suno fields (default) |
| `--format json` | Machine-readable object with independent Suno fields |
| `--format legacy` | Preserve original `STYLE/MOOD/BPM/...` output |
| `--lyrics-file FILE` | Supply complete UTF-8 lyrics without rewriting |
| `--section NAME` | Add an editable structural section (repeatable) |
| `--cue NAME=DIRECTION` | Add a direction to the named section |
| `--exclude TEXT` | Fill Suno's separate Exclude control (repeatable) |
| `--instrumental` | Force Instrumental on |
| `--style-notes TEXT` | Additional freeform style/arrangement instruction |
| `--no-original` | Do not append the original creative description |
| `--title TITLE` | Song title |

Example JSON command:

```bash
text-to-music-prompt --format json --title "Medianoche" \
  --exclude "autotune" "dreamy synthwave 110 bpm female vocals"
```

## Outputs and migration

- **Suno human-readable report**: default CLI mode; paste values individually into Suno.
- **JSON**: `--format json` keeps `style_of_music`, `lyrics`, `title`, `exclude`,
  `instrumental`, `vocal_gender` and `lyric_brief` as independent properties.
- **Legacy analysis**: `--format legacy` or Python `format_prompt()` for existing
  integrations that need the `STYLE/MOOD/BPM` report.

A title is optional; `exclude` and `instrumental` are Advanced controls in Suno,
not strings to paste inside lyrics. `vocal_gender` is a suggested UI control when
unambiguous vocal type is detected. `lyric_brief` is **not** a Suno lyrics field.

## Legacy API / compatibility

`MusicPromptEngine().process(text)` still returns the existing
`MusicPrompt` dataclass with detected genre, subgenre, mood, BPM, key,
instruments, production, language, voice type, vocal style, rhythm,
structure, era and theme. `format_prompt(prompt)` still generates
the previous `STYLE: ...\nMOOD: ...` analysis view.

**Changed in 0.2:** `format_for_suno(prompt)` now renders actual Suno
fields instead of aliasing `format_prompt()`. The CLI defaults to Suno
fields, but `--format legacy` retains its previous display.

`SunoPrompt` and `SunoPromptEngine` remain aliases of the original
`MusicPrompt` and `MusicPromptEngine`. Use `SunoFields` when you need
paste-ready Suno controls.

An optional `lyric_brief` in `SunoFields` is explicitly a theme brief
for a *lyric-generation tool*. It is **not** auto-inserted into Lyrics
because prose requests may be sung literally.

## Supported and unsupported behavior

This package **does not** connect to Suno, generate audio, guarantee exact
timing, guarantee every section cue will be obeyed, or use an LLM to write
new lyrics. Some free-form details are outside its keyword vocabulary;
the original source sentence is preserved as additional musical guidance
unless `--no-original` is set. Manually review ambiguous instructions
or contradictory constraints before pasting into Suno.

Official source references for the field design and conventions:

- [Suno: How to Make a Song](https://suno.com/hub/how-to-make-a-song) — Style, Lyrics and section labels
- [Suno: v6 FAQ](https://help.suno.com/en/articles/13924481) — complex instructions and current model family
- [Suno: Exclude elements](https://help.suno.com/en/articles/3161921) — the separate Exclude control
- [Suno: Vocal Gender](https://help.suno.com/en/articles/10153473) — vocal gender in Advanced Options
- [Suno: Lyrics improvements](https://suno.com/release-notes/lyrics-improvements-on-web) — structure labels in the editor

## Development

```bash
git clone https://github.com/edujbarrios/text-to-music-prompt-structurer.git
cd text-to-music-prompt-structurer
python -m pip install -e ".[dev]"
python -m pytest
ruff check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) to extend the vocabularies.

## License

Copyright © 2026 Eduardo J. Barrios.

Licensed under the [Mozilla Public License 2.0](LICENSE). See
[NOTICE](NOTICE) for attribution details.
