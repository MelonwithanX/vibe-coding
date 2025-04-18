import pytest
import pandas as pd
from performance_ingest import load_performance, summarize_performance

def test_load_performance_columns():
    df = load_performance('PerformanceData/Performance_20250321.csv')
    assert list(df.columns) == ['Date', 'Account', 'Return']

def test_load_performance_dtypes():
    df = load_performance('PerformanceData/Performance_20250321.csv')
    assert pd.api.types.is_datetime64_any_dtype(df['Date'])
    assert pd.api.types.is_numeric_dtype(df['Return'])

def test_load_performance_non_empty():
    df = load_performance('PerformanceData/Performance_20250321.csv')
    assert not df.empty

def test_summarize_performance_stats():
    df = load_performance('PerformanceData/Performance_20250321.csv')
    stats = summarize_performance(df)
    assert 'mean_return' in stats
    assert 'volatility' in stats
    assert 'max_drawdown' in stats
    assert isinstance(stats['mean_return'], float)
    assert isinstance(stats['volatility'], float)
    assert isinstance(stats['max_drawdown'], float)
