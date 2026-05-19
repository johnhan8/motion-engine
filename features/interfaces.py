"""Preparatory contracts for the feature extraction layer (no extraction logic yet)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class MotionState:
    """Carrier for motion context fed into feature extraction.

    Fields will be defined when ticks/windows are modeled; intentionally empty placeholder.
    """


@dataclass(frozen=True, slots=True)
class FeatureVector:
    """Structured output of feature extraction.

    Contents TBD; placeholder for architecture wiring only.
    """


@runtime_checkable
class FeatureExtractionLayer(Protocol):
    """Transform motion state into a feature vector (implementation deferred)."""

    def extract(self, state: MotionState) -> FeatureVector:
        ...
