# Text-to-Music Prompt Structurer

Turn free-form musical ideas into consistent, structured prompts for text-to-music workflows.

Text-to-Music Prompt Structurer detects the musical details in a plain-language description—such as genre, mood, tempo, key, instrumentation, production, vocals, and language—and organizes them into a predictable result. The included formatter produces concise, Suno-compatible prompt output, while the structured Python model can be used in other music-generation workflows.

## Features

- Detects genres and subgenres
- Extracts moods, tempo, BPM, and musical keys
- Identifies instruments, vocal styles, and languages
- Recognizes production and mixing characteristics
- Returns structured Python objects for custom integrations
- Formats results as readable, Suno-compatible prompts
- Runs locally with Python and no third-party dependencies

## Quick start

```bash
git clone https://github.com/edujbarrios/text-to-music-prompt-structurer.git
cd text-to-music-prompt-structurer
python structurer.py "indie pop with acoustic guitar in d minor, sad and nostalgic, 120 bpm"
```

Example output:

```text
STYLE: Indie Pop
MOOD: Sad, Nostalgic
BPM: ~120
KEY: D Minor
INSTRUMENTS: Acoustic Guitar, Guitar
```

Requires Python 3.7 or later. No external packages are required.

## Usage

### Command line

Pass a musical description as a single quoted argument:

```bash
python structurer.py "latin trap at 90 bpm with 808 and hi-hats, dark mood, male vocals in Spanish"
```

The command prints only the fields detected in the description:

```text
STYLE: Latin Trap
MOOD: Dark
BPM: ~90
INSTRUMENTS: 808 Bass, Hi-hats
PRODUCTION: Dark tone
VOCALS: Male lead vocals
LANGUAGE: Spanish
```

### Python module

Use the engine and built-in formatter directly:

```python
from text_to_music_prompt_structurer import SunoPromptEngine, format_for_suno

engine = SunoPromptEngine()
prompt = engine.process("synthwave with 808, dark and dreamy, female vocals in English")

print(format_for_suno(prompt))
```

### Structured data

The engine returns a `SunoPrompt` model whose fields can be consumed by another formatter, interface, or text-to-music integration:

```python
from text_to_music_prompt_structurer import SunoPromptEngine

prompt = SunoPromptEngine().process(
    "jazz in c# minor with saxophone and piano, smooth and mysterious"
)

print(prompt.genre)
print(prompt.mood)
print(prompt.key)
print(prompt.instruments)
```

Available fields include:

- `genre` and `subgenre`
- `mood`
- `bpm` and `tempo`
- `key`
- `instruments`
- `production`
- `vocals`
- `language`

## How it works

The processing pipeline loads the JSON vocabularies in [`vocab/`](vocab), runs registered detection strategies against the input text, and returns a structured prompt model. The formatter then renders the detected fields as a compact text prompt.

```text
musical description
        ↓
vocabulary-based detectors
        ↓
structured prompt model
        ↓
Suno-compatible text output or a custom integration
```

## Vocabulary

The repository includes editable JSON vocabularies for:

- genres
- moods and energy
- tempo, rhythm, and structure
- musical keys and eras
- instruments
- production and mixing
- vocals and languages

To extend detection, add terms to the relevant file in [`vocab/`](vocab). Detector behavior can be extended in [`text_to_music_prompt_structurer/`](text_to_music_prompt_structurer).

## Project structure

```text
text-to-music-prompt-structurer/
├── structurer.py                         # Command-line entry point
├── example_module_usage.py               # Programmatic examples
├── text_to_music_prompt_structurer/      # Detection engine and data model
├── vocab/                                # JSON vocabularies
├── CONTRIBUTING.md
└── LICENSE
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on vocabulary additions and new detection strategies.

## License

Released under the [MIT License](LICENSE).

## Author

Created by **Eduardo J. Barrios**.

- [Website](https://edujbarrios.com)
- [GitHub profile](https://github.com/edujbarrios)
- [Project repository](https://github.com/edujbarrios/text-to-music-prompt-structurer)

> [!CAUTION]
> This is an unofficial tool and is not affiliated with, endorsed by, or connected to Suno AI.
