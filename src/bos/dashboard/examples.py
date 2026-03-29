"""Exhaustive examples for every DashboardClient endpoint and parameter config.

7 endpoints. Covers:
  GET no args (typed list), GET no args (raw dict)
  GET with kwargs (owner, dates, year/n params)

Usage:
    export BOS_API=your-token
    python -m bos.dashboard.examples
"""

from bos import BOSClient

client = BOSClient()
b = client.dashboard


# ============================================================
# GET — no args, returns raw dict
# ============================================================

data_key = b.get_data_key()
queue_cap = b.get_queue_capacity()


# ============================================================
# GET — no args, returns typed list
# ============================================================

ranking_bare = b.get_ranking()
dispatch_bare = b.get_dispatch()
revenue_bare = b.get_revenue()


# ============================================================
# GET — with kwargs, returns typed list
# ============================================================

ranking_owner = b.get_ranking(owner="vistra")
ranking_filtered = b.get_ranking(iso="ERCOT", category="standalone")
ranking_dates = b.get_ranking(startdate="2025-01-01", enddate="2025-12-31")
ranking_report = b.get_ranking(report_name="owner_performance")

dispatch_owner = b.get_dispatch(owner="vistra")
dispatch_month = b.get_dispatch(owner="vistra", month="2025-03-31")

revenue_owner = b.get_revenue(owner="vistra")
revenue_dates = b.get_revenue(startdate="2025-01-01", enddate="2025-12-31")
revenue_filtered = b.get_revenue(iso="ERCOT", category="standalone")


# ============================================================
# GET — with kwargs, returns raw dict
# ============================================================

tbn_ercot_bare = b.get_tbn_ercot()
tbn_ercot_params = b.get_tbn_ercot(year="2025", n="2")
tbn_ercot_4hr = b.get_tbn_ercot(year="2026", n="4")

tbn_us_bare = b.get_tbn_us()
tbn_us_params = b.get_tbn_us(year="2025", n="2")
