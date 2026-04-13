"""Dashboard endpoint declarations."""

BOS_BRIDGE = "https://batteryos.com/api/v1/bridge"

ENDPOINTS = [
    {"endpoint": "/ranking/", "host": BOS_BRIDGE, "api_key": "BOS_API"},
    {"endpoint": "/dispatch/", "host": BOS_BRIDGE, "api_key": "BOS_API"},
    {"endpoint": "/revenue/", "host": BOS_BRIDGE, "api_key": "BOS_API"},
    {"endpoint": "/tbn_ercot/", "host": BOS_BRIDGE, "api_key": "BOS_API"},
    {"endpoint": "/tbn_us/", "host": BOS_BRIDGE, "api_key": "BOS_API"},
    {"endpoint": "/data/", "host": BOS_BRIDGE, "api_key": "BOS_API"},
    {"endpoint": "/queue_capacity/", "host": BOS_BRIDGE, "api_key": "BOS_API"},
]
