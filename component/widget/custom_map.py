import geopandas as gpd
import ipyvuetify as v
import numpy as np
from ipyleaflet import AwesomeIcon, GeoJSON, Marker, WidgetControl
from ipywidgets import Output
from sepal_ui import mapping as m
from shapely.geometry import Polygon

from component.scripts.scripts import *


class MapTile(v.Card):
    def __init__(self, parameters, *args, **kwargs):

        self.class_ = "pa-2 justify-center"

        super().__init__(*args, **kwargs)

        self.param = parameters
        self.map_ = m.SepalMap(gee=False)
        self.map_.default_style = {"cursor": "crosshair"}

        self.lat = None
        self.lon = None

        self.output = Output()
        control = WidgetControl(widget=self.output, position="topleft")
        self.map_.add_control(control)

        self.map_.on_interaction(self.return_coordinates)

        self.children = [self.map_]

    def get_square(self, width=1):

        # lon-lat
        ul = np.array([round_(self.lon, width, "lon"), round_(self.lat, width, "lat")])
        ur = ul + (width, 0)
        br = ul + (width, -width)
        bl = ul + (0, -width)

        coords = list(list(f) for f in [ul, ur, br, bl, ul])

        data = gpd.GeoDataFrame(geometry=[Polygon(coords)]).__geo_interface__

        geojson = GeoJSON(data=data, _metadata={"type": "square"}, name="AOI")
        geojson.__setattr__("_metadata", {"type": "square"})

        return geojson

    def return_coordinates(self, **kwargs):

        with self.output:
            self.output.clear_output()
            lat, lon = kwargs["coordinates"]

            lat = round(lat, 2)
            lon = round(lon, 2)

            print(f"lon:{lon}, lat: {lat}")

        if kwargs.get("type") == "click":

            # Remove markdown if there is one
            remove_layers_if(self.map_, "type", "marker", _metadata=True)
            remove_layers_if(self.map_, "type", "square", _metadata=True)

            self.lat, self.lon = kwargs.get("coordinates")

            marker_icon = AwesomeIcon(
                name="fas fa-bullseye",
                marker_color="darkred",
                icon_color="white",
                spin=False,
            )

            marker = Marker(
                location=kwargs.get("coordinates"),
                draggable=False,
                _metadata={"type": "marker"},
                name="AOI Point",
                icon=marker_icon,
            )

            marker.__setattr__("_metadata", {"type": "marker"})

            self.map_.add_layer(marker)

            # Create a square rounding the point
            self.map_.add_layer(self.get_square(width=self.param.required.grid))

            self.param.required.lat = round(self.lat, 2)
            self.param.required.lon = round(self.lon, 2)
