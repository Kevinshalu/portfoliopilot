"""Smoke tests for Tool 5: anomalies."""
import numpy as np
import pandas as pd

from tools.anomalies import _compute_zscores, _fetch_price_volume, flag_anomalies


def test_compute_zscores_flags_known_spike():
    """A synthetic spike on the last day should produce |z| >> 2 on that row."""
    np.random.seed(0)
    n = 70
    close = pd.Series(100 + np.random.normal(0, 1, n).cumsum())
    high = close + 0.5
    low = close - 0.5
    volume = pd.Series(np.random.normal(1_000_000, 50_000, n))  # ~5% baseline noise
    # Inject a clean 10x volume spike on the very last row
    volume.iloc[-1] = 10_000_000

    df = pd.DataFrame({"Open": close, "High": high, "Low": low, "Close": close, "Volume": volume})
    z = _compute_zscores(df, baseline_days=60, window_days=5)
    assert not z.empty
    assert z["volume"].iloc[-1] > 5.0


def test_compute_zscores_too_short_returns_empty():
    """Insufficient history should return an empty DataFrame, not raise."""
    df = pd.DataFrame({
        "Open": [1, 2], "High": [1, 2], "Low": [1, 2], "Close": [1, 2], "Volume": [100, 100],
    })
    assert _compute_zscores(df, baseline_days=60, window_days=5).empty


def test_flag_anomalies_end_to_end():
    """Live pipeline should return the expected shape and a valid summary."""
    result = flag_anomalies()
    assert "anomalies" in result
    assert "summary" in result
    assert isinstance(result["anomalies"], list)
    # Every flagged anomaly should be well-shaped
    for a in result["anomalies"]:
        assert set(a.keys()) >= {"ticker", "date", "signal", "z_score", "value"}
        assert a["signal"] in {"return", "volume", "range"}
        assert abs(a["z_score"]) >= 2.0  # respects the default threshold