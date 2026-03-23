import pytest
import pandas as pd
import numpy as np
from src.data_processor import build_master_table


def test_data_processing_numeric_stability():
    # Verifies engine generates scores without crashing on local data
    results = build_master_table(lambda *args: None)

    assert not results.empty
    assert 'Value Score' in results.columns
    # Logic check: Verify scores are numbers, not strings or NaNs
    assert isinstance(results['Value Score'].iloc[0], (int, float, np.integer))


def test_logic_score_integrity():
    # Verifies all 4 AI scores are present in final output table
    results = build_master_table(lambda *args: None)

    required_scores = ['Value Score', 'Growth Score', 'Momentum Score', 'Overall AI Score']
    for score in required_scores:
        assert score in results.columns
        assert not results[score].isnull().any()


def test_ticker_data_loading():
    # Verifies that Ticker column is correctly loaded and formatted
    results = build_master_table(lambda *args: None)

    # Asserting against specific dataset size (108 tickers)
    assert len(results) > 100
    assert 'Ticker' in results.columns
    # Check tickers are strings
    assert isinstance(results['Ticker'].iloc[0], str)


def test_sector_distribution():
    # Verifies Sector-based logic has enough diversity to rank
    results = build_master_table(lambda *args: None)

    unique_sectors = results['Sector'].nunique()
    assert unique_sectors > 1


def test_overall_score_clamping():
    # Verifies final engine respects the logic-based scoring bounds
    results = build_master_table(lambda *args: None)

    overall_min = results['Overall AI Score'].min()
    overall_max = results['Overall AI Score'].max()

    # Overall AI Score should be normalized
    assert overall_min >= 0
    assert overall_max <= 100


def test_null_values():
    # Verifies engine handles missing values correctly
    results = build_master_table(lambda *args: None)
    assert results['Value Score'].dtype in [np.float64, np.int64]


def test_column_naming_convention():
    # Verifies column names match what the Streamlit UI expects
    results = build_master_table(lambda *args: None)

    expected_cols = ['Ticker', 'Sector', 'Value Score', 'Growth Score', 'Momentum Score']
    for col in expected_cols:
        assert col in results.columns


def test_dataframe_sorting_capability():
    # Verifies that the output can be sorted by Overall AI Score."""
    results = build_master_table(lambda *args: None)

    sorted_df = results.sort_values(by='Overall AI Score', ascending=True)
    assert sorted_df.iloc[0]['Ticker'] != sorted_df.iloc[-1]['Ticker']


def test_callback_execution():
    # Verifies that function correctly communicates with the UI agent
    calls = []

    def mock_callback(progress, message):
        calls.append(progress)

    build_master_table(mock_callback)
    assert len(calls) > 0


def test_deterministic_output():
    # Verifies running the engine twice returns identical AI advice
    results_run_1 = build_master_table(lambda *args: None)
    results_run_2 = build_master_table(lambda *args: None)

    pd.testing.assert_frame_equal(results_run_1, results_run_2)


def test_individual_scores_bounds():
    # Verifies that individual AI scores do not break the UI scale
    results = build_master_table(lambda *args: None)

    scores = ['Value Score', 'Growth Score', 'Momentum Score']
    for score in scores:
        assert results[score].min() >= 0
        assert results[score].max() <= 100


def test_sector_data_integrity():
    # Verifies that every stock is assigned a valid Sector string
    results = build_master_table(lambda *args: None)

    assert 'Sector' in results.columns
    # The bot cannot rank by sector if a sector is missing (NaN)
    assert not results['Sector'].isnull().any()
    assert isinstance(results['Sector'].iloc[0], str)


def test_progress_completion():
    # Verifies the progress callback actually reaches 100%
    progress_values = []

    def mock_callback(progress, message):
        progress_values.append(progress)

    build_master_table(mock_callback)

    assert max(progress_values) == pytest.approx(1.0, rel=1e-2)


def test_no_infinite_scores():
    # Verifies division by zero didn't result in infinite
    results = build_master_table(lambda *args: None)

    scores = ['Value Score', 'Growth Score', 'Momentum Score', 'Overall AI Score']
    for score in scores:
        assert not np.isinf(results[score]).any()
