"""
Text-to-Music Prompt Structurer - Package Initialization
Unstructured text → Structured Suno AI prompt

Author: Eduardo J. Barrios
Website: https://edujbarrios.com
GitHub: https://github.com/edujbarrios

UNOFFICIAL TOOL - Not affiliated with Suno AI
"""

from importlib.metadata import version

__version__ = version("text-to-music-prompt-structurer")
__author__ = "Eduardo J. Barrios"
__all__ = [
    "MusicPrompt",
    "MusicPromptEngine",
    "format_prompt",
    "SunoPrompt",
    "SunoPromptEngine",
    "format_for_suno",
    "SunoFields",
    "SunoSection",
    "build_suno_prompt",
    "render_suno_prompt",
    "validate_suno_prompt",
    "PromptIssue",
    "extract_negative_constraints",
    "NegativeConstraints",
]

# Core imports for package access
from text_to_music_prompt_structurer.engine import MusicPromptEngine, SunoPromptEngine
from text_to_music_prompt_structurer.exclusions import (
    NegativeConstraints,
    extract_negative_constraints,
)
from text_to_music_prompt_structurer.formatter import format_for_suno, format_prompt
from text_to_music_prompt_structurer.models import MusicPrompt, SunoPrompt
from text_to_music_prompt_structurer.suno import (
    PromptIssue,
    SunoFields,
    SunoSection,
    build_suno_prompt,
    render_suno_prompt,
    validate_suno_prompt,
)
# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
