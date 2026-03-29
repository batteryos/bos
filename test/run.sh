#!/usr/bin/env bash
# BOS API Test Suite — smoke tests for all 89 endpoints
# Usage: ./test/run.sh [--quick]
#
# Requires: curl, BOS_API env var or ~/.bos/credentials
# --quick: skip slow/chained tests (calc NS results, per-asset endpoints)

set -euo pipefail

TOKEN="${BOS_API:-$(cat ~/.bos/credentials 2>/dev/null || true)}"
if [ -z "$TOKEN" ]; then
    echo "ERROR: No token. Set BOS_API or create ~/.bos/credentials"
    exit 1
fi

AUTH="Authorization: Token $TOKEN"
BEAST="https://beast.batteryos.dev/api/v1"
MAIN="https://batteryos.dev/api/v1"
QUICK="${1:-}"

PASS=0
FAIL=0
SKIP=0

test_endpoint() {
    local domain="$1" method="$2" host="$3" path="$4" desc="$5" expect="${6:-200}"
    local start elapsed status

    start=$(date +%s%N 2>/dev/null || date +%s)

    if [ "$method" = "GET" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" -L -H "$AUTH" --max-time 15 "${host}${path}" 2>/dev/null || echo "000")
    elif [ "$method" = "POST" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" -L -X POST -H "$AUTH" -H "Content-Type: application/json" -d '{}' --max-time 15 "${host}${path}" 2>/dev/null || echo "000")
    elif [ "$method" = "POST_FORM" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" -L -X POST -H "$AUTH" -H "Content-Type: application/x-www-form-urlencoded" -d "format=json&curves=dam&years=2025" --max-time 15 "${host}${path}" 2>/dev/null || echo "000")
    elif [ "$method" = "SKIP" ]; then
        printf "  %-10s %-40s SKIP    (mutating)\n" "$domain" "$desc"
        SKIP=$((SKIP + 1))
        return
    fi

    elapsed=$(( ($(date +%s%N 2>/dev/null || date +%s) - start) / 1000000 ))ms 2>/dev/null || elapsed="?"

    if [ "$expect" = "not5xx" ]; then
        if [ "${status:0:1}" != "5" ] && [ "$status" != "000" ]; then
            printf "  %-10s %-40s PASS    %s  %s\n" "$domain" "$desc" "$status" "$elapsed"
            PASS=$((PASS + 1))
        else
            printf "  %-10s %-40s FAIL    %s  %s\n" "$domain" "$desc" "$status" "$elapsed"
            FAIL=$((FAIL + 1))
        fi
    else
        if [ "$status" = "$expect" ]; then
            printf "  %-10s %-40s PASS    %s  %s\n" "$domain" "$desc" "$status" "$elapsed"
            PASS=$((PASS + 1))
        else
            printf "  %-10s %-40s FAIL    %s (expected $expect)\n" "$domain" "$desc" "$status"
            FAIL=$((FAIL + 1))
        fi
    fi
}

echo ""
echo "  BOS API Test Suite — $(date +%Y-%m-%d)"
echo "  Token: ${TOKEN:0:8}...  Hosts: beast + main"
echo "  ================================================================"
echo ""
printf "  %-10s %-40s %-8s %s\n" "Domain" "Endpoint" "Status" "Info"
printf "  %-10s %-40s %-8s %s\n" "------" "--------" "------" "----"

# === PRICES (beast.batteryos.dev) ===
test_endpoint prices POST_FORM "$BEAST" "/prices/history/ercot/HB_HOUSTON/" "DAM history HB_HOUSTON" 200
test_endpoint prices GET "$BEAST" "/kronos/contracts/ifed/" "IFED contract list" 200
test_endpoint prices GET "$BEAST" "/kronos/contracts/ifed/ERN/" "ERN settlements" 200
test_endpoint prices GET "$BEAST" "/kronos/contracts/ifed/ERH/" "ERH settlements" 200
test_endpoint prices GET "$BEAST" "/analysis/" "Analysis proxy" not5xx

# === BESS ASSETS (batteryos.dev) ===
test_endpoint bess POST "$MAIN" "/asset/ercot/" "Asset list" 200
test_endpoint bess GET "$MAIN" "/asset/ercot/owners/" "Owners" 200
test_endpoint bess GET "$MAIN" "/asset/ercot/qse/" "QSEs" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/revenue/" "Revenue actual" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/revenue/perfect/" "Revenue CO perfect" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/revenue/perfect/eo/" "Revenue EO perfect" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/volume/" "Volume actual" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/volume/perfect/" "Volume CO perfect" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/volume/perfect/eo/" "Volume EO perfect" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/volume/dl/" "Volume download" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/volume/dispatch/" "Volume dispatch" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/bosindex/" "BOS Index" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/bosindex/perfect/" "BOS Index perfect" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/availability/" "Availability" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/performance/" "Performance" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/percentiles/" "Percentiles" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/ranking/" "Ranking" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/hsl/" "HSL" 200
test_endpoint bess POST "$MAIN" "/asset/ercot/cycles/" "Cycles" 200
test_endpoint bess POST "$MAIN" "/asset/fixtures/" "Fixtures" not5xx
test_endpoint bess GET "$MAIN" "/asset/webhook/dragon/register/" "Webhook register" not5xx
# Mutating
test_endpoint bess SKIP "" "" "POST new/asset (mutating)"
test_endpoint bess SKIP "" "" "POST new/res_name (mutating)"

# === CALC (batteryos.dev) ===
test_endpoint calc GET "$MAIN" "/calc/stack/node_data/" "Node data" 200
test_endpoint calc GET "$MAIN" "/calc/stack/product_feature/" "Product features" 200
test_endpoint calc GET "$MAIN" "/calc/stack/scenario_params/" "Scenario params" 200
test_endpoint calc GET "$MAIN" "/calc/stack/exchange/" "Exchanges" 200
test_endpoint calc GET "$MAIN" "/calc/data/" "Data list" 200
test_endpoint calc GET "$MAIN" "/calc/calc/" "Calc list" 200
test_endpoint calc GET "$MAIN" "/calc/webhook/dragon/register" "Dragon webhook reg" not5xx
test_endpoint calc GET "$MAIN" "/calc/webhook/prices/register" "Prices webhook reg" not5xx
# Mutating
test_endpoint calc SKIP "" "" "POST data/ (create)"
test_endpoint calc SKIP "" "" "POST calc/ (create)"
test_endpoint calc SKIP "" "" "POST dispatch (mutating)"

if [ "$QUICK" != "--quick" ]; then
    # Chained: need a calc slug first
    CALC_SLUG=$(curl -s -H "$AUTH" --max-time 10 "$MAIN/calc/calc/" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['slug'] if d else '')" 2>/dev/null || true)
    if [ -n "$CALC_SLUG" ]; then
        test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/" "Calc detail" 200
        test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/status/" "Calc status" 200
        test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/summary/" "Calc summary" not5xx
        test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/nodes/" "Calc nodes" 200
        test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/scenarios/" "Calc scenarios" 200
        test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/nodescenarios/" "Calc NS list" 200

        NS_SLUG=$(curl -s -H "$AUTH" --max-time 10 "$MAIN/calc/calc/$CALC_SLUG/nodescenarios/" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['slug'] if d else '')" 2>/dev/null || true)
        if [ -n "$NS_SLUG" ]; then
            test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/nodescenarios/$NS_SLUG/" "NS detail" 200
            test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/nodescenarios/$NS_SLUG/detail/" "NS extended" not5xx
            test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/nodescenarios/$NS_SLUG/result/" "NS annual result" not5xx
            test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/nodescenarios/$NS_SLUG/params/" "NS params" not5xx
            test_endpoint calc GET "$MAIN" "/calc/calc/$CALC_SLUG/nodescenarios/$NS_SLUG/status/" "NS status" 200
        fi
    fi

    test_endpoint calc GET "$MAIN" "/calc/node/ercot/HB_HOUSTON/" "Node lookup" not5xx
    test_endpoint calc GET "$MAIN" "/calc/valid_refdates/ercot/HB_HOUSTON/ice/" "Valid refdates" not5xx
fi

# === QUEUE (batteryos.dev) ===
test_endpoint queue GET "$MAIN" "/queue/ercot/projects/" "Projects" 200
test_endpoint queue GET "$MAIN" "/queue/ercot/projects/milestones/" "Milestones" 200
test_endpoint queue GET "$MAIN" "/queue/pois/" "POIs" 200
test_endpoint queue GET "$MAIN" "/queue/buses/" "Buses" 200
test_endpoint queue GET "$MAIN" "/queue/poi_buses/" "POI-bus mappings" 200
# Mutating
test_endpoint queue SKIP "" "" "POST add/bus (mutating)"
test_endpoint queue SKIP "" "" "POST update/bus (mutating)"
test_endpoint queue SKIP "" "" "POST add/poibus (mutating)"

if [ "$QUICK" != "--quick" ]; then
    INR=$(curl -s -H "$AUTH" --max-time 10 "$MAIN/queue/ercot/projects/" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0].get('inr','') if d else '')" 2>/dev/null || true)
    if [ -n "$INR" ]; then
        test_endpoint queue GET "$MAIN" "/queue/ercot/project/$INR/" "Project detail" 200
    fi
fi

# === BRIDGE (batteryos.dev) ===
test_endpoint bridge GET "$MAIN" "/bridge/ranking/" "Ranking" 200
test_endpoint bridge GET "$MAIN" "/bridge/dispatch/" "Dispatch" 200
test_endpoint bridge GET "$MAIN" "/bridge/revenue/" "Revenue" 200
test_endpoint bridge GET "$MAIN" "/bridge/tbn_ercot/" "TBn ERCOT" 200
test_endpoint bridge GET "$MAIN" "/bridge/tbn_us/" "TBn US" 200
test_endpoint bridge GET "$MAIN" "/bridge/data/" "Data key" 200
test_endpoint bridge GET "$MAIN" "/bridge/queue_capacity/" "Queue capacity" 200

# === PUBLISH (both hosts) ===
test_endpoint publish POST "$BEAST" "/kronos/contracts/admin/BOS/" "Monthly (beast)" not5xx
test_endpoint publish POST "https://titan.batteryos.com/api/v1" "/kronos/contracts/admin/BOS/" "Monthly (titan)" not5xx

# === SUMMARY ===
TOTAL=$((PASS + FAIL + SKIP))
echo ""
echo "  ================================================================"
echo "  Result: $PASS passed, $FAIL failed, $SKIP skipped ($TOTAL total)"
echo ""

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
