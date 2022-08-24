# -*- coding: utf-8 -*-
"""Skim module.

This module implements utility functions that provide high level details of
raster data.

This module is part of the core medaprep library and is intended to be called
by user code.

"""
import pandas as pd
import xarray as xr


def _dask_skim_memory(indata: xr.Dataset) -> pd.Series:
    """Skim memory of dask-backed Xarray Dataset."""
    ddf = indata.to_dask_dataframe()
    s = ddf.memory_usage().compute()
    return s


def _skim_memory(indata: xr.Dataset) -> pd.Series:
    """Skim memory of Xarray Dataset."""
    df = indata.to_dataframe()
    s = df.memory_usage()
    return s


def memory(indata: xr.Dataset) -> pd.Series:
    """
    This function uses utilities from pandas and dask (for dask-backed datasets)
    to check the memory size of the input dataset.

    Args:
        indata (xarray.Dataset): dataset to be skimmed.

    Returns:
        (pandas.Series): series containing number of bytes for each column.

    Example:

        .. code-block:: python

            >>> print(data)
                <xarray.Dataset>
                Dimensions:      (time: 1, y: 1142, x: 1137)
                Coordinates:
                    * y            (y) float64 3.716e+06 3.715e+06 ... 3.351e+06 3.351e+06
                    * x            (x) float64 -1.102e+07 -1.102e+07 ... -1.066e+07 -1.066e+07
                    spatial_ref  int32 3857
                    * time         (time) datetime64[ns] 2022-07-03T17:25:22
                Data variables:
                    visual       (time, y, x) uint8 dask.array<chunksize=(1, 1142, 1137), meta=np.ndarray>
                    B01          (time, y, x) uint16 dask.array<chunksize=(1, 1142, 1137), meta=np.ndarray>
            >>> print(skim.memory(data))
            Index          6576899
            visual         1298454
            B01            2596908
            spatial_ref    5193816
            dtype: int64

    """  # noqa: E501
    # check if input is xarray dataset
    assert isinstance(indata, xr.Dataset)

    # check if input is a dask xarray dataset
    if indata.chunks:
        return _dask_skim_memory(indata)
    else:
        return _skim_memory(indata)


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
            >>> from medaprep import skim

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

    """  # noqa: E501
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
