import pandas as pd
import xarray as xr


def skim(indata: xr.Dataset) -> pd.DataFrame:
    """
    This function returns a dataframe with information about the variables,
    data types, null values, means, standard deviations, maximums, and
    minimums for a given dataset.

    Args:
        indata (xarray.Dataset)

    Returns:
        skim_table (pandas.DataFrame) containing basic information about the
        dataset

    """
    variables = list(indata.data_vars)
    d = dict(indata.dtypes)
    types = [d[v] for v in list(indata.data_vars)]
    null_counts = indata.isnull().sum().to_array().data > 0
    mus = indata.mean().to_array().data
    stds = indata.std().to_array().data
    maxs = indata.max().to_array().data
    mins = indata.min().to_array().data
    CRS = indata.spatial_ref
    resolution = indata.x.values[1]-indata.x.values[0]

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
    df["resolution"] = resolution
    df["CRS"] = CRS
    return df
