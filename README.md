# Text-to-Music Prompt Structurer

[![PyPI](https://img.shields.io/pypi/v/text-to-music-prompt-structurer)](https://pypi.org/project/text-to-music-prompt-structurer/)
[![CI](https://github.com/edujbarrios/text-to-music-prompt-structurer/actions/workflows/ci.yml/badge.svg)](https://github.com/edujbarrios/text-to-music-prompt-structurer/actions/workflows/ci.yml)
[![MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue)](LICENSE)

Turn a musical idea into **separate Suno Custom/Advanced inputs**: Style of Music,
Lyrics, Exclude, title and optional vocal controls. Works offline, has no mandatory
dependencies and requires **Python 3.10+**.

## Install

~~~bash
pip install --upgrade text-to-music-prompt-structurer
~~~

Verify:

~~~bash
text-to-music-prompt --help
~~~

## Quick start

~~~bash
text-to-music-prompt --title "Luz de madrugada" \
  "neo soul and jazz, warm female vocals in Spanish, piano, 92 bpm, no autotune"
~~~

The result includes separate headings such as:

~~~text
TITLE
Luz de madrugada

STYLE OF MUSIC
Genre blend: Neo Soul + Jazz; 92 BPM; ...

EXCLUDE
Autotune

VOCAL GENDER
Female
~~~

**Copy each value to the matching Suno field.** Do not paste the whole report
into the Lyrics field. `--format json` produces equivalent separate properties,
useful for apps and automation.

## Lyrics and song sections

Supply your own lyrics (preserved without rewriting):

~~~bash
text-to-music-prompt --lyrics-file lyrics.txt \
  "nostalgic soul, female vocals in Spanish, 90 bpm"
~~~

Or create a song structure with instructions for individual sections:

~~~bash
text-to-music-prompt \
  --section "Intro" --cue "Intro=solo piano, no drums" \
  --section "Verse 1" \
  --section "Chorus" --cue "Chorus=restrained harmonies" \
  --section "Chorus" --cue "Chorus#2=full band, huge final chorus" \
  --section "Outro" --cue "Outro=piano only" \
  "melancholic indie pop and jazz, intimate female voice, 105 bpm"
~~~

Repeated sections can have different cues. Use `--cue "Chorus#2=..."`
to target the **second occurrence**; repeated unnumbered `Chorus=...` cues
are assigned in order. The generated section skeleton does not invent lyrics.

## Python API

~~~python
from text_to_music_prompt_structurer import (
    MusicPromptEngine, SunoSection, validate_suno_prompt,
)

engine = MusicPromptEngine()
fields = engine.process_suno(
    "cinematic neo soul and jazz, 92 bpm, piano, female vocals in Spanish, no autotune",
    title="Luz de madrugada",
    sections=[
        SunoSection("Verse 1", lyrics="Aún espero la luz.", cue="breathy solo lead"),
        SunoSection("Chorus", lyrics="Volverá la luz.", cue="layered harmonies"),
    ],
)
print(fields.style_of_music)  # Suno -> Style of Music
print(fields.lyrics)          # Suno -> Lyrics
print(fields.exclude)         # Suno -> Exclude
print(fields.to_dict())       # Structured Python dictionary
print(validate_suno_prompt(fields))
~~~

## Useful CLI flags

| Flag | Purpose |
| --- | --- |
| `--format json` | Machine-readable Suno fields |
| `--format legacy` | Previous `STYLE/MOOD/BPM` analysis |
| `--lyrics-file FILE` | Use your own UTF-8 lyrics |
| `--section NAME` | Append a song section; repeatable |
| `--cue "NAME[#N]=TEXT"` | Direct a named section or the Nth occurrence |
| `--exclude "TEXT"` | Add an explicit Exclude field item |
| `--instrumental` | Enable instrumental-only mode |
| `--style-notes "TEXT"` | Append production details |
| `--no-original` | Omit the free-form description from the style summary |
| `--no-auto-exclude` | Disable extraction of global `no X` directives |
| `--check` | Print quality warnings to stderr |
| `--max-style-chars N` | Optional user-defined style budget, with `--check` |
| `--max-lyrics-chars N` | Optional user-defined lyrics budget, with `--check` |

~~~bash
text-to-music-prompt --format json --check --max-style-chars 1000 \
  "indie pop and jazz, piano, 105 bpm, without autotune"
~~~

**Constraints:** global `no drums` is mapped to Exclude, but
`no drums in the intro, drums in the chorus` is kept as a
**section-local musical direction**, not a global exclusion. The parser
supports common Spanish phrasing such as `sin batería`, `voz femenina`,
`voz rasgada`, `susurrado` and `coros`. Detected multi-genre blends retain
their source order. Numeric BPM values must be complete, in the supported
30–300 BPM range.

## Project vision

Led by **Eduardo J. Barrios**, whose background includes advanced knowledge
of **AI, NLP and LLMs**, this project aims to design an extensible, rigorous
music-prompting system suited to Suno. The current implementation is a
deterministic local parser, **not an LLM or a Suno API client**. Section tags
and arrangement instructions are guidance rather than guaranteed generation
controls.

## Development and releases

~~~bash
git clone https://github.com/edujbarrios/text-to-music-prompt-structurer.git
cd text-to-music-prompt-structurer
pip install -e ".[dev]"
pytest
ruff check .
~~~

Merging an updated package version in `pyproject.toml` into `main`
automatically triggers [GitHub Actions](.github/workflows/release.yml) to
test, build, publish to PyPI (OIDC Trusted Publishing) and attach distributions
to the corresponding GitHub Release. The PyPI project must have a Trusted
Publisher for `edujbarrios/text-to-music-prompt-structurer`,
workflow `release.yml`, environment `pypi`.

See [CHANGELOG](CHANGELOG.md), [CONTRIBUTING](CONTRIBUTING.md)
and the [MPL-2.0 license](LICENSE).
