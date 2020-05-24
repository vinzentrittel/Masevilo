import folium
from folium.raster_layers import ImageOverlay
from dataclasses import dataclass

from sys import argv


def wrap(value, min_value, max_value):
    """
    Project value onto interval from min_value to max_value.
    Out of bounds values will be wrapped around.
    """
    return ((value - min_value) % (max_value - min_value)) + min_value


def wrap_latitude(coordinate):
    """
    Project coordinate (latitude) onto interval [-90,90].
    """
    return wrap(coordinate, -90, 90)


def wrap_longitude(coordinate):
    """
    Project coordinate (longitude) onto interval [-90,90].
    """
    return wrap(coordinate, -180, 180)


@dataclass
class GeoLocation:
    def __init__(self, latitude, longitude):
        self._latitude = wrap_latitude(latitude)
        self._longitude = wrap_longitude(longitude)

    @property
    def tolist(self):
        return self.longitude, self.latitude

    def __add__(self, other: GeoLocation):
        return GeoLocation(self.latitude + other.latitude, self.longitude + other.longitude)

    def __sub__(self, other: GeoLocation):
        return GeoLocation(self.latitude - other.latitude, self.longitude + other.longitude)

    def __lt__(self, other):
        if self.latitude < other.latitude or self.longitude < other.longitude:
            return True
        return False

    def __gt__(self, other):
        if self.latitude > other.latitude or self.longitude > other.longitude:
            return True
        return False

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

def get_bounding_box(loc: GeoLocation, radius=1.0):
    """
    Construct a bounding box of around passed GeoLocation.
    Bounding box values will be provided on a scale from 
    """
    return [
        [wrap_latitude(loc.latitude - radius), wrap_longitude(loc.longitude - radius)],
        [wrap_latitude(loc.latitude + radius), wrap_longitude(loc.longitude + radius)],
    ]


class TrashMap:
    MAP_RADIUS = 0.5
    SCAN_LINES = 4000

    def __init__(self, center: GeoLocation, radius=MAP_RADIUS, *, scanlines=SCAN_LINES):
        self.radius = radius
        self.center = center

        line = lambda: [0 for _ in range(scanlines)]
        self.map = [line() for _ in range(scanlines)]

    def add(self, location: GeoLocation, value=1):
        if location in self:

    def __contains__(self, location: GeoLocation):
        if location < self.center - self.radius or location > self.center + self.radius:
            return False
        return True


if __name__ == "__main__":
    """ some testing """
    bingen = GeoLocation(float(argv[1]), float(argv[2]))

    m = folium.Map(loacation=bingen.tolist)
    overlay = ImageOverlay(
        "overlay.png", get_bounding_box(bingen, float(argv[3])), opacity=0.5
    )

    m.add_child(overlay)

    m.save("index.html")

    m = TrashMap(0, 0)
