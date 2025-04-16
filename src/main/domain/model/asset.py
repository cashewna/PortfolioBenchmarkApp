import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Asset:
  """Represents a single asset with time series data."""

  def __init__(self, name: str, filepath: Path):
    self.name = name
    if not isinstance(filepath, Path):
      filepath = Path(filepath)
    self.filepath = filepath
    self.data = self._load_data()

  def _load_data(self) -> pd.Series:
    try:
      df = pd.read_csv(self.filepath, index_col='Date', parse_dates=True)
      # Sort the index chronologically to calculate returns correctly
      data_series = df['PX_LAST'].sort_index()
      return data_series
    except Exception as e:
      logging.error(f"Error loading data for {self.name}: {e}")
  
  def calculate_daily_returns(self) -> pd.Series:
    """Calculate daily returns for the asset."""
    daily_returns = self.data.pct_change()
    return daily_returns
  
  def get_price(self, date: pd.Timestamp) -> float:
    """Get the price of the asset on a specific date."""
    if date in self.data.index:
      return self.data.loc[date]
    else:
      logging.error(f"Date {date} not found in asset data.")
