"""
GeoPandas Basic Operations Demonstration

This script demonstrates basic geospatial operations using GeoPandas including
loading data from various formats, coordinate system conversions, area calculations,
and writing spatial files.

Requirements: geopandas, shapely
"""

from __future__ import annotations

import io
import json
import tempfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon


print("\n" + "=" * 60)
print("GEOPANDAS BASIC OPERATIONS")
print("=" * 60)


# ============================================================
# CREATE GEODATAFRAME FROM SCRATCH
# ============================================================

print("\n" + "=" * 60)
print("CREATE GEODATAFRAME FROM SCRATCH")
print("=" * 60)

# Create points
points_data = {
    "city": ["New York", "Los Angeles", "Chicago", "Houston"],
    "population": [8336817, 3979576, 2693976, 2320268],
    "longitude": [-74.0060, -118.2437, -87.6298, -95.3698],
    "latitude": [40.7128, 34.0522, 41.8781, 29.7604],
}

df = pd.DataFrame(points_data)

# Convert to GeoDataFrame
geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
gdf_cities = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

print("Cities GeoDataFrame:")
print(gdf_cities)
print(f"\nCRS: {gdf_cities.crs}")


# ============================================================
# CREATE POLYGONS
# ============================================================

print("\n" + "=" * 60)
print("CREATE POLYGONS")
print("=" * 60)

# Create polygon regions
regions_data = {
    "name": ["Region A", "Region B", "Region C"],
    "geometry": [
        Polygon([(-74.1, 40.6), (-74.1, 40.8), (-73.9, 40.8), (-73.9, 40.6)]),
        Polygon([(-118.3, 33.9), (-118.3, 34.1), (-118.1, 34.1), (-118.1, 33.9)]),
        Polygon([(-87.7, 41.7), (-87.7, 41.9), (-87.5, 41.9), (-87.5, 41.7)]),
    ],
}

gdf_regions = gpd.GeoDataFrame(regions_data, crs="EPSG:4326")

print("Regions GeoDataFrame:")
print(gdf_regions)


# ============================================================
# LOAD FROM CSV WITH COORDINATES
# ============================================================

print("\n" + "=" * 60)
print("LOAD FROM CSV")
print("=" * 60)

csv_data = """name,lat,lon,value
Point A,40.7489,-73.9680,100
Point B,34.0522,-118.2437,200
Point C,41.8781,-87.6298,150
"""

df_csv = pd.read_csv(io.StringIO(csv_data))
gdf_from_csv = gpd.GeoDataFrame(
    df_csv,
    geometry=gpd.points_from_xy(df_csv["lon"], df_csv["lat"]),
    crs="EPSG:4326"
)

print("GeoDataFrame from CSV:")
print(gdf_from_csv)


# ============================================================
# LOAD FROM GEOJSON
# ============================================================

print("\n" + "=" * 60)
print("LOAD FROM GEOJSON")
print("=" * 60)

geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Location 1", "category": "Park"},
            "geometry": {
                "type": "Point",
                "coordinates": [-73.9851, 40.7589]
            }
        },
        {
            "type": "Feature",
            "properties": {"name": "Location 2", "category": "Museum"},
            "geometry": {
                "type": "Point",
                "coordinates": [-73.9626, 40.7794]
            }
        }
    ]
}

with tempfile.TemporaryDirectory() as tmp_dir:
    geojson_path = Path(tmp_dir) / "locations.geojson"
    geojson_path.write_text(json.dumps(geojson_data), encoding="utf-8")
    
    gdf_geojson = gpd.read_file(geojson_path)
    print("GeoDataFrame from GeoJSON:")
    print(gdf_geojson)


# ============================================================
# LOAD FROM SHAPEFILE
# ============================================================

print("\n" + "=" * 60)
print("LOAD/WRITE SHAPEFILE")
print("=" * 60)

# Write to shapefile, then read it back
with tempfile.TemporaryDirectory() as tmp_dir:
    shapefile_path = Path(tmp_dir) / "cities.shp"
    gdf_cities.to_file(shapefile_path)
    
    gdf_from_shp = gpd.read_file(shapefile_path)
    print("GeoDataFrame from Shapefile:")
    print(gdf_from_shp)


# ============================================================
# COORDINATE SYSTEM CONVERSION
# ============================================================

print("\n" + "=" * 60)
print("COORDINATE SYSTEM CONVERSION")
print("=" * 60)

# Original CRS (WGS84 - lat/lon)
print(f"Original CRS: {gdf_cities.crs}")
print(f"Original geometry (first point):\n{gdf_cities.geometry.iloc[0]}")

# Convert to Web Mercator (EPSG:3857)
gdf_web_mercator = gdf_cities.to_crs("EPSG:3857")
print(f"\nWeb Mercator CRS: {gdf_web_mercator.crs}")
print(f"Web Mercator geometry (first point):\n{gdf_web_mercator.geometry.iloc[0]}")

# Convert to UTM Zone 18N (for New York area - EPSG:32618)
gdf_utm = gdf_cities.to_crs("EPSG:32618")
print(f"\nUTM Zone 18N CRS: {gdf_utm.crs}")
print(f"UTM geometry (first point):\n{gdf_utm.geometry.iloc[0]}")

# Convert back to WGS84
gdf_back_to_wgs84 = gdf_utm.to_crs("EPSG:4326")
print(f"\nBack to WGS84: {gdf_back_to_wgs84.geometry.iloc[0]}")


# ============================================================
# AREA CALCULATIONS
# ============================================================

print("\n" + "=" * 60)
print("AREA CALCULATIONS")
print("=" * 60)

# Area in degrees (not meaningful for WGS84)
print("Areas in geographic CRS (degrees² - not meaningful):")
print(gdf_regions[["name", "geometry"]].copy().assign(area_deg2=gdf_regions.area))

# Convert to projected CRS for accurate area calculation
# Using Albers Equal Area for USA (EPSG:5070)
gdf_regions_projected = gdf_regions.to_crs("EPSG:5070")
gdf_regions_projected["area_m2"] = gdf_regions_projected.area
gdf_regions_projected["area_km2"] = gdf_regions_projected.area / 1_000_000

print("\nAreas in projected CRS (square meters and km²):")
print(gdf_regions_projected[["name", "area_m2", "area_km2"]])


# ============================================================
# SPATIAL OPERATIONS
# ============================================================

print("\n" + "=" * 60)
print("SPATIAL OPERATIONS")
print("=" * 60)

# Distance calculation (requires projected CRS)
gdf_cities_proj = gdf_cities.to_crs("EPSG:5070")
ny_point = gdf_cities_proj.geometry.iloc[0]
gdf_cities_proj["distance_from_ny_km"] = gdf_cities_proj.geometry.distance(ny_point) / 1000

print("Distance from New York (km):")
print(gdf_cities_proj[["city", "distance_from_ny_km"]])

# Buffer (create area around points)
gdf_cities_proj["buffer_50km"] = gdf_cities_proj.geometry.buffer(50000)  # 50 km
print("\nBuffers created (50km radius):")
print(gdf_cities_proj[["city", "buffer_50km"]])

# Centroid
gdf_regions_proj = gdf_regions.to_crs("EPSG:5070")
gdf_regions_proj["centroid"] = gdf_regions_proj.geometry.centroid
print("\nRegion centroids:")
print(gdf_regions_proj[["name", "centroid"]])

# Bounds
bounds = gdf_cities.geometry.bounds
print("\nBounding boxes (minx, miny, maxx, maxy):")
print(bounds)


# ============================================================
# SPATIAL JOINS
# ============================================================

print("\n" + "=" * 60)
print("SPATIAL JOINS")
print("=" * 60)

# Which cities are within which regions?
cities_in_regions = gpd.sjoin(gdf_cities, gdf_regions, how="left", predicate="within")
print("Cities within regions:")
print(cities_in_regions[["city", "name"]])


# ============================================================
# SPATIAL FILTERING
# ============================================================

print("\n" + "=" * 60)
print("SPATIAL FILTERING")
print("=" * 60)

# Create bounding box for filtering
bbox = Polygon([
    (-120, 33),
    (-120, 42),
    (-70, 42),
    (-70, 33)
])

# Filter points within bounding box
cities_in_bbox = gdf_cities[gdf_cities.geometry.within(bbox)]
print("Cities within bounding box:")
print(cities_in_bbox[["city"]])


# ============================================================
# GEOMETRIC PROPERTIES
# ============================================================

print("\n" + "=" * 60)
print("GEOMETRIC PROPERTIES")
print("=" * 60)

# Point properties
print("City locations:")
print(gdf_cities.assign(
    x=gdf_cities.geometry.x,
    y=gdf_cities.geometry.y
)[["city", "x", "y"]])

# Polygon properties
gdf_regions_proj = gdf_regions.to_crs("EPSG:5070")
print("\nPolygon properties:")
print(gdf_regions.assign(
    is_valid=gdf_regions.geometry.is_valid,
    area_deg2=gdf_regions.geometry.area,
    length=gdf_regions.geometry.length
)[["name", "is_valid", "area_deg2", "length"]])


# ============================================================
# WRITE TO VARIOUS FORMATS
# ============================================================

print("\n" + "=" * 60)
print("WRITE TO FILES")
print("=" * 60)

with tempfile.TemporaryDirectory() as tmp_dir:
    tmp_path = Path(tmp_dir)
    
    # Write to GeoJSON
    geojson_out = tmp_path / "output.geojson"
    gdf_cities.to_file(geojson_out, driver="GeoJSON")
    print(f"Written to GeoJSON: {geojson_out.name}")
    
    # Write to Shapefile
    shapefile_out = tmp_path / "output.shp"
    gdf_cities.to_file(shapefile_out, driver="ESRI Shapefile")
    print(f"Written to Shapefile: {shapefile_out.name}")
    
    # Write to GeoPackage
    gpkg_out = tmp_path / "output.gpkg"
    gdf_cities.to_file(gpkg_out, driver="GPKG", layer="cities")
    print(f"Written to GeoPackage: {gpkg_out.name}")
    
    # Read back to verify
    gdf_verify = gpd.read_file(geojson_out)
    print("\nVerified GeoJSON read:")
    print(gdf_verify.head())


# ============================================================
# COORDINATE REFERENCE SYSTEM INFO
# ============================================================

print("\n" + "=" * 60)
print("CRS INFORMATION")
print("=" * 60)

print(f"CRS Name: {gdf_cities.crs.name}")
print(f"CRS Type: {gdf_cities.crs.type_name}")
print(f"EPSG Code: {gdf_cities.crs.to_epsg()}")
print(f"Units: {gdf_cities.crs.axis_info[0].unit_name if gdf_cities.crs.axis_info else 'N/A'}")

# Common CRS examples
print("\nCommon CRS:")
print("  EPSG:4326 - WGS84 (lat/lon, global)")
print("  EPSG:3857 - Web Mercator (web maps)")
print("  EPSG:5070 - Albers Equal Area (USA)")
print("  EPSG:32618 - UTM Zone 18N (New York area)")


print("\n" + "=" * 60)
print("END OF GEOPANDAS DEMO")
print("=" * 60)
