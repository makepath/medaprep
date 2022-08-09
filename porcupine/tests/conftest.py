import numpy as np
import pandas as pd
import pytest
import xarray as xr

from porcupine import skim


def create_input_dataset(seed=27) -> xr.Dataset:
    """Construct a test xarray Dataset."""
    np.random.seed(seed)
    elevation = 5 * np.random.randn(2, 2, 3) + 10
    precipitation = 0.03 * np.random.rand(2, 2, 3) + 3
    temperature = 5 * np.random.rand(2, 2, 3) + 30
    precipitation[0, 1, :] *= np.nan
    lon = [[0.0, 100.0], [200.0, 300.0]]
    lat = [[0.0, 100.0], [200.0, 300.0]]
    time = pd.date_range("2022-08-01", periods=3)
    reference_time = pd.Timestamp("2022-10-10")

    ds = xr.Dataset(
        data_vars=dict(
            elevation=(["x", "y", "time"], elevation),
            temperature=(["x", "y", "time"], temperature),
            precipitation=(["x", "y", "time"], precipitation),
        ),
        coords=dict(
            lon=(["x", "y"], lon),
            lat=(["x", "y"], lat),
            time=time,
            reference_time=reference_time,
        ),
        attrs=dict(
            description="Weather related data.",
            spatial_ref="EPSG:32615",
            resolution=10.0,
            mu_elevation=10,
            std_elevation=5,
            mu_precipiation=3,
            std_precipitation=0.03,
            mu_temperature=30,
            std_temperature=5,
        ),
    )

    return ds


@pytest.fixture(name="test_dataset", scope="session")
def fixture_test_dataset():
    """Test fixture to create a test input dataset."""
    data = create_input_dataset()
    return data


@pytest.fixture(name="test_skim_df", scope="session")
def fixture_test_skim_df(test_dataset):
    """Test skim DataFrame."""
    df_skim = skim.features(test_dataset)
    return df_skim
