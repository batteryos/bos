"""Exhaustive examples for every CalcClient endpoint and parameter config.

39 endpoints. Covers every distinct call signature:
  GET no args, GET single slug, GET slug+sub, GET slug+nested, GET 2-3 path segments
  GET binary (get_bytes), POST no body, POST with CalcCreate/DataObjectCreate dataclass
  POST with MultichartParams, POST with path segments

Usage:
    export BOS_API=your-token
    python -m bos.calc.examples
"""

from bos import BOSClient
from bos.calc.models import CalcCreate, DataObjectCreate, MultichartParams

client = BOSClient()
c = client.calc


# ============================================================
# GET — no args (static paths)
# ============================================================

nodes = c.get_node_data()
features = c.get_product_features()
params = c.get_scenario_params()
exchanges = c.get_exchanges()
calcs = c.list_calcs()
data_objs = c.list_data_objects()
c.register_dragon_webhook()
c.register_prices_webhook()


# ============================================================
# GET — single slug
# ============================================================

calc = c.get_calc("CALC_SLUG")
status = c.get_calc_status("CALC_SLUG")
summary = c.get_calc_summary("CALC_SLUG")
data_obj = c.get_data_object("DATA_SLUG")
results = c.fetch_results("STACK_SLUG")
ns_rev = c.get_ns_revenue("STACK_SLUG")
c.toggle_favorite("STACK_SLUG")
fwd_status = c.get_forwards_status("FORWARDS_SLUG")


# ============================================================
# GET — slug + sub-collection (returns list)
# ============================================================

calc_nodes = c.list_calc_nodes("CALC_SLUG")
calc_scenarios = c.list_calc_scenarios("CALC_SLUG")
ns_list = c.list_node_scenarios("CALC_SLUG")
data_calcs = c.get_data_object_calcs("DATA_SLUG")


# ============================================================
# GET — slug + nested slug
# ============================================================

node = c.get_calc_node("CALC_SLUG", "NODE_SLUG")
scenario = c.get_calc_scenario("CALC_SLUG", "SCENARIO_SLUG")
ns = c.get_node_scenario("CALC_SLUG", "NS_SLUG")


# ============================================================
# GET — slug + nested slug + sub-resource
# ============================================================

ns_detail = c.get_ns_detail("CALC_SLUG", "NS_SLUG")
ns_result = c.get_ns_result("CALC_SLUG", "NS_SLUG")
ns_daily = c.get_ns_daily_result("CALC_SLUG", "NS_SLUG")
ns_params = c.get_ns_params("CALC_SLUG", "NS_SLUG")
ns_status = c.get_ns_status("CALC_SLUG", "NS_SLUG")


# ============================================================
# GET — two/three path segments
# ============================================================

node_detail = c.get_node("ercot", "HB_HOUSTON")
refdates = c.get_valid_refdates("ercot", "HB_HOUSTON", "ice")


# ============================================================
# GET — binary download
# ============================================================

xls_bytes = c.download_ns_xls("CALC_SLUG", "NS_SLUG")


# ============================================================
# POST — CalcCreate dataclass (typed path)
# ============================================================

new_calc = c.create_calc(CalcCreate(name="Houston 100MW/2hr"))

new_calc_full = c.create_calc(
    CalcCreate(
        name="Houston Custom",
        iso="ERCOT",
        node="HB_HOUSTON",
        capacity=200.0,
        duration=4.0,
        description="Custom 4hr calc",
        is_public=True,
    )
)

# kwargs escape hatch
new_calc_kw = c.create_calc(name="Quick Calc", iso="ERCOT", node="HB_NORTH")


# ============================================================
# POST — DataObjectCreate dataclass
# ============================================================

new_data = c.create_data_object(DataObjectCreate(name="My Data"))
new_data_full = c.create_data_object(
    DataObjectCreate(name="Full", description="With desc")
)


# ============================================================
# POST — MultichartParams dataclass
# ============================================================

chart = c.multichart("STACK_SLUG")
chart_typed = c.multichart(
    "STACK_SLUG", MultichartParams(chart_type="revenue", period="annual")
)
chart_kw = c.multichart("STACK_SLUG", chart_type="volume")


# ============================================================
# POST — no body (action triggers)
# ============================================================

c.dispatch("STACK_SLUG")
c.trigger_forwards("ercot", "HB_HOUSTON", "2026-03-25")
c.trigger_historical("ercot", "HB_HOUSTON")
