"""Dashboard API client -- pre-computed market dashboards."""

from bos.base import BaseClient
from bos.dashboard.models import DispatchEntry, RankingEntry, RevenueEntry


class DashboardClient(BaseClient):
    """Client for /api/v1/bridge endpoints. All GET, no required params."""

    def get_ranking(self, **params):
        """GET /ranking/ -- Asset performance rankings."""
        data = self.get("/ranking/", params=params or None)
        results = data.get("results", data) if isinstance(data, dict) else data
        return [RankingEntry.from_dict(r) for r in results]

    def get_dispatch(self, **params):
        """GET /dispatch/ -- Fleet dispatch summary."""
        data = self.get("/dispatch/", params=params or None)
        results = data.get("results", data) if isinstance(data, dict) else data
        return [DispatchEntry.from_dict(r) for r in results]

    def get_revenue(self, **params):
        """GET /revenue/ -- Revenue summary."""
        data = self.get("/revenue/", params=params or None)
        results = data.get("results", data) if isinstance(data, dict) else data
        return [RevenueEntry.from_dict(r) for r in results]

    def get_tbn_ercot(self, **params):
        """GET /tbn_ercot/ -- TBn spreads for ERCOT hubs."""
        return self.get("/tbn_ercot/", params=params or None)

    def get_tbn_us(self, **params):
        """GET /tbn_us/ -- TBn spreads across US ISOs."""
        return self.get("/tbn_us/", params=params or None)

    def get_data_key(self):
        """GET /data/ -- Dashboard data key."""
        return self.get("/data/")

    def get_queue_capacity(self):
        """GET /queue_capacity/ -- Queue capacity by fuel type and stage."""
        data = self.get("/queue_capacity/")
        return data.get("results", data) if isinstance(data, dict) else data
