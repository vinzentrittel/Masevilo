# Codename: ClearMyBeach

This is an attempt to gather some people and clean up trash in as a group activity

## Calculate Map Tile Coordinates

To calculate the right tile indices from a given geo location, install mercantile:

    pip install mercantile

## Interactive Map Plugin

    pip install folium

## Matplotlib for Heatmap Overlay

    pip install matplotlib

To show the plotting from terminal, install python3-tk library

    sudo apt install python3-tk

## Make API calls

For the development process do API calls to (master.apis.dev.openstreetmap.org)[https://master.apis.dev.openstreetmap.org/].

Sample call:

    https://master.apis.dev.openstreetmap.org/api/0.6/map?bbox=1.2,1.2,1.3,1.3

## Pulling Map Tile Images

Parts of maps will be pulled from (thunderforest.com)[https://www.thunderforest.com]. Dedicated API key for up to 150,000 tile keys per month is

`c29d97b23bc04da4bb6b2a02dfc7c7e9`

Parallel downloading of all tiles from (a.tile.thunderforest.com)[https://a.tile.thunderforest.com], (b.tile.thunderforest.com)[https://b.tile.thunderforest.com] and (c.tile.thunderforest.com)[https://c.tile.thunderforest.com]. Important to note is, its prefixes, a, b and c. This is neccessarry to not be limited to 6-9 simultanious connections, as some browsers will tend to do.
To get a tile `x=3`, `y=3`, `z=3`, where x is zoom level between 0-22, get:
    
https://a.tile.thunderforest.com/cycle/3/3/3.png?apikey=XYZ
