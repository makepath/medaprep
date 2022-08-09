# -*- coding: utf-8 -*-
"""Porcupine test suite for skim module.

This module implements the test suite for porcupine's skim module.

This module is intended to be executed by running pytest from the project's
root directory.

Todo:
"""
import pandas as pd
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


def test_skim(test_skim_df):
    """Test that skimming the constructed input matches the expected output."""
    target = skim_output()
    assert_series_equal(test_skim_df["variables"], target["variables"])
    assert_series_equal(test_skim_df["data_types"], target["data_types"])
    assert_series_equal(test_skim_df["NaNs"], target["NaNs"])
