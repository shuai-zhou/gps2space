"""

A module to measure the nearest distance from point to point and polygon

"""
import itertools
import numpy as np
import pandas as pd
from operator import itemgetter
from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString

def dist_to_point(gpd_a, gpd_b, proj=2163):
	"""
	Perform distance measure from Point to nearest Point

	Parameters
	==========
	gpd_a: The GeoDataFrame you want to find their nearest points
	gpd_b: The GeoDataFrame from where you are looking for nearest points
	proj: Projection system

	Returns
	=======
	gdf: GeoDataFrame (user-defined projection)
	"""

	gpd_a = gpd_a.to_crs(epsg=proj)
	gpd_b = gpd_b.to_crs(epsg=proj)
	n_a = np.array(list(zip(gpd_a.geometry.x, gpd_a.geometry.y)))
	n_b = np.array(list(zip(gpd_b.geometry.x, gpd_b.geometry.y)))
	tree_b = cKDTree(n_b)
	dist, idx = tree_b.query(n_a, k=1)
	gdf = pd.concat([gpd_a.reset_index(drop=True), \
                     gpd_b.loc[idx, gpd_b.columns != 'geometry'].reset_index(drop=True), \
                     pd.Series(dist, name='dist2point')], axis=1)
	return gdf

def closest_poly(x, gdf_target, spatial_index, search_radius=None):

	"""
	Detect the nearest polygons based on SEARCH_RADIUS (buffer size)

	Parameters
	==========
	gdf_target: The GeoDataFrame from which you want to find the nearest polygons
	spatial_index: Spatial index of the gpd_target GeoPandas dataframe
	search_radius: Search radius, i.e., the buffer size to buffer point features

	Returns
	=======
	xxx: xxx
	"""

    # SEARCH_RADIUS in meters
	search_radius = search_radius
	bbox = x.buffer(search_radius, cap_style=3)
	possible_matches_index = list(spatial_index.intersection(bbox.bounds))

    # If no intersection, return NaN
	if len(possible_matches_index) == 0:
		return None

    # If has intersections, return the minimum distance
	else:
		possible_matches = gdf_target.iloc[possible_matches_index]
		return possible_matches.distance(x).min()

def dist_to_poly(gdf_source, gdf_target, proj=2163, search_radius=None):
	"""
	Perform the nearest distance measures from a source GeoPandas dataframe to a target GeoPandas dataframe

	Parameters
	==========
	gdf_souruce: The source GeoDataFrame contains point features
	gpd_target: The GeoDataFrame from which you want to find the nearest polygons from the gdf_source
	proj: Projection system
	search_radius: Search radius, i.e., the buffer size to buffer point features

	Returns
	=======
	gdf: GeoDataFrame
	"""
    # Project GeoPandas dataframe and copy gdf_source
	gdf_source = gdf_source.to_crs(epsg=proj)
	gdf_target = gdf_target.to_crs(epsg=proj)
	gdf_dist = gdf_source.copy()

    # If SEARCH_RADIUS is not specified, iterate over all the features
	if not search_radius:
		gdf_dist['dist2poly'] = gdf_source.geometry.apply(
                                lambda x: gdf_target.distance(x).min())

    # If SEARCH_RADIUS is specified, keep those only within SEARCH_RADIUS, otherwise, make NaN
	else:
		spatial_index = gdf_target.sindex
		gdf_dist['dist2poly'] = gdf_source.geometry.apply(
                                lambda x: closest_poly(x, gdf_target, spatial_index, search_radius))

	return gdf_dist

