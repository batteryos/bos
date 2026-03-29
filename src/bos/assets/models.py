"""Assets domain dataclasses -- responses and requests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# ============================================================
# Response dataclasses (what the API returns)
# ============================================================


@dataclass
class Owner:
    """Asset owner."""

    slug: str
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> Owner:
        return cls(slug=data["slug"], name=data["name"])


@dataclass
class QSE:
    """Qualified Scheduling Entity."""

    slug: str
    name: str
    code: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> QSE:
        return cls(slug=data["slug"], name=data["name"], code=data.get("code"))


@dataclass
class Asset:
    """BESS asset.

    Note: owner and qse are flattened to name strings by the API.
    """

    slug: str
    name: str
    node: Optional[str]
    owner: Optional[str]
    qse: Optional[str]
    capacity: float
    duration: float
    category: str
    cod: Optional[str] = None
    iso: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    plant_code: Optional[str] = None
    inr: Optional[str] = None
    is_private: bool = True
    display: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Asset:
        return cls(
            slug=data["slug"],
            name=data["name"],
            node=data.get("node"),
            owner=data.get("owner"),
            qse=data.get("qse"),
            capacity=float(data.get("capacity", 0)),
            duration=float(data.get("duration", 0)),
            category=data.get("category", "standalone"),
            cod=data.get("cod"),
            iso=data.get("iso"),
            latitude=(
                float(data["latitude"]) if data.get("latitude") is not None else None
            ),
            longitude=(
                float(data["longitude"]) if data.get("longitude") is not None else None
            ),
            plant_code=data.get("plant_code"),
            inr=data.get("inr"),
            is_private=data.get("is_private", True),
            display=data.get("display", False),
        )


# ============================================================
# Request dataclasses (what you send)
# ============================================================


@dataclass
class AssetFilter:
    """Filter body for asset list and analytics POST endpoints.

    Used by: list_assets, get_revenue, get_volume, get_ranking,
    get_availability, get_performance, get_bos_index, get_hsl,
    get_cycles, and all other POST /{iso}/... endpoints.
    """

    owner_name: Optional[list[str] | str] = None
    node: Optional[list[str] | str] = None
    capacity: Optional[list[float] | float] = None
    duration: Optional[list[float] | float] = None
    category: Optional[str] = None
    status: Optional[list[str] | str] = None
    substatus: Optional[list[str] | str] = None
    qse_code: Optional[list[str] | str] = None
    qse_name: Optional[list[str] | str] = None
    hub: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    display: Optional[bool] = None
    is_private: Optional[bool] = None
    assets: Optional[list[str] | str] = None


@dataclass
class NewAsset:
    """POST /new/asset/ -- register a new BESS asset."""

    name: str
    iso: str
    node: str
    capacity: float
    duration: float
    category: str = "standalone"
    owner_name: Optional[str] = None
    qse_name: Optional[str] = None
    qse_code: Optional[str] = None
    cod: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    plant_code: Optional[str] = None
    inr: Optional[str] = None
    fips: Optional[str] = None


@dataclass
class NewResourceName:
    """POST /new/res_name/ -- register a new resource name."""

    asset_name: str
    resource_type_name: str
    asset_resource_name: str
    is_gen: bool = False
    is_load: bool = False
    is_bess: bool = True
    asset_resource_hash: Optional[str] = None
