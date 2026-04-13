"""Prices API client -- contracts, actuals, forwards."""

import io
import zipfile

import pandas as pd
from bos.base import BaseClient
from bos.prices.models import AvailableDate, Contract, ContractPrice, Exchange


class PricesClient(BaseClient):
    """Client for prices and kronos endpoints."""

    # -- Kronos contracts -------------------------------------------------

    def list_exchanges(self):
        """GET /kronos/contracts/ -- List available exchanges."""
        data = self.get("/kronos/contracts/")
        if isinstance(data, list):
            return [Exchange.from_dict(d) for d in data]
        return data

    def list_contracts(self, exchange_code="IFED", **filters):
        """GET /kronos/contracts/{exchange_code}/ -- Contract metadata.

        Args:
            exchange_code: Exchange MIC code (default: IFED)
            **filters: iso, node, dart_mode, settlement
        """
        data = self.get(f"/kronos/contracts/{exchange_code}/", params=filters or None)
        if isinstance(data, list):
            return [Contract.from_dict(d) for d in data]
        return data

    def get_contract(
        self,
        symbol,
        exchange_code="IFED",
        refdate=None,
        fordate=None,
        startref=None,
        endref=None,
        strip=None,
        freq=None,
        step=None,
        data_format=None,
    ):
        """GET /kronos/contracts/{exchange_code}/{symbol}/ -- Prices or dates.

        Without date params: returns available dates.
        With date params: returns prices.
        """
        params = {}
        if refdate:
            params["refdate"] = refdate
        if fordate:
            params["fordate"] = fordate
        if startref:
            params["startref"] = startref
        if endref:
            params["endref"] = endref
        if strip:
            params["strip"] = strip
        if freq:
            params["freq"] = freq
        if step is not None:
            params["step"] = str(step).lower()
        if data_format:
            params["data_format"] = data_format

        data = self.get(
            f"/kronos/contracts/{exchange_code}/{symbol}/",
            params=params or None,
        )

        if isinstance(data, list) and data:
            if "min_fordate" in data[0]:
                return [AvailableDate.from_dict(d) for d in data]
            if "price" in data[0]:
                return [ContractPrice.from_dict(d) for d in data]
        return data

    def get_available_refdates(self, symbol, exchange_code="IFED", **params):
        """GET /kronos/contracts/{exchange_code}/{symbol}/available_dates/"""
        return self.get(
            f"/kronos/contracts/{exchange_code}/{symbol}/available_dates/",
            params=params or None,
        )

    def compare_prices(
        self, symbol, contract_exchange, price_exchange, refdate, **params
    ):
        """GET /kronos/compare/{exc1}/{symbol}/{exc2}/{refdate}/"""
        return self.get(
            f"/kronos/compare/{contract_exchange}/{symbol}/"
            f"{price_exchange}/{refdate}/",
            params=params or None,
        )

    # -- Prices data ------------------------------------------------------

    def get_actuals(self, iso, node, **params):
        """POST /prices/history/{iso}/{node}/ -- Historical actuals.
        Returns a list of records if JSON, or a Pandas DataFrame if a ZIP file is returned.
        """
        data = self.post(f"/prices/history/{iso}/{node}/", json_data=params or None)

        if isinstance(data, bytes):
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    # Find all CSV files and combine them
                    csv_files = [f for f in z.namelist() if f.endswith(".csv")]
                    if not csv_files:
                        return data  # Return raw bytes if no CSVs found in ZIP

                    dfs = []
                    for csv_file in csv_files:
                        with z.open(csv_file) as f:
                            dfs.append(pd.read_csv(f))

                    return pd.concat(dfs, ignore_index=True)
            except Exception:
                # Log error and return raw bytes if processing fails
                return data

        return data

    def get_forwards(self, iso, node, refdate, **params):
        """POST /prices/futures/{iso}/{node}/{refdate}/ -- Forwards data.
        Returns a list of records if JSON, or a Pandas DataFrame if a ZIP file is returned.
        """
        data = self.post(
            f"/prices/futures/{iso}/{node}/{refdate}/", json_data=params or None
        )

        if isinstance(data, bytes):
            try:
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    csv_files = [f for f in z.namelist() if f.endswith(".csv")]
                    if not csv_files:
                        return data

                    dfs = []
                    for csv_file in csv_files:
                        with z.open(csv_file) as f:
                            dfs.append(pd.read_csv(f))

                    return pd.concat(dfs, ignore_index=True)
            except Exception:
                return data

        return data

    def get_agg_forwards(self, exchange, iso, node, curve, agg, **params):
        """GET /prices/futures/{exchange}/{iso}/{node}/{curve}/{agg}/"""
        return self.get(
            f"/prices/futures/{exchange}/{iso}/{node}/{curve}/{agg}/",
            params=params or None,
        )
