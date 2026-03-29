"""Exhaustive examples for every AssetsClient endpoint and parameter config.

30 endpoints. Covers every distinct (method, parameter shape) combination:
  GET  with iso default, GET with iso+slug, GET with slug action
  POST bare, POST with AssetFilter dataclass, POST with kwargs escape hatch
  POST with NewAsset/NewResourceName dataclass, POST with nested slugs

Usage:
    export BOS_API=your-token
    python -m bos.assets.examples
"""

from bos import BOSClient
from bos.assets.models import AssetFilter, NewAsset, NewResourceName

client = BOSClient()
a = client.assets


# ============================================================
# GET — iso only (default "ercot")
# ============================================================

owners = a.list_owners()
owners_explicit = a.list_owners(iso="ercot")
qses = a.list_qses()


# ============================================================
# GET — iso + asset_slug
# ============================================================

detail = a.get_asset("ercot", "ASSET_SLUG")
timeline = a.get_asset_timeline("ercot", "ASSET_SLUG")


# ============================================================
# GET — slug action
# ============================================================

a.toggle_analysis_favorite("ANALYSIS_SLUG")


# ============================================================
# POST — bare (no body)
# ============================================================

assets_bare = a.list_assets()
rev_bare = a.get_revenue()
vol_bare = a.get_volume()
idx_bare = a.get_bos_index()
cyc_bare = a.get_cycles()


# ============================================================
# POST — with AssetFilter dataclass (typed path)
# ============================================================

assets_typed = a.list_assets(AssetFilter(owner_name=["Vistra"], duration=[2]))
rev_typed = a.get_revenue(AssetFilter(category="standalone"))
vol_typed = a.get_volume(AssetFilter(owner_name="Vistra"))
rank_typed = a.get_ranking(AssetFilter(owner_name="Vistra", category="standalone"))
perf_typed = a.get_performance(AssetFilter(duration=[2, 4]))
avail_typed = a.get_availability(AssetFilter(hub="HB_HOUSTON"))
hsl_typed = a.get_hsl(AssetFilter(category="standalone"))
pct_typed = a.get_percentiles(AssetFilter(owner_name="Vistra"))


# ============================================================
# POST — with kwargs escape hatch (undocumented params)
# ============================================================

assets_kw = a.list_assets(owner_name="Vistra", category="standalone")
rev_kw = a.get_revenue(iso="ercot", owner_name="Vistra")
assets_mixed = a.list_assets(AssetFilter(owner_name="Vistra"), new_api_param=True)


# ============================================================
# POST — all 3 revenue variants
# ============================================================

rev = a.get_revenue()
rev_co = a.get_perfect_revenue()
rev_co_filtered = a.get_perfect_revenue(AssetFilter(category="standalone"))
rev_eo = a.get_eo_perfect_revenue()
rev_eo_filtered = a.get_eo_perfect_revenue(AssetFilter(duration=[2]))


# ============================================================
# POST — all 7 volume endpoints
# ============================================================

vol = a.get_volume()
vol_co = a.get_perfect_volume()
vol_co_filtered = a.get_perfect_volume(AssetFilter(category="colocated"))
vol_eo = a.get_eo_perfect_volume()
vol_dl = a.download_volume()
vol_dl_filtered = a.download_volume(AssetFilter(owner_name="Vistra"))
vol_dispatch = a.get_dispatch_volume()
vol_dispatch_filtered = a.get_dispatch_volume(AssetFilter(category="standalone"))


# ============================================================
# POST — all 9 analytics endpoints
# ============================================================

idx = a.get_bos_index()
idx_co = a.get_perfect_bos_index()
avail = a.get_availability()
perf = a.get_performance()
pct = a.get_percentiles()
rank = a.get_ranking()
hsl = a.get_hsl()
asset_hsl = a.get_asset_hsl("ercot", "ASSET_SLUG")
cyc = a.get_cycles()


# ============================================================
# POST — iso + asset_slug
# ============================================================

asset_vol = a.download_asset_volume("ercot", "ASSET_SLUG")
asset_vol_f = a.download_asset_volume(
    "ercot", "ASSET_SLUG", AssetFilter(category="standalone")
)
asset_hsl_f = a.get_asset_hsl("ercot", "ASSET_SLUG", AssetFilter(category="standalone"))


# ============================================================
# POST — iso + 3 nested slugs (deepest nesting)
# ============================================================

res_vol = a.download_resource_volume("ercot", "ASSET_SLUG", "COMP_SLUG", "RES_SLUG")


# ============================================================
# POST — admin with NewAsset / NewResourceName dataclass
# ============================================================

fixtures = a.dump_fixtures()

new = a.add_asset(
    NewAsset(
        name="New Battery",
        iso="ercot",
        node="HB_HOUSTON",
        capacity=100.0,
        duration=2.0,
    )
)

new_full = a.add_asset(
    NewAsset(
        name="Full Battery",
        iso="ercot",
        node="HB_HOUSTON",
        capacity=200.0,
        duration=4.0,
        category="colocated",
        owner_name="Vistra",
        cod="2025-06-01",
        latitude=30.0,
        longitude=-95.0,
    )
)

res = a.add_resource_name(
    NewResourceName(
        asset_name="New Battery",
        resource_type_name="BESS",
        asset_resource_name="RES_1",
    )
)
