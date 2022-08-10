# -*- coding: utf-8 -*-
"""Skim module.

This module implements utility functions that provide high level details of
raster data.

This module is part of the core porcupine library and is intended to be called
by user code.

Todo:
"""
import pandas as pd
import xarray as xr


def features(indata: xr.Dataset) -> pd.DataFrame:
    """
    This function returns a dataframe with information about the variables,
    data types, null values, means, standard deviations, maximums, and
    minimums for a given dataset.

    Args:
        indata (xarray.Dataset): datset to be skimmed.

    Returns:
        (pandas.DataFrame): table containing basic information about the
        dataset.

    Example:

        .. code-block:: python

            >>> import numpy as np
            >>> import pandas as pd
            >>> import xarray as xr
            >>> from porcupine import skim

            >>> temp = 15 + 8 * np.random.randn(2, 2, 3)
            >>> precip = 10 * np.random.rand(2, 2, 3)
            >>> lon = [[-99.83, -99.32], [-99.79, -99.23]]
            >>> lat = [[42.25, 42.21], [42.63, 42.59]]
            >>> ds = xr.Dataset(
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

            >>> df = skim.features(ds)
            >>> df
                variables       data_types  NaNs    mean    std     maximums    minimums
            0   temperature     float64     False   14.3177 9.08339 30.3361     -7.76803
            1   precipitation   float64     False   4.62568 3.03081 9.89768     0.147005

    """
    variables = list(indata.data_vars)
    d = dict(indata.dtypes)
    types = [d[v] for v in list(indata.data_vars)]
    null_counts = indata.isnull().sum().to_array().data > 0
    mus = indata.mean().to_array().data
    stds = indata.std().to_array().data
    maxs = indata.max().to_array().data
    mins = indata.min().to_array().data

    data_dict = {
        "variables": variables,
        "data_types": types,
        "NaNs": null_counts,
        "mean": mus,
        "std": stds,
        "maximums": maxs,
        "minimums": mins,
    }
    df = pd.DataFrame(data_dict)
    return df
