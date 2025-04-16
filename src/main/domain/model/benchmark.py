import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple # Use Tuple for definition type hint
import logging

# Import the Asset class we created
from .asset import Asset # Relative import within the same package

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Benchmark:
    """Represents the benchmark portfolio (e.g., Fund X)."""

    def __init__(self, name: str, component_definitions: Dict[str, Tuple[float, Path]]):
        """
        Initializes the Benchmark.

        Args:
            name (str): The name of the benchmark.
            component_definitions (Dict[str, Tuple[float, Path]]):
                A dictionary where keys are component names (str) and values
                are tuples of (weight: float, filepath: Path).
        """
        self.name = name
        self._weights: Dict[str, float] = {}
        self._component_assets: Dict[str, Asset] = {} # Stores the Asset objects

        if not component_definitions:
            logging.error("Attempted to create a Benchmark with no components.")
            raise ValueError("Benchmark must have at least one component.")

        logging.info(f"Creating Benchmark '{name}' with components: {list(component_definitions.keys())}")

        total_weight = 0.0
        for asset_name, (weight, filepath) in component_definitions.items():
            if weight < 0:
                 logging.error(f"Component '{asset_name}' has negative weight: {weight}")
                 raise ValueError(f"Component weight cannot be negative: {asset_name} ({weight})")

            # Store weight
            self._weights[asset_name] = weight
            total_weight += weight

            # Create and store the Asset object
            try:
                # Use the component name as the Asset name for consistency
                asset = Asset(name=asset_name, filepath=filepath)
                self._component_assets[asset_name] = asset
                logging.debug(f"Successfully created Asset for component '{asset_name}'.")
            except (FileNotFoundError, ValueError, Exception) as e:
                # If an Asset fails to load, re-raise the error - benchmark cannot be created.
                logging.error(f"Failed to load data for benchmark component '{asset_name}' from {filepath}: {e}", exc_info=True)
                # Decide: should benchmark creation fail if one asset fails? Yes, likely.
                raise ValueError(f"Failed to initialize component '{asset_name}'.") from e

        # Check if weights sum to approximately 1 (optional check)
        if not np.isclose(total_weight, 1.0):
             logging.warning(f"Benchmark '{name}' component weights sum to {total_weight}, which is not 1.0.")
             # Depending on requirements, you might raise ValueError here instead of just warning.

        logging.info(f"Benchmark '{name}' created successfully.")


    def get_component_names(self) -> List[str]:
        """Returns the names of the benchmark components."""
        return list(self._component_assets.keys())

    def get_component_weight(self, component_name: str) -> float:
        """Returns the weight of a specific component."""
        if component_name not in self._weights:
            raise KeyError(f"Component '{component_name}' not found in benchmark weights.")
        return self._weights[component_name]

    def get_component_asset(self, component_name: str) -> Asset:
        """Returns the Asset object for a specific component."""
        if component_name not in self._component_assets:
             raise KeyError(f"Component '{component_name}' not found in benchmark assets.")
        return self._component_assets[component_name]
