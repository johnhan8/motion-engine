from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ClassificationResult:
    label: Optional[str]
    scores: Dict[str, float]
    confidence: Optional[float]
    strategy_id: str
    raw: Optional[Dict[str, Any]] = None
