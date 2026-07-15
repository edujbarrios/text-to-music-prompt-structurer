# Text-to-Music Prompt Structurer

[![PyPI](https://img.shields.io/pypi/v/text-to-music-prompt-structurer?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/text-to-music-prompt-structurer/)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-orange.svg?style=for-the-badge)](https://github.com/edujbarrios/text-to-music-prompt-structurer/blob/main/LICENSE)

Turn free-form musical ideas into structured prompts for text-to-music workflows.

The package detects genre, mood, BPM, key, instruments, production details, vocals, and language. It has no runtime dependencies and requires Python 3.10 or later.

## Install

```bash
python -m pip install text-to-music-prompt-structurer
```

## Command line

```bash
text-to-music-prompt "indie pop with acoustic guitar in d minor, sad and nostalgic, 120 bpm"
```

Output:

```text
STYLE: Indie Pop
MOOD: Sad, Nostalgic
BPM: ~120
KEY: D Minor
INSTRUMENTS: Acoustic Guitar, Guitar
```

## Python

```python
from text_to_music_prompt_structurer import MusicPromptEngine, format_prompt

prompt = MusicPromptEngine().process(
    "synthwave with 808, dark and dreamy, female vocals in English"
)

print(format_prompt(prompt))
```

The returned `MusicPrompt` object provides structured fields including `genre`, `subgenre`, `mood`, `bpm`, `tempo`, `key`, `instruments`, `production`, `vocals`, and `language`.

## Development

```bash
git clone https://github.com/edujbarrios/text-to-music-prompt-structurer.git
cd text-to-music-prompt-structurer
python -m pip install -e ".[dev]"
python -m pytest
ruff check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) to add vocabularies or detection strategies. Release history is available in [CHANGELOG.md](CHANGELOG.md).

## License

Copyright © 2026 Eduardo J. Barrios.

This project is licensed under the [Mozilla Public License 2.0](LICENSE). MPL 2.0 is a file-level copyleft license: modifications to covered source files must remain available under MPL 2.0, while those files may be combined with code under other licenses. See [NOTICE](NOTICE) for attribution details.

> [!NOTE]
> This is an unofficial tool and is not affiliated with, endorsed by, or connected to Suno AI.
