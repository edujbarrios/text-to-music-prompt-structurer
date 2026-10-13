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

# "no drums in the intro" and "chorus without drums" describe local
# arrangements, not a global ban in Suno's Exclude field. Only recognize
# explicit section names so unrelated "no drums in the mix" remains global.
_SECTIONS = (
    r"(?:intro|introduction|verse(?:\s+[1-9][0-9]?)?|chorus|"
    r"pre-chorus|post-chorus|bridge|outro|drop|breakdown|"
    r"estrofa(?:\s+[1-9][0-9]?)?|estribillo|puente|final)"
)
_SCOPE_AFTER = re.compile(
    rf"^\s+(?:in|during|for|on|en|durante|para)\s+"
    rf"(?:(?:the|el|la|los|las)\s+)?{_SECTIONS}(?!\w)",
    re.IGNORECASE,
)
_SCOPE_BEFORE = re.compile(
    rf"\b{_SECTIONS}\s+$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class NegativeConstraints:
    """Global exclusions, safe positive-detection input and scoped directions."""

    cleaned_description: str
    excludes: tuple[str, ...]
    style_description: str = ""
    scoped: tuple[str, ...] = ()


def extract_negative_constraints(description: str) -> NegativeConstraints:
    """Move only global negative constraints to Exclude.

    Scoped directions (e.g. 'no drums in the intro') are preserved as musical
    directions instead of turning into a global no-drums exclusion.
    Unknown negations remain verbatim and vocal toggles are handled elsewhere.
    """
    excludes: list[str] = []
    scoped: list[str] = []
    cleaned_parts: list[str] = []
    style_parts: list[str] = []
    last = 0

    for match in _NEGATION.finditer(description):
        start, stop = match.span()
        before = description[last:start]
        cleaned_parts.append(before)
        style_parts.append(before)

        after_section = _SCOPE_AFTER.match(description[stop:])
        before_section = _SCOPE_BEFORE.search(description[:start])
        if after_section or before_section:
            # Remove scoped negatives from positive instrument detection, but
            # retain them inside Style/section directions.
            scoped_text = description[
                start:stop + (after_section.end() if after_section else 0)
            ]
            scoped.append(scoped_text)
            style_parts.append(description[start:stop])
        else:
            canonical = _ALIASES[match.group(1).lower()]
            if canonical not in excludes:
                excludes.append(canonical)
            style_parts.append(" ")
        cleaned_parts.append(" ")
        last = stop

    cleaned_parts.append(description[last:])
    style_parts.append(description[last:])
    return NegativeConstraints(
        cleaned_description="".join(cleaned_parts),
        excludes=tuple(excludes),
        style_description="".join(style_parts),
        scoped=tuple(scoped),
    )


# SPDX-FileCopyrightText: 2026 Eduardo J. Barrios
# SPDX-License-Identifier: MPL-2.0
