"""Assets API client -- BESS asset data, revenue, volume, analytics."""

from bos.base import BaseClient
from bos.assets.models import Asset, Owner, QSE


class AssetsClient(BaseClient):
    """Client for /api/v1/asset endpoints. 30 endpoints.

    POST methods take a typed request dataclass as the first arg::

        from bos.assets.models import AssetFilter
        client.assets.list_assets(AssetFilter(owner_name=["Vistra"], duration=[2]))
    """

    # --- Asset list & detail ---

    def list_assets(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/ -- List all assets in ISO."""
        data = self.post(f"/{iso}/", self.serialize(filters, kwargs))
        if isinstance(data, list):
            return [Asset.from_dict(d) for d in data]
        return data

    def get_asset(self, iso, asset_slug):
        """GET /{iso}/{asset_slug}/ -- Single asset detail."""
        return self.get(f"/{iso}/{asset_slug}/")

    def get_asset_timeline(self, iso, asset_slug):
        """GET /{iso}/{asset_slug}/timeline/ -- Asset event timeline."""
        return self.get(f"/{iso}/{asset_slug}/timeline/")

    def list_owners(self, iso="ercot"):
        """GET /{iso}/owners/ -- List asset owners."""
        data = self.get(f"/{iso}/owners/")
        if isinstance(data, list):
            return [Owner.from_dict(d) for d in data]
        return data

    def list_qses(self, iso="ercot"):
        """GET /{iso}/qse/ -- List QSEs."""
        data = self.get(f"/{iso}/qse/")
        if isinstance(data, list):
            return [QSE.from_dict(d) for d in data]
        return data

    # --- Revenue ---

    def get_revenue(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/revenue/ -- Actual revenue, all assets."""
        return self.post(f"/{iso}/revenue/", self.serialize(filters, kwargs))

    def get_perfect_revenue(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/revenue/perfect/ -- CO perfect dispatch revenue."""
        return self.post(f"/{iso}/revenue/perfect/", self.serialize(filters, kwargs))

    def get_eo_perfect_revenue(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/revenue/perfect/eo/ -- EO perfect dispatch revenue."""
        return self.post(f"/{iso}/revenue/perfect/eo/", self.serialize(filters, kwargs))

    # --- Volume ---

    def get_volume(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/volume/ -- Actual volume, all assets."""
        return self.post(f"/{iso}/volume/", self.serialize(filters, kwargs))

    def get_perfect_volume(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/volume/perfect/ -- CO perfect dispatch volume."""
        return self.post(f"/{iso}/volume/perfect/", self.serialize(filters, kwargs))

    def get_eo_perfect_volume(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/volume/perfect/eo/ -- EO perfect dispatch volume."""
        return self.post(f"/{iso}/volume/perfect/eo/", self.serialize(filters, kwargs))

    def download_volume(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/volume/dl/ -- Volume download (all assets)."""
        return self.post(f"/{iso}/volume/dl/", self.serialize(filters, kwargs))

    def get_dispatch_volume(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/volume/dispatch/ -- Dispatch volume."""
        return self.post(f"/{iso}/volume/dispatch/", self.serialize(filters, kwargs))

    def download_asset_volume(self, iso, asset_slug, filters=None, **kwargs):
        """POST /{iso}/{asset_slug}/volume/dl/ -- Per-asset volume download."""
        return self.post(
            f"/{iso}/{asset_slug}/volume/dl/", self.serialize(filters, kwargs)
        )

    def download_resource_volume(
        self, iso, asset_slug, component_slug, resource_slug, filters=None, **kwargs
    ):
        """POST /{iso}/asset/{a}/component/{c}/resource/{r}/volume/dl/"""
        path = (
            f"/{iso}/asset/{asset_slug}/component/{component_slug}"
            f"/resource/{resource_slug}/volume/dl/"
        )
        return self.post(path, self.serialize(filters, kwargs))

    # --- Analytics ---

    def get_bos_index(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/bosindex/ -- BOS Index."""
        return self.post(f"/{iso}/bosindex/", self.serialize(filters, kwargs))

    def get_perfect_bos_index(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/bosindex/perfect/ -- Perfect BOS Index."""
        return self.post(f"/{iso}/bosindex/perfect/", self.serialize(filters, kwargs))

    def get_availability(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/availability/ -- Availability/outage status."""
        return self.post(f"/{iso}/availability/", self.serialize(filters, kwargs))

    def get_performance(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/performance/ -- Performance metrics."""
        return self.post(f"/{iso}/performance/", self.serialize(filters, kwargs))

    def get_percentiles(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/percentiles/ -- Nth percentile analysis."""
        return self.post(f"/{iso}/percentiles/", self.serialize(filters, kwargs))

    def get_ranking(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/ranking/ -- Asset rankings."""
        return self.post(f"/{iso}/ranking/", self.serialize(filters, kwargs))

    def get_hsl(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/hsl/ -- HSL data, all assets."""
        return self.post(f"/{iso}/hsl/", self.serialize(filters, kwargs))

    def get_asset_hsl(self, iso, asset_slug, filters=None, **kwargs):
        """POST /{iso}/{asset_slug}/hsl/ -- HSL for single asset."""
        return self.post(f"/{iso}/{asset_slug}/hsl/", self.serialize(filters, kwargs))

    def get_cycles(self, filters=None, iso="ercot", **kwargs):
        """POST /{iso}/cycles/ -- Battery cycle count data."""
        return self.post(f"/{iso}/cycles/", self.serialize(filters, kwargs))

    # --- Admin ---

    def dump_fixtures(self, **kwargs):
        """POST /fixtures/ -- Dump fixture data."""
        return self.post("/fixtures/", self.serialize(None, kwargs))

    def add_asset(self, asset=None, **kwargs):
        """POST /new/asset/ -- Register new asset."""
        return self.post("/new/asset/", self.serialize(asset, kwargs))

    def add_resource_name(self, resource=None, **kwargs):
        """POST /new/res_name/ -- Register new resource name."""
        return self.post("/new/res_name/", self.serialize(resource, kwargs))

    def toggle_analysis_favorite(self, slug):
        """GET /analysis/{slug}/toggle_favorite_status/ -- Toggle favorite."""
        return self.get(f"/analysis/{slug}/toggle_favorite_status/")
