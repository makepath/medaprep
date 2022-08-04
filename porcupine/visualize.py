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
                style_function=lambda x: dict(fill=False, 
                    weight=1, 
                    opacity=0.5,
                    color=color[i]),
                name=name[i]).add_to(m)
    #automatically set bounds based on widest box
    bounds = _compute_bounds(bbox)
    m.fit_bounds(bounds=_convert_bounds(bounds))
    return m

