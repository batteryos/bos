"""Exhaustive examples for every PricesClient endpoint and parameter config.

19 endpoints. Covers:
  GET no args (list), GET slug, GET slug+query params, GET proxy+kwargs,
  POST form-encoded with all param combos, CSV downloads, cross-exchange compare

Usage:
    export BOS_API=your-token
    python -m bos.prices.examples
"""

from bos import BOSClient
from bos.prices.models import ERCOT_HUBS, HUB_CONTRACT_MAP, SHAPES, Hub

client = BOSClient()
p = client.prices


# ============================================================
# Exchanges
# ============================================================

exchanges = p.list_exchanges()


# ============================================================
# Contracts -- default IFED, with exchange_code, with filters
# ============================================================

contracts = p.list_contracts()
contracts_ifed = p.list_contracts("IFED")
contracts_bos = p.list_contracts("BOS")
contracts_filtered = p.list_contracts("IFED", shape="peak")


# ============================================================
# Contract detail -- available dates (no date params)
# ============================================================

dates = p.get_contract("ERH")
dates_bos = p.get_contract("ERH", exchange_code="BOS")


# ============================================================
# Contract detail -- prices (with date params)
# ============================================================

prices_ref = p.get_contract("ERH", refdate="2026-03-25")
prices_for = p.get_contract("ERH", refdate="2026-03-25", fordate="2026-06-01")
prices_range = p.get_contract("ERH", startref="2026-01-01", endref="2026-03-25")
prices_strip = p.get_contract("ERH", refdate="2026-03-25", strip="CAL26")
prices_freq = p.get_contract("ERH", refdate="2026-03-25", freq="monthly")
prices_step = p.get_contract("ERH", refdate="2026-03-25", step=True)
prices_custom = p.get_contract("ERH", exchange_code="BOS", refdate="2026-03-25")


# ============================================================
# Contract CSV download
# ============================================================

csv_bytes = p.get_contract_csv("ERH", refdate="2026-03-25")
csv_strip = p.get_contract_csv("ERH", refdate="2026-03-25", strip="CAL26")
csv_custom = p.get_contract_csv("ERH", exchange_code="BOS", refdate="2026-03-25")


# ============================================================
# Available refdates (dedicated endpoint)
# ============================================================

refdates = p.get_available_refdates("ERH")
refdates_bos = p.get_available_refdates("ERH", exchange_code="BOS")


# ============================================================
# Cross-exchange price comparison
# ============================================================

comparison = p.compare_prices("ERH", "IFED", "BOS", "2026-03-25")


# ============================================================
# DAM/RTM history (POST form-encoded)
# ============================================================

history_min = p.get_history("HB_HOUSTON")
history_1c1y = p.get_history("HB_HOUSTON", curves=["dam"], years=[2025])
history_str = p.get_history("HB_HOUSTON", curves="dam", years=2025)
history_mc1y = p.get_history("HB_HOUSTON", curves=["dam", "rtm"], years=[2025])
history_1cmy = p.get_history("HB_HOUSTON", curves=["dam"], years=[2024, 2025])
history_mcmy = p.get_history("HB_HOUSTON", curves=["dam", "rtm"], years=[2024, 2025])
history_north = p.get_history("HB_NORTH", curves=["dam"], years=[2025])
history_fmt = p.get_history("HB_HOUSTON", curves=["dam"], years=[2025], fmt="csv")

for hub in ERCOT_HUBS:
    p.get_history(hub, curves=["dam"], years=[2025])


# ============================================================
# Prices data -- node stats, actuals, forwards
# ============================================================

stats = p.get_node_stats("ercot", "HB_HOUSTON")
actuals = p.get_actuals("ercot", "HB_HOUSTON", curves=["dam"], years=[2025])
forwards = p.get_forwards("ercot", "HB_HOUSTON", "2026-03-25")
forwards_status = p.get_forwards_status("some-slug")
agg = p.get_agg_forwards("IFED", "ercot", "HB_HOUSTON", "dam", "monthly")
avail_dates = p.get_forwards_available_dates("IFED", "ercot", "HB_HOUSTON")


# ============================================================
# Proxy catch-alls
# ============================================================

prices_bare = p.proxy_prices("history/ercot/HB_HOUSTON/")
prices_params = p.proxy_prices("history/ercot/HB_HOUSTON/", format="json")
kronos_bare = p.proxy_kronos("contracts/ifed/")
kronos_params = p.proxy_kronos("contracts/ifed/ERH/", refdate="2026-03-25")
analysis_bare = p.proxy_analysis("some/endpoint/")
analysis_params = p.proxy_analysis("some/endpoint/", param1="a", param2="b")


# ============================================================
# Constants and helpers
# ============================================================

houston = Hub.from_name("HB_HOUSTON")
busavg = Hub.from_name("HB_BUSAVG")

for shape in SHAPES:
    symbol = HUB_CONTRACT_MAP.get("HB_HOUSTON", {}).get(shape)
    if symbol:
        p.get_contract(symbol)
