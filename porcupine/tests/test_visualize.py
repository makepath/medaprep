# -*- coding: utf-8 -*-
"""Porcupine test suite for visualize module.

This module implements the test suite for porcupine's visualize module.

This module is intended to be executed by running pytest from the project's
root directory.

Todo:
    * Assert that bounds from folium are the bounds we expect.
"""
import colorcet as cc
import folium
import folium.plugins
import numpy as np
import pytest
from bokeh.layouts import layout
from bokeh.plotting import figure
from porcupine import skim, visualize
from scipy.stats import gaussian_kde


@pytest.fixture(name="create_single_input")
def fixture_create_single_input():
    """Test utility function to create a single input."""
    bbox = (
        -98.64490090090091,
        29.365099099099098,
        -96.84309909909909,
        31.1669009009009,
    )
    name = "Query"
    folium_map = folium.Map()
    color = "blue"
    return bbox, name, folium_map, color


@pytest.fixture(name="create_multiple_input")
def fixture_create_multiple_input():
    """Test utility function to create multiple inputs."""
    bbox = [
        (
            -98.64490090090091,
            29.365099099099098,
            -96.84309909909909,
            31.1669009009009,
        ),
        (
            -99.00020036474238,
            28.8021464220105,
            -95.7356923552778,
            31.63553809078258,
        ),
    ]
    names = ["Query", "Returned"]
    folium_map = folium.Map()
    colors = ["blue", "green"]

    return bbox, names, folium_map, colors


def test_visualize_query_single(create_single_input):
    """Test that visualizing a single query creates some bounds in the
    the output.
    """
    ins = create_single_input
    out = visualize.query(
        bbox=ins[0], name=ins[1], folium_map=ins[2], color=ins[3]
    )
    assert out.get_bounds()


def test_visualize_query_multiple(create_multiple_input):
    """Test that visualizing a multiple query creates some bounds in the
    output.
    """
    ins = create_multiple_input
    out = visualize.query(
        bbox=ins[0], name=ins[1], folium_map=ins[2], color=ins[3]
    )
    assert out.get_bounds()
