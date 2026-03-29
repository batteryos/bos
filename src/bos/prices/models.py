"""Prices domain dataclasses -- responses and constants."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

ERCOT_HUBS = [
    "HB_BUSAVG",
    "HB_HOUSTON",
    "HB_HUBAVG",
    "HB_NORTH",
    "HB_PAN",
    "HB_SOUTH",
    "HB_WEST",
]

HUB_CONTRACT_MAP = {
    "HB_NORTH": {
        "peak": "ERN",
        "2x16": "ER2",
        "7x8": "ECI",
        "he1017": "ED7",
        "he1822": "ERC",
    },
    "HB_HOUSTON": {
        "peak": "ERH",
        "2x16": "EDB",
        "7x8": "ECJ",
        "he1017": "ERM",
        "he1822": "ERB",
    },
    "HB_SOUTH": {
        "peak": "ERS",
        "2x16": "EDA",
        "7x8": "ECK",
        "he1017": "ERQ",
        "he1822": "ERD",
    },
    "HB_WEST": {
        "peak": "ERW",
        "2x16": "EDC",
        "7x8": "ECL",
        "he1017": "ERT",
        "he1822": "ERE",
    },
}

SHAPES = ["peak", "2x16", "7x8", "he1017", "he1822"]


@dataclass
class Exchange:
    """Exchange metadata from the Kronos API."""

    mic: str
    name: str
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> Exchange:
        return cls(
            mic=data.get("mic", ""),
            name=data.get("name", ""),
            url=data.get("url"),
        )


@dataclass
class Contract:
    """Contract metadata from the Kronos API."""

    symbol: str
    hub: Optional[str] = None
    shape: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    iso: Optional[str] = None
    fo_type: Optional[str] = None
    phys_type: Optional[str] = None
    dart_mode: Optional[str] = None
    settlement: Optional[str] = None

    @property
    def node(self) -> Optional[str]:
        """Alias for hub (Kronos API returns 'node')."""
        return self.hub

    @classmethod
    def from_dict(cls, data: dict) -> Contract:
        return cls(
            symbol=data.get("symbol", ""),
            hub=data.get("node") or data.get("hub"),
            shape=data.get("shape"),
            name=data.get("name"),
            url=data.get("url"),
            iso=data.get("iso"),
            fo_type=data.get("fo_type"),
            phys_type=data.get("phys_type"),
            dart_mode=data.get("dart_mode"),
            settlement=data.get("settlement"),
        )


@dataclass
class AvailableDate:
    """Available date range for a contract."""

    refdate: str
    min_fordate: str
    max_fordate: str

    @classmethod
    def from_dict(cls, data: dict) -> AvailableDate:
        return cls(
            refdate=str(data.get("refdate", "")),
            min_fordate=str(data.get("min_fordate", "")),
            max_fordate=str(data.get("max_fordate", "")),
        )


@dataclass
class ContractPrice:
    """Contract price record from the Kronos API."""

    exchange: str
    symbol: str
    refdate: str
    fordate: str
    price: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    open_interest: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> ContractPrice:
        return cls(
            exchange=data.get("exchange", ""),
            symbol=data.get("symbol", ""),
            refdate=str(data.get("refdate", "")),
            fordate=str(data.get("fordate", "")),
            price=float(data["price"]) if data.get("price") is not None else None,
            open=float(data["open"]) if data.get("open") is not None else None,
            high=float(data["high"]) if data.get("high") is not None else None,
            low=float(data["low"]) if data.get("low") is not None else None,
            close=float(data["close"]) if data.get("close") is not None else None,
            volume=int(data["volume"]) if data.get("volume") is not None else None,
            open_interest=(
                int(data["open_interest"])
                if data.get("open_interest") is not None
                else None
            ),
        )


@dataclass
class Settlement:
    """Contract settlement for a specific refdate."""

    symbol: str
    refdate: str
    price: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict) -> Settlement:
        return cls(
            symbol=data.get("symbol", ""),
            refdate=data.get("refdate", ""),
            price=float(data["price"]) if data.get("price") is not None else None,
        )


@dataclass
class Hub:
    """ERCOT pricing hub with contract symbol mapping."""

    name: str
    contracts: Optional[dict[str, str]] = None

    @classmethod
    def from_name(cls, name: str) -> Hub:
        return cls(name=name, contracts=HUB_CONTRACT_MAP.get(name))
