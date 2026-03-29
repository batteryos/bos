"""Main BOS API client -- entry point for all domains."""

from bos.analysis.client import AnalysisClient
from bos.analysis.config import ENDPOINTS as ANALYSIS_ENDPOINTS
from bos.assets.client import AssetsClient
from bos.assets.config import ENDPOINTS as ASSETS_ENDPOINTS
from bos.auth import resolve_tokens
from bos.calc.client import CalcClient
from bos.calc.config import ENDPOINTS as CALC_ENDPOINTS
from bos.dashboard.client import DashboardClient
from bos.dashboard.config import ENDPOINTS as DASHBOARD_ENDPOINTS
from bos.gridqueue.client import QueueClient
from bos.gridqueue.config import ENDPOINTS as QUEUE_ENDPOINTS
from bos.prices.client import PricesClient
from bos.prices.config import ENDPOINTS as PRICES_ENDPOINTS


class BOSClient:
    """Unified client for the BatteryOS API.

    Usage::

        from bos import BOSClient

        client = BOSClient()
        calcs = client.calc.list_calcs()
        tbn = client.prices.get_actuals_tbn("ercot", "HB_HOUSTON")
        assets = client.assets.list_assets()
        ranking = client.dashboard.get_ranking()
        projects = client.queue.list_projects()
    """

    def __init__(self, token=None, timeout=30):
        tokens = resolve_tokens(token)
        self.calc = CalcClient(tokens, CALC_ENDPOINTS, timeout=timeout)
        self.assets = AssetsClient(tokens, ASSETS_ENDPOINTS, timeout=timeout)
        self.queue = QueueClient(tokens, QUEUE_ENDPOINTS, timeout=timeout)
        self.dashboard = DashboardClient(tokens, DASHBOARD_ENDPOINTS, timeout=timeout)
        self.prices = PricesClient(tokens, PRICES_ENDPOINTS, timeout=timeout)
        self.analysis = AnalysisClient(tokens, ANALYSIS_ENDPOINTS, timeout=timeout)
