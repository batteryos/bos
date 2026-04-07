"""Prices endpoint declarations."""

TITAN = "https://batteryos.com/api/v1"

ENDPOINTS = [
    {"endpoint": "/kronos/contracts/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/kronos/contracts/{exchange_code}/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/kronos/contracts/{exchange_code}/{symbol}/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/kronos/contracts/{exchange_code}/{symbol}/available_dates/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/kronos/compare/{exc1}/{symbol}/{exc2}/{refdate}/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/prices/history/{iso}/{node}/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/prices/futures/{iso}/{node}/{refdate}/",
     "host": TITAN, "api_key": "BOS_API"},
    {"endpoint": "/prices/futures/{exchange}/{iso}/{node}/{curve}/{agg}/",
     "host": TITAN, "api_key": "BOS_API"},
]
