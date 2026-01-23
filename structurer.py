#!/usr/bin/env python3

"""
Suno Prompt Structurer
Convert unstructured musical ideas into structured Suno AI prompts

Author: Eduardo J. Barrios
Website: https://edujbarrios.com
GitHub: https://github.com/edujbarrios

UNOFFICIAL TOOL - Not affiliated with Suno AI
"""

import sys
from suno_structurer.engine import SunoPromptEngine
from suno_structurer.formatter import format_for_suno


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print("Usage: python suno.py \"your musical idea here\"")
        print("\nExample:")
        print('  python suno.py "indie pop with acoustic guitar, sad and nostalgic, 120 bpm"')
        sys.exit(1)
    
    # Process the input
    engine = SunoPromptEngine()
    prompt = engine.process(" ".join(sys.argv[1:]))
    
    # Display the result
    print(format_for_suno(prompt))


if __name__ == "__main__":
    main()
