import pytest
import pandas as pd
from pathlib import Path

from src.main.domain.model.asset import Asset
from src.main.domain.model.benchmark import Benchmark

@pytest.fixture
def resource_path() -> Path:
    """Provides the path to the test resources directory."""
    path = Path("src/main/resources")
    if not path.exists():
        pytest.fail(f"Resource directory not found at: {path.resolve()}")
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

@pytest.fixture
def spgsci_path(resource_path: Path) -> Path:
    """Path to the commodities index data."""
    p = resource_path / "spgsci.csv"
    if not p.exists():
        pytest.fail(f"spgsci.csv not found at: {p.resolve()}")
    return p

@pytest.fixture
def fund_x_component_definitions(mxwo_path: Path, sbwau_path: Path, spgsci_path: Path) -> dict:
    """Defines the components for Fund X: name -> (weight, path)"""
    return {
        "Equities": (0.50, mxwo_path),
        "Fixed Income": (0.30, sbwau_path),
        "Commodities": (0.20, spgsci_path),
    }

# --- Test Cases ---

def test_benchmark_creation_stores_properties(fund_x_component_definitions):
    """Tests that Benchmark correctly stores name, weights, and creates Assets."""
    benchmark_name = "Fund X"
    benchmark = Benchmark(name=benchmark_name, component_definitions=fund_x_component_definitions)

    assert benchmark.name == benchmark_name, "Benchmark name not stored correctly."

    assert set(benchmark.get_component_names()) == set(fund_x_component_definitions.keys()), \
        "Stored component names do not match input."

    for name, (weight, _) in fund_x_component_definitions.items():
        assert benchmark.get_component_weight(name) == weight, \
            f"Weight for component '{name}' is incorrect."

    for name in fund_x_component_definitions.keys():
        component_asset = benchmark.get_component_asset(name)
        assert isinstance(component_asset, Asset), \
            f"Component '{name}' should be an Asset instance."
        assert component_asset.name == name, \
            f"Asset name for component '{name}' should match component name."
        # Check if the correct path was used (optional but good)
        assert component_asset.filepath == fund_x_component_definitions[name][1]

def test_benchmark_creation_fails_with_empty_components():
    """Tests that creating a benchmark with no components raises an error."""
    with pytest.raises(ValueError, match="Benchmark must have at least one component"):
        Benchmark(name="Empty Fund", component_definitions={})