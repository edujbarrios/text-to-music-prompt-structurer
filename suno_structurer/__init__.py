"""
Suno Prompt Structurer - Package Initialization
Unstructured text → Structured Suno AI prompt

Author: Eduardo J. Barrios
Website: https://edujbarrios.com
GitHub: https://github.com/edujbarrios

UNOFFICIAL TOOL - Not affiliated with Suno AI
"""

__version__ = "1.0.0"
__author__ = "Eduardo J. Barrios"
__all__ = ["SunoPrompt", "SunoPromptEngine", "format_for_suno"]

# Core imports for package access
from suno_structurer.models import SunoPrompt
from suno_structurer.engine import SunoPromptEngine
from suno_structurer.formatter import format_for_suno
