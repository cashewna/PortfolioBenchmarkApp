import pytest
import pandas as pd
from pathlib import Path
from src.main.domain.model.asset import Asset

@pytest.fixture
def resource_path() -> Path:
  path = Path("src/main/resources")
  if not path.exists():
    pytest.fail(f"Resource path {path} does not exist.")
  return path

@pytest.fixture
def mxwo_path(resource_path: Path) -> Path:
    """Path to the equities index data."""
    p = resource_path / "mxwo.csv"
    if not p.exists():
        pytest.fail(f"mxwo.csv not found at: {p.resolve()}")
    return p

@pytest.fixture
def sbwau_path(resource_path: Path) -> Path:
    """Path to the fixed income index data."""
    p = resource_path / "sbwau.csv"
    if not p.exists():
        pytest.fail(f"sbwau.csv not found at: {p.resolve()}")
    return p

def test_calculate_daily_returns(sbwau_path: Path):
   asset = Asset(name="SBWAU", filepath=sbwau_path)
   returns = asset.calculate_daily_returns()
   print(returns)
   assert isinstance(returns, pd.Series), "Daily returns should be a pandas Series."
   
  