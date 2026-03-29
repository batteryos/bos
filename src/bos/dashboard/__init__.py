"""BOS Dashboard domain -- pre-computed market dashboards."""

from bos.dashboard.client import DashboardClient
from bos.dashboard.models import DispatchEntry, RankingEntry, RevenueEntry

__all__ = [
    "DashboardClient",
    "DispatchEntry",
    "RankingEntry",
    "RevenueEntry",
]
