# -*- coding: utf-8 -*-
"""medaprep test suite for skim module.

This module implements the test suite for medaprep's skim module.

This module is intended to be executed by running pytest from the project's
root directory.

"""
import numpy as np
import pandas as pd
import xarray as xr
from medaprep import skim
from pandas.testing import assert_series_equal


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


def test_skim_features(test_dataset):
    """Test that skimming the constructed input matches the expected output."""
    target = skim_output()
    skim_df = skim.features(test_dataset)
    assert_series_equal(skim_df["variables"], target["variables"])
    assert_series_equal(skim_df["data_types"], target["data_types"])
    assert_series_equal(skim_df["NaNs"], target["NaNs"])


def skim_memory_input():
    """Create a sample input for skim memory."""
    temp = 15 + 8 * np.random.randn(2, 2, 3)
    precip = 10 * np.random.rand(2, 2, 3)
    lon = [[-99.83, -99.32], [-99.79, -99.23]]
    lat = [[42.25, 42.21], [42.63, 42.59]]
    ds = xr.Dataset(
            {
                "temperature": (["x", "y", "time"], temp),
                "precipitation": (["x", "y", "time"], precip),
                },
            coords={
                "lon": (["x", "y"], lon),
                "lat": (["x", "y"], lat),
                "time": pd.date_range("2014-09-06", periods=3),
                "reference_time": pd.Timestamp("2014-09-05"),
                },
            )
    return ds


def skim_memory_output():
    """Create the expected output from skim memory."""
    data = {
            "Index": 577,
            "temperature": 96,
            "precipitation": 96,
            "lon": 96,
            "lat": 96,
            "reference_time": 96
            }

    df = pd.Series(data)
    return df


#def test_skim_memory(test_xr_dataset):
 #   """Test skimming xarray dataset and returning memory in bytes."""
  #  target = skim_memory_output()
   # skim_memory_df = skim.memory(test_xr_dataset)
    #assert_series_equal(target, skim_memory_df)

