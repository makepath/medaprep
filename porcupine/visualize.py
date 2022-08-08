import folium
import numpy as np
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
    """query takes in a list of bounding boxes (bbox), a list of names
    corresponding to the bounding boxes (name), and a folium map (m).
    It adds the bounding boxes to the map (m) with the corresponding
    names, and colors the boxes based on the list of colors (color). It then
    sets the bounds of the map based on the largest provided bounding box, and
    returns the map.

    Args:
        bbox (tuple(s)): containing (x1, y1, x2, y2)
            latitude and longitude coordinates of bounding boxes.
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
