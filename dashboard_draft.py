import pandas as pd
import geopandas as gpd
import arcgis
import carto2gpd
import esri2gpd

# import vacant lots data
# this is from AGO, not Carto, so we need to use the `arcgis` package to import it
# and then convert it to a gdf

# IMPORTANT:
# copy only the selected portion of the 'Query URL'. This ensures that that the data is not returned in the JSON format.

vac_lots_url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Vacant_Indicators_Land/FeatureServer/0"

vac_lots_gdf = esri2gpd.get(vac_lots_url, fields = ['ADDRESS', 'OWNER1', 'OWNER2']).to_crs(epsg=2272)

# import phs land care data
phs_landcare_url = "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/PHS_CommunityLandcare/FeatureServer/0"
phs_landcare_gdf = esri2gpd.get(phs_landcare_url, fields=['COMM_PARTN, SHAPE']).to_crs(epsg=2272)

vac_lots_gdf = gpd.sjoin(vac_lots_gdf, phs_landcare_gdf, how="left")

vac_lots_gdf['COMM_PARTN'] = vac_lots_gdf['COMM_PARTN'].fillna(0)

# pull public owners by string from OWNER1 column
pub_owners_1 = vac_lots_gdf[vac_lots_gdf['OWNER1'].str.contains('PHILA', na = False)]

pub_owners_1 = pub_owners_1[pub_owners_1['OWNER1'].str.contains('|'.join(['AUTH', 'LAND BANK', 'REDEV']), na = False)]

pub_owners_1 = pub_owners_1[~pub_owners_1['OWNER1'].str.contains('|'.join(['IND', 'None']), na = False)]

pub_owners_1 = pub_owners_1['OWNER1'].unique().tolist()

# pull public owners by string from OWNER2 column
pub_owners_2 = vac_lots_gdf[vac_lots_gdf['OWNER2'].str.contains('PHILA', na = False)]

pub_owners_2 = pub_owners_2[pub_owners_2['OWNER2'].str.contains('|'.join(['AUTH', 'LAND BANK', 'REDEV']), na = False)]

pub_owners_2 = pub_owners_2[~pub_owners_2['OWNER2'].str.contains('|'.join(['IND', 'None']), na = False)]

pub_owners_2 = pub_owners_2['OWNER2'].unique().tolist()

# concatenate
pub_owners = pub_owners_1 + pub_owners_2

# filter out None values; leave in final list variable form
# note: I *think* this is close enough, but it's not perfect
pub_owners = list(filter(lambda item: item is not None, pub_owners))

# define function for a new column indicating if a lot is publicly owned
def fun(vac_lots_gdf):
    if vac_lots_gdf['OWNER1'] in pub_owners or vac_lots_gdf['OWNER2'] in pub_owners:
        return 1 # public
    else:
        return 0 # private

# apply function
vac_lots_gdf['PUB_OWN'] = vac_lots_gdf.apply(fun, axis=1)

# define function for a new column indicating if land is public + PHS, public + non-PHS, or private

def f(vac_lots_gdf):
    if vac_lots_gdf['PUB_OWN'] == 1 and vac_lots_gdf['COMM_PARTN'] == 0:
        return 'Public, Non-PHS'
    elif vac_lots_gdf['PUB_OWN'] == 0 and vac_lots_gdf['COMM_PARTN'] == 0:
        return 'Private'
    else:
        return 'Public, PHS'

# apply the function
vac_lots_gdf['PUB_OR_PRIV'] = vac_lots_gdf.apply(f, axis=1)

# if you want a print-out of the first 100 rows
# vac_lots_gdf[1:100]

# if you want a hist of the distribution
# vac_lots_gdf['PUB_OR_PRIV'].value_counts().plot(kind='bar')

# filter for remaining important columns
vac_lots_gdf1 = vac_lots_gdf[['ADDRESS', 
                              'OWNER1',
                              'OWNER2',
                              'COMM_PARTN',
                              'PUB_OR_PRIV',
                              'geometry']]


# define a list of blight terms
blight = ['weed', 
        'rubbish', 
        'garbage',
        'tire',
        'debris',
        'clean',
        'waste',
        'vegetation',
        'dumping',
        'scrap',
        'auto',
         'vehicle',
         'graffiti',
         'dangerous',
         ]

# import 311 complaints from the last year
url = "https://phl.carto.com/api/v2/sql"

li_where = "requested_datetime > current_date - 365"

li_gdf = carto2gpd.get(url, 
                       "public_cases_fc", 
                        fields=['service_request_id',
                                "subject",
                                "status",
                                "service_name",
                                "service_code"], 
                        where=li_where)

li_gdf['status'] = li_gdf['status'].str.strip().str.lower()

li_gdf['service_name'] = li_gdf['service_name'].str.strip().str.lower()

# filter for only complaints that are still open and that are associated with blight
li_gdf = li_gdf[li_gdf['status'] == "open"]

li_gdf = li_gdf[li_gdf['service_name'].str.contains('|'.join(blight), regex=True)]

# plot, if you want to
# li_gdf.plot(column = "service_name", legend = True, figsize=(15, 15), alpha = 0.1)

# need to get rid of any null geometries in order to reproject
li_gdf = li_gdf[li_gdf.geometry.notnull()]

li_gdf.to_crs(epsg=2272)

# join vac lots to complaints

vac_lots_gdf1 = gpd.sjoin(vac_lots_gdf1, li_gdf.to_crs(epsg=2272), how="left")

# now filter out any lots that don't have a blight complaint

vac_lots_gdf2 = vac_lots_gdf1[~pd.isnull(vac_lots_gdf1['service_name'])]

vac_lots_gdf3 = vac_lots_gdf2.groupby(['ADDRESS'])['service_name'].apply(', '.join).reset_index()

vac_lots_gdf2[[
                'ADDRESS',
                'OWNER1',
                'OWNER2',
                'COMM_PARTN',
                'PUB_OR_PRIV',
                'geometry'
                ]]

vac_lots_gdf3 = vac_lots_gdf3.merge(vac_lots_gdf2, on='ADDRESS', how='left')

vac_lots_gdf3 = vac_lots_gdf3[[
                                'ADDRESS',
                                'service_name_x',
                                'OWNER1',
                                'OWNER2',
                                'COMM_PARTN',
                                'PUB_OR_PRIV',
                                'geometry'
                            ]]

vac_lots_gdf3 =  gpd.GeoDataFrame(vac_lots_gdf3, 
                                    geometry = "geometry")

vac_lots_gdf3 = vac_lots_gdf3.rename(columns={'service_name_x': 'SERVICE_NAME'})

# calculate centroids for export to arcgis
vac_lots_gdf3['CENTROIDS'] = vac_lots_gdf3.geometry.centroid

vac_lots_gdf3 = vac_lots_gdf3.drop(columns = ['geometry'])

vac_lots_gdf3 = gpd.GeoDataFrame(vac_lots_gdf3,
                                 geometry = 'CENTROIDS')

#import gun crime data

url = "https://phl.carto.com/api/v2/sql"

guncrime_where = "dispatch_date_time > current_date - 365"

guncrime_gdf = carto2gpd.get(url, "incidents_part1_part2", 
                    fields=['text_general_code', 
                           'dispatch_date'], 
                    where=guncrime_where)

# need to get rid of any null geometries in order to reproject
guncrime_gdf = guncrime_gdf[guncrime_gdf.geometry.notnull()]

guncrime_gdf = guncrime_gdf.to_crs(epsg=2272)

guncrime_gdf = guncrime_gdf[guncrime_gdf["text_general_code"].str.contains("Aggravated Assault Firearm|Robbery Firearm")]


import sklearn
from sklearn.neighbors import KernelDensity
import numpy as np
import matplotlib.pyplot as plt

# Get X and Y coordinates of well points
x_sk = guncrime_gdf["geometry"].x
y_sk = guncrime_gdf["geometry"].y

# Get minimum and maximum coordinate values of well points
min_x_sk, min_y_sk, max_x_sk, max_y_sk = guncrime_gdf.total_bounds

# Create a cell mesh grid
# Horizontal and vertical cell counts should be the same
XX_sk, YY_sk = np.mgrid[min_x_sk:max_x_sk:100j, min_y_sk:max_y_sk:100j]

# Create 2-D array of the coordinates (paired) of each cell in the mesh grid
positions_sk = np.vstack([XX_sk.ravel(), YY_sk.ravel()]).T

# Create 2-D array of the coordinate values of the well points
Xtrain_sk = np.vstack([x_sk, y_sk]).T

# Get kernel density estimator (can change parameters as desired)
kde_sk = KernelDensity(bandwidth = 5280, metric = 'euclidean', kernel = 'gaussian', algorithm = 'auto')

# Fit kernel density estimator to wells coordinates
kde_sk.fit(Xtrain_sk)

# Evaluate the estimator on coordinate pairs
Z_sk = np.exp(kde_sk.score_samples(positions_sk))

# Reshape the data to fit mesh grid
Z_sk = Z_sk.reshape(XX_sk.shape)

# Plot data
#fig, ax = plt.subplots(1, 1, figsize = (10, 10))
#ax.imshow(np.rot90(Z_sk), cmap = "RdPu", extent = [min_x_sk, max_x_sk, min_y_sk, max_y_sk])
#ax.plot(x_sk, y_sk, 'k.', markersize = 2, alpha = 0.1)
#plt.show()

import rasterio

def export_kde_raster(Z, XX, YY, min_x, max_x, min_y, max_y, proj, filename):
    '''Export and save a kernel density raster.'''

    # Flip array vertically and rotate 270 degrees
    Z_export = np.rot90(np.flip(Z, 0), 3)

    # Get resolution
    xres = (max_x - min_x) / len(XX)
    yres = (max_y - min_y) / len(YY)

    # Set transform
    transform = rasterio.Affine.translation(min_x - xres / 2, min_y - yres / 2) * rasterio.Affine.scale(xres, yres)

    # Export array as raster
    with rasterio.open(
            filename,
            mode = "w",
            driver = "GTiff",
            height = Z_export.shape[0],
            width = Z_export.shape[1],
            count = 1,
            dtype = Z_export.dtype,
            crs = proj,
            transform = transform,
    ) as new_dataset:
            new_dataset.write(Z_export, 1)

# Export raster
export_kde_raster(Z = Z_sk, XX = XX_sk, YY = YY_sk,
                  min_x = min_x_sk, max_x = max_x_sk, min_y = min_y_sk, max_y = max_y_sk,
                  proj = 2272, filename = "C:/Users/Nissim/Desktop/Vacant Lots Project/guncrime_kde_rast.tif")

from matplotlib import pyplot

kde_rast = rasterio.open("C:/Users/Nissim/Desktop/Vacant Lots Project/guncrime_kde_rast.tif")

from rasterio.plot import show

#fig, ax = plt.subplots(figsize=(5,5))
#show(kde_rast, ax = ax)

#guncrime_gdf.plot(figsize = (5,5))

#fig, ax = plt.subplots(figsize=(12,12))
#guncrime_gdf.plot(ax=ax, color='orangered', alpha = 0.5)
#show(kde_rast, ax=ax)

import rasterstats

vac_lots_gdf3['rast_val'] = rasterstats.point_query(vac_lots_gdf3, "C:/Users/Nissim/Desktop/Vacant Lots Project/guncrime_kde_rast.tif")

import mapclassify

# Define the number of classes
n_classes = 5

# Create a quantiles classifier
classifier = mapclassify.Quantiles.make(k = n_classes)

# Classify the data
vac_lots_gdf3['rast_val'] = vac_lots_gdf3[['rast_val']].apply(classifier)

# scale from 1-5 instead of 0-4
vac_lots_gdf3['rast_val'] = vac_lots_gdf3['rast_val'].replace([0, 1, 2, 3, 4], [1, 2, 3, 4, 5])

# map vap_lots_gd3 with rast_val as the color column

fig, ax = plt.subplots(figsize=(12,12))
vac_lots_gdf3.plot(ax=ax, column='rast_val', cmap='RdPu', legend=True)
show(kde_rast, ax=ax)


# create a dash app

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
import dash_bootstrap_components as dbc

# create a dash leaflet map with a slider

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("Vacant and Abandoned Properties in Philadelphia"),
            html.P("This map shows the location of vacant lots and abandoned buildings in Philadelphia. The color of the lots indicates the number of gun crimes that occurred within a 1 mile radius of the lot. The darker the color, the more gun crimes that occurred within a 1 mile radius of the lot. The slider allows you to change the year of the data. The data is from 2010-2019."),

# add a slider to the map that will filter the data by gun crime score associated with rast_val
            dcc.Slider(
                id='year-slider',
                min=vac_lots_gdf3['rast_val'].min(),
                max=vac_lots_gdf3['rast_val'].max(),   
                value=vac_lots_gdf3['rast_val'].min(),
                marks={str(rast_val): str(rast_val) for rast_val in vac_lots_gdf3['rast_val'].unique()},
                step=None
            ),

            html.Div(id='slider-output-container')
        ], width=3),
        dbc.Col([
            dl.Map(style={'width': '100%', 'height': '50vh'}, center=[39.9526, -75.1652], zoom=11, children=[
                dl.TileLayer(),
                dl.GeoJSON(data=vac_lots_gdf3.to_json(), id='geojson')
            ])
        ], width=9)
    ])
])

# add a callback to the map that will filter the data by the PUB_OR_PRIV column


# add 




@app.callback(
    dash.dependencies.Output('geojson', 'children'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_geojson(selected_year):
    filtered_df = vac_lots_gdf3[vac_lots_gdf3.rast_val == selected_year]
    return dlx.dicts_to_geojson(filtered_df.to_dict('records'))

if __name__ == '__main__':
    app.run_server(debug=True)


                    

