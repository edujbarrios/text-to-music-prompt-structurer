#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0

"""
Example: Using Text-to-Music Prompt Structurer as a Python Module

This demonstrates how to use the tool programmatically in your own scripts.
"""

from text_to_music_prompt_structurer import MusicPromptEngine, format_prompt


def main():
    # Create the engine
    engine = MusicPromptEngine()

    # Example 1: Basic usage
    print("=" * 50)
    print("Example 1: Indie Pop")
    print("=" * 50)
    prompt1 = engine.process("indie pop with acoustic guitar, sad and nostalgic, 120 bpm")
    print(format_prompt(prompt1))

    # Example 2: Access structured data
    print("\n" + "=" * 50)
    print("Example 2: Structured Data Access")
    print("=" * 50)
    prompt2 = engine.process("synthwave with 808, dark and dreamy, female vocals in english")
    print(f"Genre: {prompt2.genre}")
    print(f"Moods: {', '.join(prompt2.mood)}")
    print(f"Instruments: {', '.join(prompt2.instruments)}")
    print(f"Language: {prompt2.language}")

    # Example 3: Latin Trap
    print("\n" + "=" * 50)
    print("Example 3: Latin Trap")
    print("=" * 50)
    prompt3 = engine.process(
        "latin trap 90 bpm with 808 and hi-hats, dark mood, male vocals in spanish"
    )
    print(format_prompt(prompt3))

    # Example 4: Check BPM detection
    print("\n" + "=" * 50)
    print("Example 4: BPM Detection")
    print("=" * 50)
    prompt4 = engine.process("electronic music 128 bpm")
    print(f"Detected BPM: {prompt4.bpm}")


if __name__ == "__main__":
    main()
