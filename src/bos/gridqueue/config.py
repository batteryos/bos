"""Queue endpoint declarations."""

BOS_QUEUE = "https://batteryos.com/api/v1/queue"

ENDPOINTS = [
    {"endpoint": "/{iso}/projects/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {
        "endpoint": "/{iso}/projects/milestones/",
        "host": BOS_QUEUE,
        "api_key": "BOS_API",
    },
    {"endpoint": "/{iso}/project/{inr}/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {"endpoint": "/pois/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {"endpoint": "/buses/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {"endpoint": "/{iso}/bus/{slug}/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {"endpoint": "/poi_buses/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {"endpoint": "/add/bus/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {"endpoint": "/update/bus/", "host": BOS_QUEUE, "api_key": "BOS_API"},
    {"endpoint": "/add/poibus/", "host": BOS_QUEUE, "api_key": "BOS_API"},
]
