"""
Suno Prompt Structurer - Strategy Registry
"""

from suno_structurer.models import SunoPrompt


class DetectorRegistry:
    """Registry for detector strategies."""
    
    def __init__(self):
        self.detectors = []

    def register(self, detector):
        """Register a new detector."""
        self.detectors.append(detector)

    def run(self, text: str, prompt: SunoPrompt):
        """Run all registered detectors on the input text."""
        for detector in self.detectors:
            detector.detect(text, prompt)
