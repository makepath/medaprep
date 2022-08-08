# -*- coding: utf-8 -*-
"""Porcupine test suite for skim module.

This module implements the test suite for porcupine's skim module.

This module is intended to be executed by running pytest from the project's
root directory.

Todo:
"""
import numpy as np
import pandas as pd
import pytest
import xarray as xr
from pandas.testing import assert_series_equal

from porcupine import skim


def create_input_dataset(seed=27) -> xr.Dataset:
    """Construct a test dataset to test against skim."""
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


@pytest.fixture(name="dataset_input")
def fixture_dataset_input():
    """Test fixture to create a test input dataset."""
    data = create_input_dataset()
    return data


def skim_output():
    """Create the output we expect from running skim to test against."""
    data = {
        "variables": ["elevation", "temperature", "precipitation"],
        "data_types": ["float64", "float64", "float64"],
        "NaNs": [False, False, True],
        "mean": [10.0, 30.0, 3.0],
        "std": [5.0, 5.0, 3.0],
    }
    df = pd.DataFrame(data)
    df["resolution"] = 10
    df["CRS"] = "EPSG:32615"
    return df


def test_skim(dataset_input):
    """Test that skimming the constructed input matches the expected output."""
    df_skim = skim.features(dataset_input)
    target = skim_output()
    assert_series_equal(df_skim["variables"], target["variables"])
    assert_series_equal(df_skim["data_types"], target["data_types"])
    assert_series_equal(df_skim["NaNs"], target["NaNs"])
