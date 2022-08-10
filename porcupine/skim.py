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
