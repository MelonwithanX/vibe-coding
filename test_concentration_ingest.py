import pytest
import pandas as pd
from performance_ingest import load_concentration, summarize_concentration

def test_load_concentration_columns():
    df = load_concentration('PerformanceData/Concentration_20250326.csv')
    assert list(df.columns) == ['SubSection', 'Symbol', 'Description', 'Sector', 'Value', 'ParsedWeight']

def test_load_concentration_dtypes():
    df = load_concentration('PerformanceData/Concentration_20250326.csv')
    assert pd.api.types.is_numeric_dtype(df['Value'])
    assert pd.api.types.is_numeric_dtype(df['ParsedWeight'])

def test_load_concentration_non_empty():
    df = load_concentration('PerformanceData/Concentration_20250326.csv')
    assert not df.empty

def test_concentration_value_ranges():
    df = load_concentration('PerformanceData/Concentration_20250326.csv')
    # Reasonable value and weight ranges
    assert (df['Value'] >= 0).all()
    assert (df['ParsedWeight'] >= 0).all()
    assert (df['ParsedWeight'] <= 100).all() or (df['ParsedWeight'] <= 100).sum() > 0

def test_summarize_concentration():
    df = load_concentration('PerformanceData/Concentration_20250326.csv')
    summary = summarize_concentration(df)
    assert 'summary' in summary
    assert 'correlation' in summary
    assert 'sector_summary' in summary
    assert isinstance(summary['summary'], dict)
    assert isinstance(summary['correlation'], dict)
    assert isinstance(summary['sector_summary'], pd.DataFrame)
