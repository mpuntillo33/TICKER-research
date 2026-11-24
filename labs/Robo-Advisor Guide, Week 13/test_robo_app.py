from robo_app import metrics, suggested_allocation
import pandas as pd


def test_allocation_sums_to_100():
    allocation = suggested_allocation(35, 20, False, True, 20, "Stay the course")
    assert sum(allocation) == 100


def test_metrics_compounds_and_counts_months():
    values = pd.Series([.01, -.01, .02], index=pd.date_range("2020-01-01", periods=3, freq="MS"))
    result = metrics(values, 1000)
    assert result["months"] == 3
    assert result["wealth"].iloc[-1] == (1.01 * .99 * 1.02)
