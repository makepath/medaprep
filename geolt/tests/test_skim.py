import pytest
import numpy as np
import xarray as xr
import pandas as pd
from pandas.testing import assert_series_equal

from geolt import skim


def create_input_dataset(seed=27) -> xr.Dataset:
    # create test dataset
    np.random.seed(seed)
    elevation = 5 * np.random.randn(2, 2, 3) + 10
    precipitation = 0.03 * np.random.rand(2, 2, 3) + 3
    temperature = 5 * np.random.rand(2, 2, 3) + 30
    precipitation[0, 1, :] *= np.nan
    lon = [[-99.83, -99.32], [-99.79, -99.23]]
    lat = [[42.25, 42.21], [42.63, 42.59]]
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
            CRS="EPSG:32615",
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


@pytest.fixture
def dataset_input():
    data = xr.concat(
        [create_input_dataset(seed=s) for s in range(5)],
        pd.Index([s for s in range(5)], name="sensor"),
    )
    return data


def skim_output():
    data = {
        "variables": ["elevation", "temperature", "precipitation"],
        "data_types": ["float64", "float64", "float64"],
        "NaNs": [False, False, True],
        "mean": [10.0, 30.0, 3.0],
        "std": [5.0, 5.0, 3.0],
    }
    df = pd.DataFrame(data)
    df["resolution"] = 10.0
    df["CRS"] = "EPSG:32615"
    return df


def test_skim(dataset_input):
    df_skim = skim(dataset_input)
    target = skim_output()
    assert_series_equal(df_skim["variables"], target["variables"])
    assert_series_equal(df_skim["data_types"], target["data_types"])
    assert_series_equal(df_skim["NaNs"], target["NaNs"])
    assert_series_equal(df_skim["resolution"], target["resolution"])
    assert_series_equal(df_skim["CRS"], target["CRS"])
