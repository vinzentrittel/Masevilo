"""
Convenience function set to create an interactible folium map plugin.
It can handle geo marker display and creation.

Classes:
GeoLocation -- Entity to represent a single geo location (latitude, longitude)

Functions:
create_map -- factory function to create a folium map
add_marker_insertion -- converts map so that new markers can be inserted
add_markers -- add a list of new geo markers to a map
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Callable
from folium import plugins  # type: ignore # pylint: disable=import-error
import folium  # type: ignore # pylint: disable=import-error
from folium.plugins import MarkerCluster, FastMarkerCluster, LocateControl, Draw


@dataclass
class GeoLocation:
    """
    Data representation for latitude, longitude data tuple.
    Provides from_dict to translate json list of coordinates into GeoLocationList
    """

    latitude: float
    longitude: float

    @property
    def tolist(self):
        """ return as list [latitude, longitude]. """
        return [float(self.latitude), float(self.longitude)]

    def __str__(self):
        return f"lat: {self.latitude}, lon: {self.longitude}"

    @classmethod
    def from_dict(cls, locations):
        """ convert bulk json locations to a list of GeoLocations. """
        return [cls(loc["latitude"], loc["longitude"]) for loc in locations.values()]


def add_markers(geo_locations: List[GeoLocation], trash_map: folium.Map) -> folium.Map:
    """ add list of GeoLocation to a map plugin """
    locations = [loc.tolist for loc in geo_locations]
    # create a marker cluster called "Public toilet cluster"
    marker_cluster = FastMarkerCluster([])
	#add a marker for each toilet, add it to the cluster, not the map
    for each in locations:
        popup = '<b>remove trash</b><button type="button">Click Me!</button>'
        folium.Marker(each, popup=popup).add_to(marker_cluster)
    marker_cluster.add_to(trash_map)

    return trash_map


def add_marker_insertion(trash_map: folium.Map) -> folium.Map:
    """ transform a map to create markers on click events """
    popups = '<b>drouble click to <br>remove trash</b>'
    trash_map.add_child(folium.ClickForMarker(popup=popups))
    return trash_map


def create_map(
        center: GeoLocation,
        transform: Callable[[folium.Map], folium.Map] = (lambda x: x)
) -> folium.Map:
    """
    Create a folium map plugin, to display a world map and markers on the map.

    Keyword Arguments:
    center -- mid point of the map
    transform -- transformation function to put freshly created map through
    """
    new_map = folium.Map(location=center.tolist, tiles="OpenStreetMap")
    LocateControl().add_to(new_map)
    draw = Draw(export=True)
    draw.add_to(new_map)
    return transform(new_map)


if __name__ == "__main__":
    import json

    with open("file.json") as json_file:
        data = json.load(json_file)
    print("test1")
    data = GeoLocation.from_dict(data)
    print("test2")
    m = create_map(GeoLocation(52.52, 13.4049), add_marker_insertion)
    print("test3")
    m = add_markers(data, m)
    print("test4")
    m.save("index.html")
