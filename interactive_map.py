from __future__ import annotations
import folium
import numpy as np
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

    def __add__(self, other):
        if isinstance(other, GeoLocation):
            return GeoLocation(self.latitude + other.latitude, self.longitude + other.longitude)
        else:
            return GeoLocation(self.latitude + other, self.longitude + other)

    def __sub__(self, other):
        if isinstance(other, GeoLocation):
            return GeoLocation(self.latitude - other.latitude, self.longitude - other.longitude)
        else:
            return GeoLocation(self.latitude - other, self.longitude - other)

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

    def __str__(self):
        return f"lat: {self._latitude}, lon: {self._longitude}"

def get_bounding_box(loc: GeoLocation, radius=1.0):
    """
    Construct a bounding box of around passed GeoLocation.
    Bounding box values will be provided on a scale from 
    """
    return [
        [wrap_latitude(loc.latitude - radius), wrap_longitude(loc.longitude - radius)],
        [wrap_latitude(loc.latitude + radius), wrap_longitude(loc.longitude + radius)],
    ]


def gaussian_filter(std_deviation=2, mean=0, size=7):
    variance = std_deviation * std_deviation
    factor = 1 / np.sqrt(2 * np.pi * variance)

    def gaussian_func(value, mean=mean, variance=variance, normalize=factor):
        deviation = value - mean
        return normalize * np.exp(-(deviation * deviation)/(2*variance))

    kernel = [gaussian_func(n) for n in range(-size // 2, size // 2)] 
    normalize = 1 / sum(kernel)
    return [normalize * value for value in kernel]


def filter_array(line, kernel):
    assert(len(kernel) % 2 == 1)
    radius = len(kernel) // 2
    new_line = [0 for _ in range(len(line))]
    for line_index in range(radius + 1, len(line) - radius):
        for kernel_index in range(-radius, radius + 1):
            current_index = line_index + kernel_index
            kernel_index_off = kernel_index + radius
            new_line[current_index] += kernel[kernel_index_off] * line[line_index]
    return new_line

class TrashMap:
    MAP_DIM = 0.5
    SCAN_LINES = 4000

    def __init__(self, origin: GeoLocation, dimension=MAP_DIM, *, scanlines=SCAN_LINES):
        self.dimension = dimension
        self.origin = origin
        self.scanlines = scanlines

        self.map = np.array([[0] * scanlines] * scanlines)

    def add(self, location: GeoLocation, value=1):
        if location in self:
            normal_location = location - self.origin
            index_x = round(normal_location.longitude * self.scanlines)
            index_y = round(normal_location.latitude * self.scanlines)
            self.map[index_y][index_x] += value


    def __contains__(self, location: GeoLocation):
        if location < self.origin or location > self.origin + self.dimension:
            return False
        return True

    def smooth(self):
        
        pass
        

if __name__ == "__main__":
    """ some testing """
    bingen = GeoLocation(float(argv[1]), float(argv[2]))

    m = folium.Map(loacation=bingen.tolist)
    overlay = ImageOverlay(
        "overlay.png", get_bounding_box(bingen, float(argv[3])), opacity=0.5
    )

    m.add_child(overlay)

    m.save("index.html")

    trash = TrashMap(GeoLocation(0,0))
    trash.add(GeoLocation(0.25, 0.25))
