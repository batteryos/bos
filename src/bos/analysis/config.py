"""Analysis endpoint declarations."""

TITAN = "https://titan.batteryos.com/api/v1"

ENDPOINTS = [
    {"endpoint": "/analysis/history/{iso}/{node}/tbn/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/history/{iso}/{node}/rpo/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/history/{iso}/{node}/basis/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/history/{iso}/{node}/eon/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/history/{iso}/{node}/aggregate/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/futures/{iso}/{node}/tbn/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/futures/{iso}/{node}/rpo/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/futures/{iso}/{node}/eon/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/futures/{iso}/{node}/aggregate/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/analysis/cycn/{annual_cycles}/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/chukar/{iso}/{node}/basis/{hub}/",
     "host": TITAN, "api_key": "BOS_API"},
]
