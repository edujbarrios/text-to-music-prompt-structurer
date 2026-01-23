# Suno Prompt Structurer

Convert unstructured musical ideas into structured [Suno AI](https://suno.ai) prompts.

> [!NOTE]
> The quality of [Suno AI](https://suno.ai) output depends heavily on the quality of the prompt. This simple tool helps structure your ideas into clear, effective prompts.

---

## Quick Start

```bash
python structurer.py "indie pop with acoustic guitar, sad and nostalgic, 120 bpm"
```

Output:
```
STYLE: Indie Pop
MOOD: Sad, Nostalgic
TEMPO: ~120 BPM
INSTRUMENTS: Acoustic Guitar
```

---

## Installation

```bash
git clone https://github.com/edujbarrios/suno-prompt-structurer.git
cd suno-prompt-structurer
python structurer.py "your musical idea here"
```

Requirements: Python 3.7+ (no external dependencies)

---

## Usage

### Command-Line Tool

```bash
python structurer.py "your musical idea here"
```

### Python Module

```python
from suno_structurer import SunoPromptEngine, format_for_suno

engine = SunoPromptEngine()
prompt = engine.process("indie pop with acoustic guitar, sad, 120 bpm")
print(format_for_suno(prompt))
```

Output:
```
STYLE: Indie Pop
MOOD: Sad
TEMPO: ~120 BPM
INSTRUMENTS: Acoustic Guitar
```

### Programmatic Access

```python
from suno_structurer import SunoPromptEngine

engine = SunoPromptEngine()
prompt = engine.process("synthwave with 808, dark and dreamy")

print(f"Genre: {prompt.genre}")
print(f"Moods: {', '.join(prompt.mood)}")
print(f"Instruments: {', '.join(prompt.instruments)}")
```

---

## Examples

**Latin Trap:**
```bash
python structurer.py "latin trap 90 bpm with 808 and hi-hats, dark mood, male vocals in spanish"
```
```
STYLE: Latin Trap
MOOD: Dark
TEMPO: ~90 BPM
INSTRUMENTS: 808 Bass, Hi-hats
LANGUAGE: Spanish
```

**Chill Electronic:**
```bash
python structurer.py "chill electronic music with lofi texture, piano and synths, dreamy"
```
```
STYLE: Electronic
MOOD: Chill, Dreamy
INSTRUMENTS: Piano, Synths
PRODUCTION: Lo-fi texture
```

---
## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)


### Extending

Add new genres, moods, or instruments by editing JSON files in `vocab/`:

```json
{
  "your-genre": { "genre": "Your Genre", "subgenre": null }
}
```
and any other `/vocab` json file!
---

## License

MIT License - See [LICENSE](LICENSE)

---

## Author

**Eduardo J. Barrios**
- Website: [edujbarrios.com](https://edujbarrios.com)
- GitHub: [github.com/edujbarrios](https://github.com/edujbarrios)
- Repository: [suno-prompt-structurer](https://github.com/edujbarrios/suno-prompt-structurer)

---

> [!CAUTION]
> **DISCLAIMER:** This is an unofficial tool and is not affiliated with, endorsed by, or connected to [Suno AI](https://suno.ai) in any way.

