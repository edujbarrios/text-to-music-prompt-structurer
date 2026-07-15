"""
Text-to-Music Prompt Structurer - Strategy Registry
"""

from text_to_music_prompt_structurer.models import MusicPrompt


class DetectorRegistry:
    """Registry for detector strategies."""

    def __init__(self):
        self.detectors = []

    def register(self, detector):
        """Register a new detector."""
        self.detectors.append(detector)

    def run(self, text: str, prompt: MusicPrompt):
        """Run all registered detectors on the input text."""
        for detector in self.detectors:
            detector.detect(text, prompt)
