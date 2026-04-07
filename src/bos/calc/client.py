"""Calc API client -- calculations, data objects, node-scenario results."""

from bos.base import BaseClient
from bos.calc.models import (
    Calc,
    CalcNode,
    CalcScenario,
    DataObject,
    NodeScenario,
)


class CalcClient(BaseClient):
    """Client for batteryos.com/api/v1 calc and data endpoints."""

    # --- Data objects ---

    def list_data_objects(self):
        """GET /data/ -- List all data objects."""
        data = self.get("/data/")
        if isinstance(data, list):
            return [DataObject.from_dict(d) for d in data]
        return data

    def create_data_object(self, req=None, **kwargs):
        """POST /data/ -- Upload or request data."""
        result = self.post("/data/", self.serialize(req, kwargs))
        return DataObject.from_dict(result) if isinstance(result, dict) else result

    def get_data_object(self, slug):
        """GET /data/{slug}/ -- Data object detail."""
        data = self.get(f"/data/{slug}/")
        return DataObject.from_dict(data) if isinstance(data, dict) else data

    def get_data_object_calcs(self, slug):
        """GET /data/{slug}/calc/ -- Calcs using this data object."""
        data = self.get(f"/data/{slug}/calc/")
        if isinstance(data, list):
            return [Calc.from_dict(d) for d in data]
        return data

    # --- Calc CRUD ---

    def list_calcs(self):
        """GET /calc/ -- List all calculations."""
        data = self.get("/calc/")
        if isinstance(data, list):
            return [Calc.from_dict(d) for d in data]
        return data

    def create_calc(self, req=None, **kwargs):
        """POST /calc/ -- Run a calculation."""
        result = self.post("/calc/", self.serialize(req, kwargs))
        return Calc.from_dict(result) if isinstance(result, dict) else result

    def get_calc(self, slug):
        """GET /calc/{slug}/ -- Calculation details."""
        data = self.get(f"/calc/{slug}/")
        return Calc.from_dict(data) if isinstance(data, dict) else data

    def get_calc_status(self, slug):
        """GET /calc/{slug}/status/ -- Calculation status."""
        return self.get(f"/calc/{slug}/status/")

    def get_calc_summary(self, slug):
        """GET /calc/{slug}/summary/ -- Calculation summary results."""
        return self.get(f"/calc/{slug}/summary/")

    # --- Calc nodes/scenarios ---

    def list_calc_nodes(self, slug):
        """GET /calc/{slug}/nodes/ -- List nodes in calc."""
        data = self.get(f"/calc/{slug}/nodes/")
        if isinstance(data, list):
            return [CalcNode.from_dict(d) for d in data]
        return data

    def get_calc_node(self, slug, node_slug):
        """GET /calc/{slug}/nodes/{node_slug}/ -- Node detail."""
        data = self.get(f"/calc/{slug}/nodes/{node_slug}/")
        return CalcNode.from_dict(data) if isinstance(data, dict) else data

    def list_calc_scenarios(self, slug):
        """GET /calc/{slug}/scenarios/ -- List scenarios in calc."""
        data = self.get(f"/calc/{slug}/scenarios/")
        if isinstance(data, list):
            return [CalcScenario.from_dict(d) for d in data]
        return data

    def get_calc_scenario(self, slug, scenario_slug):
        """GET /calc/{slug}/scenarios/{scenario_slug}/ -- Scenario detail."""
        data = self.get(f"/calc/{slug}/scenarios/{scenario_slug}/")
        return CalcScenario.from_dict(data) if isinstance(data, dict) else data

    # --- Node-scenario results ---

    def list_node_scenarios(self, slug):
        """GET /calc/{slug}/nodescenarios/ -- List all node-scenarios."""
        data = self.get(f"/calc/{slug}/nodescenarios/")
        if isinstance(data, list):
            return [NodeScenario.from_dict(d) for d in data]
        return data

    def get_node_scenario(self, slug, ns):
        """GET /calc/{slug}/nodescenarios/{ns}/ -- Node-scenario detail."""
        data = self.get(f"/calc/{slug}/nodescenarios/{ns}/")
        return NodeScenario.from_dict(data) if isinstance(data, dict) else data

    def get_ns_result(self, slug, ns):
        """GET /calc/{slug}/nodescenarios/{ns}/result/ -- NS results (ZIP)."""
        return self.get(f"/calc/{slug}/nodescenarios/{ns}/result/")

    def get_ns_daily_result(self, slug, ns):
        """GET /calc/{slug}/nodescenarios/{ns}/daily_result/ -- NS daily (ZIP)."""
        return self.get(f"/calc/{slug}/nodescenarios/{ns}/daily_result/")

    def get_ns_params(self, slug, ns):
        """GET /calc/{slug}/nodescenarios/{ns}/params/ -- NS input parameters."""
        return self.get(f"/calc/{slug}/nodescenarios/{ns}/params/")

    def get_ns_status(self, slug, ns):
        """GET /calc/{slug}/nodescenarios/{ns}/status/ -- NS execution status."""
        return self.get(f"/calc/{slug}/nodescenarios/{ns}/status/")

    # --- Dragonet ---

    def run_dragonet(self, iso, node, file, params=None, data_format="json"):
        """POST /dragonet/calc/ -- Run Dragonet calculation.

        Args:
            iso: ISO code
            node: Node name
            file: File-like object (CSV input)
            params: JSON string of additional parameters
            data_format: json or zip
        """
        data = {"iso": iso, "node": node, "data_format": data_format}
        if params:
            data["params"] = params
        return self.post_multipart("/dragonet/calc/", data=data, files={"file": file})
