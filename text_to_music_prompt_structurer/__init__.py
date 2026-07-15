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
]

# Core imports for package access
from text_to_music_prompt_structurer.engine import MusicPromptEngine, SunoPromptEngine
from text_to_music_prompt_structurer.formatter import format_for_suno, format_prompt
from text_to_music_prompt_structurer.models import MusicPrompt, SunoPrompt
