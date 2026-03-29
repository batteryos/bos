"""Dashboard domain dataclasses -- responses only (no POST requests)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class RankingEntry:
    """Owner performance ranking entry."""

    date: str
    label: str
    value: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    rank: Optional[int] = None
    selected: bool = False
    owner: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> RankingEntry:
        return cls(
            date=data.get("date", ""),
            label=data.get("label", ""),
            value=float(data["value"]) if data.get("value") is not None else None,
            min=float(data["min"]) if data.get("min") is not None else None,
            max=float(data["max"]) if data.get("max") is not None else None,
            rank=int(data["rank"]) if data.get("rank") is not None else None,
            selected=data.get("selected", False),
            owner=data.get("owner"),
        )


@dataclass
class DispatchEntry:
    """Fleet dispatch entry."""

    timestamp: str
    charging: float
    discharging: float

    @classmethod
    def from_dict(cls, data: dict) -> DispatchEntry:
        return cls(
            timestamp=data.get("timestamp", ""),
            charging=float(data.get("charging", 0)),
            discharging=float(data.get("discharging", 0)),
        )


@dataclass
class RevenueEntry:
    """Revenue index entry."""

    date: str
    actual: float
    perfect: float

    @classmethod
    def from_dict(cls, data: dict) -> RevenueEntry:
        return cls(
            date=data.get("date", ""),
            actual=float(data.get("actual", 0)),
            perfect=float(data.get("perfect", 0)),
        )
