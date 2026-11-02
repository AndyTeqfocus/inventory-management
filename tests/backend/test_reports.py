"""
Tests for the reports endpoints (quarterly and monthly trends),
including the global filter parameters they share with /api/orders.
"""
import pytest


class TestQuarterlyReports:
    """Test suite for /api/reports/quarterly."""

    def test_get_quarterly_reports(self, client):
        """Unfiltered call returns the four 2025 quarters in order."""
        response = client.get("/api/reports/quarterly")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert [q["quarter"] for q in data] == ["Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025"]

        for q in data:
            assert q["total_orders"] > 0
            assert q["total_revenue"] > 0
            assert q["avg_order_value"] == pytest.approx(q["total_revenue"] / q["total_orders"], abs=0.01)
            assert 0 <= q["fulfillment_rate"] <= 100

    def test_quarter_filter(self, client):
        """A quarter in the month filter narrows the result to that quarter."""
        response = client.get("/api/reports/quarterly?month=Q2-2025")
        assert response.status_code == 200
        data = response.json()
        assert [q["quarter"] for q in data] == ["Q2-2025"]

    def test_status_filter_drives_fulfillment_rate(self, client):
        """Filtering to delivered orders yields a 100% fulfillment rate."""
        response = client.get("/api/reports/quarterly?status=Delivered")
        assert response.status_code == 200
        for q in response.json():
            assert q["delivered_orders"] == q["total_orders"]
            assert q["fulfillment_rate"] == 100.0

    def test_warehouse_filter_reduces_totals(self, client):
        """A warehouse filter never increases order counts versus unfiltered."""
        all_q = {q["quarter"]: q for q in client.get("/api/reports/quarterly").json()}
        sf_q = {q["quarter"]: q for q in client.get("/api/reports/quarterly?warehouse=San%20Francisco").json()}
        assert sf_q, "expected at least one quarter for San Francisco"
        for quarter, q in sf_q.items():
            assert q["total_orders"] <= all_q[quarter]["total_orders"]
        assert sum(q["total_orders"] for q in sf_q.values()) < sum(q["total_orders"] for q in all_q.values())


class TestMonthlyTrends:
    """Test suite for /api/reports/monthly-trends."""

    def test_get_monthly_trends(self, client):
        """Unfiltered call returns months sorted ascending with counts and revenue."""
        response = client.get("/api/reports/monthly-trends")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        months = [m["month"] for m in data]
        assert months == sorted(months)

        for m in data:
            assert len(m["month"]) == 7  # YYYY-MM
            assert m["order_count"] > 0
            assert m["revenue"] > 0
            assert 0 <= m["delivered_count"] <= m["order_count"]

    def test_month_filter(self, client):
        """A single month filter returns exactly that month."""
        response = client.get("/api/reports/monthly-trends?month=2025-03")
        assert response.status_code == 200
        assert [m["month"] for m in response.json()] == ["2025-03"]

    def test_quarter_filter(self, client):
        """A quarter filter returns only that quarter's three months."""
        response = client.get("/api/reports/monthly-trends?month=Q3-2025")
        assert response.status_code == 200
        assert [m["month"] for m in response.json()] == ["2025-07", "2025-08", "2025-09"]

    def test_category_filter_matches_orders_endpoint(self, client):
        """Monthly order counts under a filter agree with /api/orders under the same filter."""
        params = "category=Sensors&warehouse=Tokyo"
        orders = client.get(f"/api/orders?{params}").json()
        trends = client.get(f"/api/reports/monthly-trends?{params}").json()
        assert sum(m["order_count"] for m in trends) == len(orders)
        assert sum(m["revenue"] for m in trends) == pytest.approx(sum(o["total_value"] for o in orders), abs=0.01)
