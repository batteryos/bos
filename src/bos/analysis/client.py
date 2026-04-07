"""Analysis API client -- TBn, RPO, basis, EOn, CRR, CycN."""

from bos.base import BaseClient


class AnalysisClient(BaseClient):
    """Client for analysis, chukar, and cycn endpoints."""

    # -- Actuals ----------------------------------------------------------

    def get_actuals_tbn(self, iso, node, **params):
        """GET /analysis/history/{iso}/{node}/tbn/ -- Actual TBn."""
        return self.get(f"/analysis/history/{iso}/{node}/tbn/", params=params or None)

    def get_actuals_rpo(self, iso, node, **params):
        """GET /analysis/history/{iso}/{node}/rpo/ -- Actual RPO."""
        return self.get(f"/analysis/history/{iso}/{node}/rpo/", params=params or None)

    def get_actuals_basis(self, iso, node, **params):
        """GET /analysis/history/{iso}/{node}/basis/ -- Basis calculation."""
        return self.get(f"/analysis/history/{iso}/{node}/basis/", params=params or None)

    def get_actuals_eon(self, iso, node, **params):
        """GET /analysis/history/{iso}/{node}/eon/ -- Actual Energy Only."""
        return self.get(f"/analysis/history/{iso}/{node}/eon/", params=params or None)

    def get_actuals_aggregate(self, iso, node, **params):
        """GET /analysis/history/{iso}/{node}/aggregate/ -- Aggregate actuals."""
        return self.get(
            f"/analysis/history/{iso}/{node}/aggregate/", params=params or None
        )

    # -- Forwards ---------------------------------------------------------

    def get_forwards_tbn(self, iso, node, **params):
        """GET /analysis/futures/{iso}/{node}/tbn/ -- Forwards TBn."""
        return self.get(f"/analysis/futures/{iso}/{node}/tbn/", params=params or None)

    def get_forwards_rpo(self, iso, node, **params):
        """GET /analysis/futures/{iso}/{node}/rpo/ -- Forwards RPO."""
        return self.get(f"/analysis/futures/{iso}/{node}/rpo/", params=params or None)

    def get_forwards_eon(self, iso, node, **params):
        """GET /analysis/futures/{iso}/{node}/eon/ -- Forwards Energy Only."""
        return self.get(f"/analysis/futures/{iso}/{node}/eon/", params=params or None)

    def get_forwards_aggregate(self, iso, node, **params):
        """GET /analysis/futures/{iso}/{node}/aggregate/ -- Aggregate forwards."""
        return self.get(
            f"/analysis/futures/{iso}/{node}/aggregate/", params=params or None
        )

    # -- CycN -------------------------------------------------------------

    def get_cycle_revenue(self, annual_cycles, file, data_format="json"):
        """POST /analysis/cycn/{annual_cycles}/ -- Cycle revenue optimizer.

        Args:
            annual_cycles: Upper bound on max cycles per year
            file: File-like object (CSV with daily revenue + cycle data)
            data_format: json or csv
        """
        return self.post_multipart(
            f"/analysis/cycn/{annual_cycles}/",
            data={"data_format": data_format},
            files={"file": file},
        )

    # -- CRR basis --------------------------------------------------------

    def get_crr_basis(self, iso, node, hub, **params):
        """GET /chukar/{iso}/{node}/basis/{hub}/ -- CRR basis."""
        return self.get(f"/chukar/{iso}/{node}/basis/{hub}/", params=params or None)
