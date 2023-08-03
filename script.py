import requests
import geopandas as gpd
import pandas as pd
import datetime
from esridump.dumper import EsriDumper


# Set the CRS to use for all layers
use_crs = "EPSG:2272"


class FeatureLayer:
    '''
    FeatureLayer is a class to represent a GIS dataset. It can be initialized with a URL to an Esri Feature Service, a SQL query to Carto, or a GeoDataFrame. 
    '''

    def __init__(self, name, esri_rest_urls=None, carto_sql_queries=None, gdf=None, crs=use_crs):
        self.name = name
        self.esri_rest_urls = [esri_rest_urls] if isinstance(
            esri_rest_urls, str) else esri_rest_urls
        self.carto_sql_queries = [carto_sql_queries] if isinstance(
            carto_sql_queries, str) else carto_sql_queries
        self.gdf = gdf
        self.crs = crs

        inputs = [self.esri_rest_urls, self.carto_sql_queries, self.gdf]
        non_none_inputs = [i for i in inputs if i is not None]

        if len(non_none_inputs) != 1:
            raise ValueError(
                'Exactly one of esri_rest_urls, carto_sql_queries, or gdf must be provided.')

        if self.esri_rest_urls is not None:
            self.type = 'esri'
        elif self.carto_sql_queries is not None:
            self.type = 'carto'
        elif self.gdf is not None:
            self.type = 'gdf'

        self.load_data()

    def load_data(self):
        print(f'Loading data for {self.name}...')
        if self.type == 'gdf':
            self.gdf = gdf
        else:
            try:
                if self.type == 'esri':
                    if self.esri_rest_urls is None:
                        raise ValueError(
                            'Must provide a URL to load data from Esri')

                    gdfs = []
                    for url in self.esri_rest_urls:
                        self.dumper = EsriDumper(url)
                        features = [feature for feature in self.dumper]

                        geojson_features = {
                            "type": "FeatureCollection", "features": features}
                        gdfs.append(gpd.GeoDataFrame.from_features(
                            geojson_features, crs=self.crs))

                    self.gdf = pd.concat(gdfs, ignore_index=True)

                elif self.type == 'carto':
                    if self.carto_sql_queries is None:
                        raise ValueError(
                            'Must provide a SQL query to load data from Carto')

                    gdfs = []
                    for sql_query in self.carto_sql_queries:
                        response = requests.get(
                            "https://phl.carto.com/api/v2/sql", params={"q": sql_query})

                        data = response.json()["rows"]
                        df = pd.DataFrame(data)
                        gdf = gpd.GeoDataFrame(
                            df, geometry=gpd.points_from_xy(df.x, df.y), crs=self.crs)

                        gdfs.append(gdf)
                    self.gdf = pd.concat(gdfs, ignore_index=True)

            except Exception as e:
                print(f'Error loading data for {self.name}: {e}')
                self.gdf = None

    def spatial_join(self, other_layer, how='left', predicate='intersects'):
        '''
        Spatial joins in this script are generally left intersect joins.
        They also can create duplicates, so we drop duplicates after the join.
        Note: We may want to revisit the duplicates.
        '''
        self.gdf = gpd.sjoin(self.gdf, other_layer.gdf,
                             how=how, predicate=predicate)
        self.gdf.drop(columns=['index_right'], inplace=True)
        self.gdf.drop_duplicates(inplace=True)


'''
Load Vacant Properties Datasets
'''

vacant_props_layers_to_load = [
    'https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Land/FeatureServer/0/', 'https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Bldg/FeatureServer/0/']


vacant_properties = FeatureLayer(
    name="Vacant Properties", esri_rest_urls=vacant_props_layers_to_load)


# '''
# Load City Owned Properties
# '''
city_owned_properties = FeatureLayer(
    name='City Owned Properties', esri_rest_urls='https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/LAMAAssets/FeatureServer/0/')

# Discover which vacant properties are city owned using a spatial join
vacant_properties.spatial_join(city_owned_properties)

# There are some matches which aren't valid because of imprecise parcel boundaries. Use a match on OPA_ID and OPABRT to remove these.
vacant_properties.gdf = vacant_properties.gdf.loc[~((vacant_properties.gdf['OPABRT'].notnull()) & (
    vacant_properties.gdf['OPA_ID'] != vacant_properties.gdf['OPABRT']))]

# Note: This removes some entries from the dataset, need to revisit this


# '''
# Load PHS Data
# '''

phs_layers_to_load = [
    'https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_CommunityLandcare/FeatureServer/0/', 'https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_PhilaLandCare_Maintenance/FeatureServer/0/'
]

phs_properties = FeatureLayer(
    name="PHS Properties", esri_rest_urls=phs_layers_to_load)

phs_properties.gdf['COMM_PARTN'] = 'PHS'
phs_properties.gdf = phs_properties.gdf[['COMM_PARTN', 'geometry']]

vacant_properties.spatial_join(phs_properties)
vacant_properties.gdf['COMM_PARTN'].fillna('None', inplace=True)


# '''
# L&I Data
# '''

# # L&I Complaints
# one_year_ago = (datetime.datetime.now() -
#                 datetime.timedelta(days=365)).strftime("%Y-%m-%d")

# complaints_sql_query = f"SELECT address, service_request_id, subject, status, service_name, service_code, lat as y, lon as x FROM public_cases_fc WHERE requested_datetime >= '{one_year_ago}'"
# l_and_i_complaints = FeatureLayer(
#     name='L&I Complaints', carto_sql_queries=complaints_sql_query, type='carto')

# # filter for only Status = 'Open'
# l_and_i_complaints.gdf = l_and_i_complaints.gdf[l_and_i_complaints.gdf['status'] == 'Open']

# # collapse complaints_gdf by address and concatenate the violationcodetitle values into a list with a semicolon separator
# l_and_i_complaints.gdf = l_and_i_complaints.gdf.groupby('address')['service_name'].apply(
#     lambda x: '; '.join([val for val in x if val is not None])).reset_index()

# # rename the column to 'li_complaints'
# l_and_i_complaints.gdf.rename(
#     columns={'service_name': 'li_complaints'}, inplace=True)

# # L&I Code Violations
# violations_sql_query = f"SELECT parcel_id_num, casenumber, casecreateddate, casetype, casestatus, violationnumber, violationcodetitle, violationstatus, opa_account_num, address, opa_owner, geocode_x as x, geocode_y as y FROM violations WHERE violationdate >= '{one_year_ago}'"
# l_and_i_violations = FeatureLayer(
#     name='L&I Code Violations', carto_sql_queries=violations_sql_query, type='carto')

# # Manipulation of L&I data- not changed much from the original script
# all_violations_count_df = l_and_i_violations.gdf.groupby(
#     'opa_account_num').count().reset_index()[['opa_account_num', 'violationnumber']]
# all_violations_count_df = all_violations_count_df.rename(
#     columns={'violationnumber': 'all_violations_past_year'})
# l_and_i_violations.gdf = l_and_i_violations.gdf[(
#     l_and_i_violations.gdf['violationstatus'] == 'OPEN')]

# open_violations_count_df = l_and_i_violations.gdf.groupby(
#     'opa_account_num').count().reset_index()[['opa_account_num', 'violationnumber']]
# open_violations_count_df = open_violations_count_df.rename(
#     columns={'violationnumber': 'open_violations_past_year'})

# # join the all_violations_count_df and open_violations_count_df dataframes on opa_account_num
# violations_count_gdf = all_violations_count_df.merge(
#     open_violations_count_df, how='left', on='opa_account_num')

# # replace NaN values with 0
# violations_count_gdf.fillna(0, inplace=True)

# # convert the all_violations_past_year and open_violations_past_year columns to integers
# violations_count_gdf['all_violations_past_year'] = violations_count_gdf['all_violations_past_year'].astype(
#     int)
# violations_count_gdf['open_violations_past_year'] = violations_count_gdf['open_violations_past_year'].astype(
#     int)

# # collapse violations_gdf by address and concatenate the violationcodetitle values into a list with a semicolon separator
# violations_gdf = l_and_i_violations.gdf.groupby('opa_account_num')['violationcodetitle'].apply(
#     lambda x: '; '.join([val for val in x if val is not None])).reset_index()

# # rename the column to 'li_violations'
# violations_gdf.rename(
#     columns={'violationcodetitle': 'li_code_violations'}, inplace=True)
