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
	Perform activity space based on convex hull method.

	Parameters
	==========
	gdf: GeoDataFrame
	group: level of aggregating points to form polygon

	Returns
	=======
	gdf: Polygon GeoDataFrame (user-defined projection)
	"""
	# Make a separate DataFrame from gdf, but remove geometry column
	# And drop duplicates in terms of the "group" parameter
	df_temp = gdf.drop('geometry', 1)
	# print(df_temp.head())
	df = df_temp.drop_duplicates(group)

	# Obtain the convex hull activity space
	gdf = gdf.to_crs(epsg=proj)
	groups = gdf.groupby(group)
	convex = groups.geometry.apply(lambda x: x.unary_union.convex_hull)
	convex = gpd.GeoDataFrame(convex.reset_index())
	convex['convex_area'] = convex['geometry'].area

	# Merge convex with gdf_temp on group to get the columns from original gdf
	convex = convex.merge(df, on=group)

	return convex

# activity space based on concave

