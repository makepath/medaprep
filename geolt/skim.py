import xarray as xr
import pandas as pd


def skim(indata: xr.Dataset) -> pd.DataFrame:
    """
    'Skims' an Xarray dataset and returns basic checks: variables within the dataset, datatypes, if any NaNs are present in a variable, means and standard deviations of variables, resolution, and CRS of the data.

    Parameters
    ----------
    indata: xarray.Dataset

    Returns
    -------
    skim_table: pandas.DataFrame containing basic information about the dataset

    Examples
    --------

    .. sourcecode:: python

    """
    variables = list(indata.data_vars)
    d = dict(indata.dtypes)
    types = [d[v] for v in list(indata.data_vars)]
    null_counts = indata.isnull().sum().to_array().data > 0
    mus = indata.mean().to_array().data
    stds = indata.std().to_array().data
    maxs = indata.max().to_array().data
    mins = indata.min().to_array().data
    CRS = indata.CRS
    resolution = indata.resolution

    data_dict = {
        "variables": variables,
        "data_types": types,
        "NaNs": null_counts,
        "mean": mus,
        "std": stds,
        "maximums":maxs,
        "minimums":mins,
    }
    df = pd.DataFrame(data_dict)
    df["resolution"] = resolution
    df["CRS"] = CRS
    return df
