import folium
import folium.plugins
import pytest

from porcupine import visualize


@pytest.fixture
def create_single_input():
    bbox = (
        -98.64490090090091,
        29.365099099099098,
        -96.84309909909909,
        31.1669009009009,
    )
    name = "Query"
    m = folium.Map()
    color = "blue"
    return bbox, name, m, color


@pytest.fixture
def create_multiple_input():
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
    m = folium.Map()
    colors = ["blue", "green"]

    return bbox, names, m, colors


def test_visualize_query_single(create_single_input):
    ins = create_single_input
    out = visualize.query(bbox=ins[0], name=ins[1], m=ins[2], color=ins[3])
    assert out.get_bounds()


def test_visualize_query_multiple(create_multiple_input):
    ins = create_multiple_input
    out = visualize.query(bbox=ins[0], name=ins[1], m=ins[2], color=ins[3])
    assert out.get_bounds()
