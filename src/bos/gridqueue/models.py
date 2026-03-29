"""Queue domain dataclasses -- responses and requests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# ============================================================
# Response dataclasses
# ============================================================


@dataclass
class Project:
    """Interconnection queue project."""

    inr: str
    entered_queue: Optional[str] = None
    iso: Optional[str] = None
    name: Optional[str] = None
    fuel: Optional[str] = None
    technology: Optional[str] = None
    interconnecting_entity: Optional[str] = None
    poi_location: Optional[str] = None
    county: Optional[str] = None
    cdr_reporting_zone: Optional[str] = None
    capacity: Optional[str] = None
    projected_cod: Optional[str] = None
    status: Optional[str] = None
    gim_study_phase: Optional[str] = None
    screening_study_started: Optional[str] = None
    screening_study_complete: Optional[str] = None
    fis_requested: Optional[str] = None
    fis_approved: Optional[str] = None
    construction_start: Optional[str] = None
    construction_end: Optional[str] = None
    ia_signed: Optional[str] = None
    comment: Optional[str] = None
    change_indicator: Optional[str] = None
    buses: Optional[list[dict]] = None

    @classmethod
    def from_dict(cls, data: dict) -> Project:
        return cls(
            inr=data["inr"],
            entered_queue=data.get("entered_queue"),
            iso=data.get("iso"),
            name=data.get("name"),
            fuel=data.get("fuel"),
            technology=data.get("technology"),
            interconnecting_entity=data.get("interconnecting_entity"),
            poi_location=data.get("poi_location"),
            county=data.get("county"),
            cdr_reporting_zone=data.get("cdr_reporting_zone"),
            capacity=data.get("capacity"),
            projected_cod=data.get("projected_cod"),
            status=data.get("status"),
            gim_study_phase=data.get("gim_study_phase"),
            screening_study_started=data.get("screening_study_started"),
            screening_study_complete=data.get("screening_study_complete"),
            fis_requested=data.get("fis_requested"),
            fis_approved=data.get("fis_approved"),
            construction_start=data.get("construction_start"),
            construction_end=data.get("construction_end"),
            ia_signed=data.get("ia_signed"),
            comment=data.get("comment"),
            change_indicator=data.get("change_indicator"),
            buses=data.get("buses"),
        )


@dataclass
class POI:
    """Point of Interconnection."""

    slug: str
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> POI:
        return cls(slug=data["slug"], name=data["name"])


@dataclass
class Bus:
    """Transmission bus."""

    slug: str
    name: Optional[str] = None
    number: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> Bus:
        return cls(
            slug=data["slug"],
            name=data.get("name"),
            number=int(data["number"]) if data.get("number") is not None else None,
        )


@dataclass
class POIBus:
    """POI-to-Bus mapping."""

    poi_location_slug: str
    poi_location_name: str
    bus_slug: str
    bus_name: Optional[str] = None
    bus_number: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> POIBus:
        return cls(
            poi_location_slug=data["poi_location_slug"],
            poi_location_name=data["poi_location_name"],
            bus_slug=data["bus_slug"],
            bus_name=data.get("bus_name"),
            bus_number=(
                int(data["bus_number"]) if data.get("bus_number") is not None else None
            ),
        )


# ============================================================
# Request dataclasses
# ============================================================


@dataclass
class BusCreate:
    """POST /add/bus/ -- add a new transmission bus."""

    bus_name: str
    bus_number: int


@dataclass
class BusUpdate:
    """POST /update/bus/ -- update an existing bus."""

    bus_slug: str
    bus_name: str
    bus_number: int


@dataclass
class POIBusCreate:
    """POST /add/poibus/ -- add a POI-to-bus mapping."""

    poi_location_slug: str
    bus_slug: str
