import pytest
import folium
import folium.plugins

from porcupine import visualize.query as vq


@pytest.fixture
def create_single_input():
    bbox = (
        -98.64490090090091,
        29.365099099099098,
        -96.84309909909909,
        31.1669009009009,
    )
    return bbox


@pytest.fixture
def create_multiple_input():
    bboxs = {
        "Query": (
            -98.64490090090091,
            29.365099099099098,
            -96.84309909909909,
            31.1669009009009,
        ),
        "Returned": (
            -99.00020036474238,
            28.8021464220105,
            -95.7356923552778,
            31.63553809078258,
        ),
    }
    return bboxs


def test_visualize_query_single(create_single_input):
    m = vq(create_single_input)
    assert m.get_bounds()


def test_visualize_query_multiple(create_multiple_input):
    m = vq(create_multiple_input)
    assert m.get_bounds()
