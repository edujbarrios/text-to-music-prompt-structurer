"""Conservative negative-constraint extraction for Suno's Exclude field.

Only known musical elements are recognized. Unknown creative wording remains in
the original description rather than being reinterpreted as an exclusion.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Canonical names for a short, unambiguous set of negated concepts.
# Keep this allowlist small: "no strings attached" is not a request to
# exclude string instruments, and "without you" is not an audio exclusion.
_ALIASES = {
    "autotune": "Autotune",
    "auto-tune": "Autotune",
    "pitch correction": "Pitch correction",
    "drums": "Drums",
    "drum kit": "Drums",
    "batería": "Drums",
    "bateria": "Drums",
    "percussion": "Percussion",
    "percusión": "Percussion",
    "percusion": "Percussion",
    "guitar": "Guitar",
    "guitars": "Guitar",
    "guitarra": "Guitar",
    "electric guitar": "Electric guitar",
    "guitarra eléctrica": "Electric guitar",
    "guitarra electrica": "Electric guitar",
    "acoustic guitar": "Acoustic guitar",
    "piano": "Piano",
    "synth": "Synths",
    "synths": "Synths",
    "synthesizers": "Synths",
    "sintetizadores": "Synths",
    "distortion": "Distortion",
    "distorsión": "Distortion",
    "reverb": "Reverb",
    "choir": "Choir",
    "coro": "Choir",
    "vocoder": "Vocoder",
    "rap": "Rap",
    "backing vocals": "Backing vocals",
    "coros": "Backing vocals",
}
_PREFIX = r"(?<!\w)(?:no|without|sin|avoid|exclude)\s+"
_TOKENS = "|".join(re.escape(x) for x in sorted(_ALIASES, key=len, reverse=True))
_NEGATION = re.compile(rf"{_PREFIX}({_TOKENS})(?!\w)", re.IGNORECASE)

# Section-local negatives must remain in the description: excluding them
# globally would contradict a later chorus or bridge that includes the instrument.
_SECTION_WORD = (
    r"(?:intro|introduction|verse|verso|estrofa|chorus|estribillo|"
    r"bridge|puente|outro|breakdown|pre-chorus|post-chorus|solo|drop|"
    r"hook|refrain|interlude|coda)"
)
_LOCAL_AFTER = re.compile(
    rf"^\s*(?:(?:only\s+)?(?:in|during|throughout|for|on|until|"
    rf"before|after|en|durante|hasta|antes\s+de|después\s+de|despues\s+de))"
    rf"\s+(?:(?:the|a|el|la|los|las)\s+)?{_SECTION_WORD}\b",
    re.IGNORECASE,
)
_LOCAL_BEFORE = re.compile(
    rf"\b{_SECTION_WORD}(?:\s+[1-9][0-9]?)?"
    rf"(?:\s+(?:is|has|goes|stays|está|esta))?\s*$",
    re.IGNORECASE,
)


def _is_section_local(description: str, match: re.Match[str]) -> bool:
    """Keep section-scoped negatives out of the global Exclude setting."""
    after = description[match.end():match.end() + 85]
    before = description[max(0, match.start() - 85):match.start()]
    return bool(_LOCAL_AFTER.match(after) or _LOCAL_BEFORE.search(before))


@dataclass(frozen=True)
class NegativeConstraints:
    """Parsed exclusions and source cleaned for musical-feature detection."""

    cleaned_description: str
    excludes: tuple[str, ...]
    detection_description: str = ""


def extract_negative_constraints(description: str) -> NegativeConstraints:
    """Separate explicit `no drums` / `sin batería` style exclusions.

    Unrecognized negations are retained. Vocal exclusions such as `no vocals`
    are handled by the existing instrumental toggle rather than this parser.
    """
    excludes: list[str] = []

    def substitute(match: re.Match[str]) -> str:
        if _is_section_local(description, match):
            return match.group(0)
        canonical = _ALIASES[match.group(1).lower()]
        if canonical not in excludes:
            excludes.append(canonical)
        return " "

    cleaned = _NEGATION.sub(substitute, description)
    detection = _NEGATION.sub(" ", description)
    return NegativeConstraints(
        cleaned_description=cleaned,
        excludes=tuple(excludes),
        detection_description=detection,
    )


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
