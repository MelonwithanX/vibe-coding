import pandas as pd
import numpy as np

def load_performance(filepath):
    """
    Reads a Performance CSV file, detects the correct header row, and returns a pandas DataFrame
    with columns: Date, Account, Return.
    """
    # Read file, find header row
    with open(filepath, 'r') as f:
        lines = f.readlines()
    header_idx = None
    for idx, line in enumerate(lines):
        if line.startswith('Time Period Performance Statistics,Header,Date'):
            header_idx = idx
            break
    if header_idx is None:
        raise ValueError("Header row not found in file: {}".format(filepath))
    # Read into DataFrame
    df = pd.read_csv(filepath, skiprows=header_idx+1, names=['Type','SubType','Date','Account','Return'])
    # Only keep rows with 'Time Period Performance Statistics,Data'
    df = df[(df['Type'] == 'Time Period Performance Statistics') & (df['SubType'] == 'Data')]
    df = df[['Date','Account','Return']]
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Return'] = pd.to_numeric(df['Return'], errors='coerce')
    df = df.dropna(subset=['Date','Return'])
    return df

def summarize_performance(df):
    """
    Given a DataFrame from load_performance, compute mean return, volatility (std), and max drawdown.
    Returns a dict.
    """
    mean_return = df['Return'].mean()
    volatility = df['Return'].std()
    # Calculate cumulative returns for drawdown
    cumulative = (1 + df['Return']).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    return {
        'mean_return': mean_return,
        'volatility': volatility,
        'max_drawdown': max_drawdown
    }


def load_concentration(filepath):
    """
    Reads a Concentration CSV file, detects the correct header row, and returns a pandas DataFrame
    with columns: SubSection, Symbol, Description, Sector, Value, ParsedWeight.
    Robust to extra/malformed lines.
    """
    data_rows = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('Concentration,Data,'):
                data_rows.append(line.strip().split(',', 7))
    df = pd.DataFrame(data_rows, columns=[
        'Type','SubType','SubSection','Symbol','Description','Sector','Value','ParsedWeight'])
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df['ParsedWeight'] = pd.to_numeric(df['ParsedWeight'], errors='coerce')
    df = df.dropna(subset=['Symbol','Value','ParsedWeight'])
    df['Symbol'] = df['Symbol'].str.strip()
    return df[['SubSection','Symbol','Description','Sector','Value','ParsedWeight']]

def summarize_concentration(df):
    """
    Exploratory analysis: summary stats and correlations for Value and ParsedWeight.
    Returns a dict with summary tables and correlation.
    """
    summary = df[['Value','ParsedWeight']].describe().to_dict()
    corr = df[['Value','ParsedWeight']].corr().to_dict()
    sector_summary = df.groupby('Sector')[['Value','ParsedWeight']].sum().reset_index()
    return {
        'summary': summary,
        'correlation': corr,
        'sector_summary': sector_summary
    }
