import folium
from shapely.geometry import box
import numpy as np

def _convert_bounds(bbox: tuple) -> tuple:
    x1, y1, x2, y2 = bbox
    return ((y1, x1), (y2, x2))

def _compute_bounds(bboxs:list[tuple])->tuple:
    xs = []
    ys = []
    for b in bboxs:
        xs.append((b[0],b[1]))
        ys.append((b[1],b[3]))
    x1 = np.min(xs)
    x2 = np.max(xs)
    y1 = np.min(ys)
    y2 = np.max(ys)
    return (x1, y1, x2, y2)

def query(bbox: [tuple|list[tuple]], name: [str|list[str]], m: folium.Map, color: [str|list[str]])->folium.Map:
    """query takes in a list of bounding boxes (bbox), a list of names corresponding to the bounding boxes (name),
    and a folium map (m). It adds the bounding boxes to the map (m) with the corresponding names, and colors the
    boxes based on the list of colors (color). It then sets the bounds of the map based on the largest provided
    bounding box, and returns the map.

    Args:
        bbox (tuple(s)): containing (x1, y1, x2, y2) latitude and longitude coordinates of bounding boxes.
        name (str): containing a name for each bbox.
        m (folium.Map): map to plot boxes on.
        color (str): color for each bounding box.

    Returns:
        folium.Map containing bounding boxes

    """
    if not isinstance(bbox,list):
        bbox = [bbox]
    if not isinstance(name,list):
        name = [name]
    if not isinstance(color,list):
        color = [color]
    assert len(bbox)==len(name)==len(color)
    
    for i in range(len(bbox)):
        folium.GeoJson(
                box(*bbox[i]),
                style_function=lambda x: dict(fill=True, 
                    weight=1, 
                    opacity=0.5,
                    color=color[i]),
                name=name[i]).add_to(m)
    #automatically set bounds based on widest box
    bounds = _compute_bounds(bbox)
    m.fit_bounds(bounds=_convert_bounds(bounds))
    return m
