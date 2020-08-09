"""

A module to measure distance

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

	Returns
	=======
	gdf: GeoDataFrame (user-defined projection)
	"""
	# gpd_a.crs = "epsg:4326"
	# gpd_b.crs = "epsg:4326"
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

# For multi-line geometry, the following will raise an error:
# Multi-part geometries do not provide a coordinate sequence
# See: dist2line.ipynb

# def dist_to_line(gpd_a, gpd_b, gpd_b_cols=['FULLNAME']):
# 	a = np.concatenate([np.array(geom.coords) for geom in gpd_a.geometry.to_list()])
# 	b = [np.array(geom.coords) for geom in gpd_b.geometry.to_list()]
# 	b_ix = tuple(itertools.chain.from_iterable([itertools.repeat(i,x) for i, x in enumerate(list(map(len, b)))]))
# 	b = np.concatenate(b)
# 	ckd_tree = cKDTree(b)
# 	dist, idx = ckd_tree.query(a, k=1)
# 	idx = itemgetter(*idx)(b_ix)
# 	gdf = pd.concat([gpd_a, gpd_b.loc[idx, gpd_b_cols].reset_index(drop=True), pd.Series(dist, name='dist2line')], axis=1)
# 	return gdf


