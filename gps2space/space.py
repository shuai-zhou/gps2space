"""

A module to measure activity space and shared space

"""
import warnings
import pandas as pd
import geopandas as gpd

# activity space based on buffer
def buffer_space(gdf, dist=0, dissolve='week', proj=2163):
	"""
	Perform activity space based on buffer method

	Parameters
	==========
	gdf: GeoDataFrame
	dist: buffer distance in meters
	dissolve: level of aggregating points to form polygon

	Returns
	=======
	gdf: Polygon GeoDataFrame (user-defined projection)
	"""
	# gdf.crs = ("epsg:4326")
	gdf = gdf.to_crs(epsg=proj)
	gdf['geometry'] = gdf.geometry.buffer(dist)
	polys = gdf.dissolve(by=[dissolve]).reset_index()
	polys['buff_area'] = polys['geometry'].area
	return polys

# activity space based on convex
def convex_space(gdf, group='week', proj=2163):
	"""
	Perform activity space based on convex method.

	Parameters
	==========
	gdf: GeoDataFrame
	dissolve: level of aggregating points to form polygon

	Returns
	=======
	gdf: Polygon GeoDataFrame (user-defined projection)
	"""
	groups = gdf.groupby(group)
	convex = groups.geometry.apply(lambda x: x.unary_union.convex_hull)
	convex = gpd.GeoDataFrame(convex.reset_index())
	convex = convex.set_crs(epsg=proj)
	convex['convx_area'] = convex['geometry'].area
	return convex

# activity space based on concave






