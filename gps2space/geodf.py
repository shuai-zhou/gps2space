"""

A module to create gdf from df

"""
import warnings
import geopandas as gpd

def df_to_gdf(df, x='long', y='lat'):
	"""
	Transform raw Lat/Long data to GeoDataFrame
	
	Parameters
	==========
	df: DataFrame
	x: Latitude
	y: Longitude
	
	Returns
	=======
	gdf: Point GeoDataFrame (unprojected)
	"""
	gdf = gpd.GeoDataFrame(df,
			       geometry=gpd.points_from_xy(df[x], df[y]),
			       crs=("epsg:4326"))
	return gdf

