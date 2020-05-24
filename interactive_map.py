import folium
from folium.raster_layers import ImageOverlay
from dataclasses import dataclass

from sys import argv

@dataclass
class GeoLocation:
    longitude: float
    latitude: float

    @property
    def tolist(self):
        return self.longitude, self.latitude

def wrap(value, min_value, max_value):
    """
    Project value onto interval from min_value to max_value.
    Out of bounds values will be wrapped around.
    """
    return ((value - min_value) % (max_value - min_value)) + min_value

def get_bounding_box(loc: GeoLocation, radius=1.0):
    """
    Construct a bounding box of around passed GeoLocation.
    Bounding box values will be provided on a scale from 
    """
    wrap_lat = lambda v: wrap(v, -90, 90)
    wrap_lon = lambda v: wrap(v, -180, 180)
    return [
        [wrap_lat(loc.latitude - radius), wrap_lon(loc.longitude - radius)],
        [wrap_lat(loc.latitude + radius), wrap_lon(loc.longitude + radius)],
    ]

if __name__ == "__main__":
    """ some testing """
    bingen = GeoLocation(float(argv[1]), float(argv[2]))

    m = folium.Map(loacation=bingen.tolist)
    overlay = ImageOverlay(
        "overlay.png", get_bounding_box(bingen), opacity=0.5
    )

    m.add_child(overlay)

    m.save("index.html")
