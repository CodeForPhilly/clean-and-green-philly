import geopandas as gpd

class FeatureLayer:
    def __init__(self, name):
        self.name = name
        self.gdf = None

    def set_gdf(self, gdf):
        """
        Set the GeoDataFrame for this FeatureLayer.
        """
        self.gdf = gdf

    def spatial_join(self, other_featurelayer):
        """
        Perform a spatial join between this FeatureLayer and another FeatureLayer.
        """
        if self.gdf is None or other_featurelayer.gdf is None:
            raise ValueError("Both FeatureLayers must have a GeoDataFrame set.")

        # Perform the spatial join
        joined_gdf = gpd.sjoin(self.gdf, other_featurelayer.gdf, how='inner', op='intersects')

        # Return the joined GeoDataFrame
        return joined_gdf