# -*- coding: utf-8 -*-
"""Visualize module for use with data processed by porcupine.

This module implements visualization functionality that enables displaying
the results of data processing outputs from porcupine.

This module is part of the core porcupine library and is intended to be called
by user code.

"""
import colorcet as cc
import folium
import numpy as np
import pandas as pd
import xarray as xr
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from scipy.stats import gaussian_kde
from shapely.geometry import box


def _convert_bounds(bbox: tuple) -> tuple:
    x1, y1, x2, y2 = bbox
    return ((y1, x1), (y2, x2))


def _compute_bounds(bboxs: list[tuple]) -> tuple:
    xs = []
    ys = []
    for b in bboxs:
        xs.append((b[0], b[1]))
        ys.append((b[1], b[3]))
    x1 = np.min(xs)
    x2 = np.max(xs)
    y1 = np.min(ys)
    y2 = np.max(ys)
    return (x1, y1, x2, y2)


def _compute_center(bbox):
    x1, y1, x2, y2 = bbox
    mu_x = (x1 + x2) / 2
    mu_y = (y1 + y2) / 2
    return (mu_y, mu_x)


def query(
    bbox: [tuple | list[tuple]],
    name: [str | list[str]],
    folium_map: folium.Map,
    color: [str | list[str]],
) -> folium.Map:
    """
    query takes in a list of bounding boxes (bbox), a list of names
    corresponding to the bounding boxes (name), and a folium map (m).
    It adds the bounding boxes to the map (m) with the corresponding
    names, and colors the boxes based on the list of colors (color). It then
    sets the bounds of the map based on the largest provided bounding box, and
    returns the map.

    Args:
        bbox (tuple(s)): containing (x1, y1, x2, y2) latitude and longitude
            coordinates of bounding boxes.
        name (str): containing a name for each bbox.
        m (folium.Map): map to plot boxes on.
        color (str): color for each bounding box.

    Returns:
        folium.Map containing bounding boxes

    """
    if not isinstance(bbox, list):
        bbox = [bbox]
    if not isinstance(name, list):
        name = [name]
    if not isinstance(color, list):
        color = [color]
    assert len(bbox) == len(name) == len(color)

    for (b, n, c) in zip(bbox, name, color):
        folium.GeoJson(
            box(*b),
            style_function=lambda x, color=c: dict(
                fill=False, weight=5, opacity=0.5, color=color
            ),
            name=n + " Center",
            tooltip=n,
        ).add_to(folium_map)

        folium.Marker(
            _compute_center(b),
            popup=n + " Center",
            icon=folium.Icon(color=c, icon="star"),
        ).add_to(folium_map)

    folium_map.fit_bounds(bounds=_convert_bounds(bbox[0]))
    return folium_map


def distributions(
    indata: xr.Dataset, skim_table: pd.DataFrame, sample_size: int
) -> list:
    """
    This function returns a list of bokeh figures containing
    estimated distributions of the variables within the
    dataset.

    Args:
        indata (xarray.Dataset): input data containing variables which
            distributions will be estimated from.
        skim_table (pandas.DataFrame): dataframe containing basic info about
            the dataset.

    Returns:
        Bokeh figures containing estimated distributions of each variable.

    """
    est_pdfs = []
    epsilon = 0.00001
    palette = [cc.rainbow[i * 15] for i in range(17)]
    for i, row in skim_table.iterrows():
        variable = row["variables"]
        min_val = row["minimums"]
        max_val = row["maximums"]
        data_np = indata[variable].to_dataframe()[variable].values
        if row["NaNs"]:
            data_np = data_np[~np.isnan(data_np)]
        pdf = gaussian_kde(data_np)
        x = np.linspace(int(min_val - 5.0), int(max_val + 20.0), sample_size)
        y = pdf(x)
        y /= np.sum(y) + epsilon
        p = figure(
            title=variable,
            height=300,
            width=900,
            x_range=(int(min_val - 5.0), int(max_val + 10.0)),
            toolbar_location="above",
            height_policy="auto",
        )
        source = ColumnDataSource(data=dict(x=x, y=y))
        p.patch(
            x="x",
            y="y",
            color=palette[i],
            alpha=0.6,
            line_color="black",
            source=source,
        )
        p.title.text_font_size = "25px"
        est_pdfs.append(p)
    return est_pdfs
