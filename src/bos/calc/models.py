"""Calc domain dataclasses -- responses and requests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

# ============================================================
# Response dataclasses
# ============================================================


@dataclass
class CalcStatus:
    """Calc execution status."""

    slug: str
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> CalcStatus:
        if isinstance(data, str):
            return cls(slug=data, name=data)
        return cls(slug=data.get("slug", ""), name=data.get("name", ""))


@dataclass
class Calc:
    """Calculation object. Contains nodes x scenarios = node-scenarios."""

    slug: str
    name: str
    iso: str
    node: str
    capacity: float
    duration: float
    status: Optional[str] = None
    description: Optional[str] = None
    is_favorite: bool = False
    is_public: bool = False
    tags: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Calc:
        status = data.get("status")
        if isinstance(status, dict):
            status = status.get("slug") or status.get("name")
        return cls(
            slug=data["slug"],
            name=data.get("name", ""),
            iso=data.get("iso", ""),
            node=data.get("node", ""),
            capacity=float(data.get("capacity", 1)),
            duration=float(data.get("duration", 1)),
            status=status,
            description=data.get("description"),
            is_favorite=data.get("is_favorite", False),
            is_public=data.get("is_public", False),
            tags=data.get("tags"),
        )


@dataclass
class CalcNode:
    """Pricing node within a calc."""

    slug: str
    calc_slug: str
    node: str

    @classmethod
    def from_dict(cls, data: dict) -> CalcNode:
        calc_slug = data.get("calc_slug", "")
        if not calc_slug and "calc" in data:
            calc_slug = (
                data["calc"] if isinstance(data["calc"], str) else str(data["calc"])
            )
        return cls(slug=data["slug"], calc_slug=calc_slug, node=data["node"])


@dataclass
class CalcScenario:
    """Battery parameter scenario."""

    slug: str
    calc_slug: str
    name: str
    params: Optional[list[dict[str, Any]]] = None

    @classmethod
    def from_dict(cls, data: dict) -> CalcScenario:
        calc_slug = data.get("calc_slug", "")
        if not calc_slug and "calc" in data:
            calc_slug = (
                data["calc"] if isinstance(data["calc"], str) else str(data["calc"])
            )
        return cls(
            slug=data["slug"],
            calc_slug=calc_slug,
            name=data.get("name", ""),
            params=data.get("params"),
        )


@dataclass
class NodeScenario:
    """Node x Scenario dispatch result pair."""

    slug: str
    node_slug: str
    scenario_slug: str
    dragon_slug: Optional[str] = None
    status: Optional[str] = None
    exchange: Optional[str] = None
    refdate: Optional[str] = None
    backcast_startdate: Optional[str] = None
    backcast_enddate: Optional[str] = None
    forecast_startdate: Optional[str] = None
    forecast_enddate: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> NodeScenario:
        node = data.get("node_slug", "")
        if not node and "node" in data:
            node = data["node"] if isinstance(data["node"], str) else str(data["node"])
        scenario = data.get("scenario_slug", "")
        if not scenario and "scenario" in data:
            scenario = (
                data["scenario"]
                if isinstance(data["scenario"], str)
                else str(data["scenario"])
            )
        status = data.get("status")
        if isinstance(status, dict):
            status = status.get("slug") or status.get("name")
        return cls(
            slug=data["slug"],
            node_slug=node,
            scenario_slug=scenario,
            dragon_slug=data.get("dragon_slug"),
            status=status,
            exchange=data.get("exchange"),
            refdate=data.get("refdate"),
            backcast_startdate=data.get("backcast_startdate"),
            backcast_enddate=data.get("backcast_enddate"),
            forecast_startdate=data.get("forecast_startdate"),
            forecast_enddate=data.get("forecast_enddate"),
        )


@dataclass
class DataObject:
    """Saved data/analysis reference."""

    slug: str
    name: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> DataObject:
        return cls(
            slug=data["slug"],
            name=data.get("name"),
            description=data.get("description"),
        )


@dataclass
class Exchange:
    """Futures exchange (ICE, CME)."""

    iso: str
    mic: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Exchange:
        return cls(iso=data.get("iso", ""), mic=data.get("mic"), name=data.get("name"))


# ============================================================
# Request dataclasses
# ============================================================


@dataclass
class CalcCreate:
    """POST /calc/ -- create a new dispatch calculation."""

    name: str
    iso: str = "ERCOT"
    node: str = "HB_HOUSTON"
    capacity: float = 100.0
    duration: float = 2.0
    description: Optional[str] = None
    is_public: bool = False


@dataclass
class DataObjectCreate:
    """POST /data/ -- create a data object."""

    name: str
    description: Optional[str] = None


@dataclass
class MultichartParams:
    """POST /stack/{slug}/multichart/ -- multi-chart visualization."""

    chart_type: Optional[str] = None
    period: Optional[str] = None
    aggregation: Optional[str] = None
