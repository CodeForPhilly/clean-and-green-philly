# Notes:
    # at some point, I'll run into an issue where simply counting back X number of months
    # requires me to import multiple years' worth of data. Should I just write that into
    # the script now (i.e., default to reading & combining 2 years worth of data
    #  and then counting back the appropriate number of months)?

# Steps

# 1) Import libraries
    # note: only necessary additional one is probably carto2gpd
        # if I set the script to read in layers from maps.phl.data, tho
        # then I won't need carto2gpd. see if I can do it this way for now.
        # tho there may be an opportunity to redo this later on in a non-arcgis-dependant way.

# Importing arcpy
import arcpy


##### 
# I can work on this later. Import datasets from local machine for now. 
# As mentioned you can connect to ArcGIS Online through the ArcGIS API for Python.
# The below is how to establish a connection to ArcGIS online.
from arcgis.gis import GIS
gis = GIS("https://www.arcgis.com", "UserName", "P@ssword123"")
#####


# Set the workspace environment
arcpy.env.workspace = 'C:/Data/Tongass'

# Get the current raster cell size setting and make sure it is a specific size for standard output.
if arcpy.env.cellSize != 30:
    arcpy.env.cellSize = 30

# Set environment CRS to NAD 1983 (2011) StatePlane Pennsylvania South FIPS3702 (US Feet)
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 (2011) StatePlane Pennsylvania South FIPS3702 (US Feet)")

##### 

# 3) Import datasets
aprx = arcpy.mpArcGISProject("CURRENT")
m = aprx.listMaps("Map")[0]
itemid = '2ec9f27bea254a428e4eb70e7650672d'
m.addDataFromPath("https://mycounty.maps.arcgis.com/home/item.html?id=" + itemid)

#shootings
https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/SHOOTINGS/FeatureServer

# OR
featureLayer = arcpy.MakeFeatureLayer_management("https://sampleserver6.arcgisonline.com/arcgis/rest/services/PoolPermits/FeatureServer/0", 
                                                 layer_name)

##### 

    # make sure to import all of these as shapefiles for easiest import, even if it takes a while
    # also poosible to just read them in directly from AGO assuming this code gets run directly in python

    # also double-check that these all in the correct CRS
        #can use arcpy.management.Project()

    # a) 311 calls
    # b) vacant lots
    # c) phs-owned lots
    # d) Philadelphia shootings

all_311_calls = geopandas.read_file('')

# https://metadata.phila.gov/#home/datasetdetails/5543864d20583086178c4e98/representationdetails/5762e19fa237544b2ecfe722/
# https://metadata.phila.gov/#home/datasetdetails/5543ca6d5c4ae4cd66d3ff52/representationdetails/5e5d50e0fbc9650019b56025/

all_vac_lots = geopandas.read_file('C:\Users\Nissim\Desktop\Vacant Lots Project\vacant_land_indicators/Vacant_Indicators_Land.shp')

phs_lots = geopandas.read_file('C:\Users\Nissim\Desktop\Vacant Lots Project\phs_lots/phs_lots.shp')

all_shootings = geopandas.read_file('C:\Users\Nissim\Desktop\Vacant Lots Project\shootings/shootings.shp')

all_crime = geopandas.read_file('C:\Users\Nissim\Desktop\Vacant Lots Project\phl_crime/incidents_par1_part2.shp')

# 3) clean vacant land indicators

    # a) filter by attribute using the following statement: 
        arcpy.management.SelectLayerByAttribute(
            "vacant_land_indicators", 
            "NEW_SELECTION", 
            "OWNER1 LIKE '%PHILA%' And OWNER1 NOT LIKE '%SCHOOL%' And OWNER1 NOT LIKE '%LLC%' And OWNER1 NOT LIKE '%INC%' And OWNER1 NOT LIKE '%ARCH%' And OWNER1 NOT LIKE '%J%' And OWNER1 NOT LIKE '%CHURCH%' And OWNER1 NOT LIKE '%INVESTMENT%' And OWNER1 NOT LIKE '%ROXBOARD%' And OWNER1 NOT LIKE '%PROPERTY%' And OWNER1 NOT LIKE '%REAL ESTATE%' And OWNER1 NOT LIKE '%ELECTRIC%' And OWNER1 NOT LIKE '%ALLEGHANY%' And OWNER1 NOT LIKE '%SUBURBAN%' And OWNER1 NOT LIKE '%REVENUE%' And OWNER1 NOT LIKE '%TR%' And OWNER1 NOT LIKE '%MONOPOLY%'", 
            None
            )

        # note: need to figure out how to make this case-insensitive

    # b) create a new layer from this select
    # c) save new layer as city_vac_lots

city_vac_lots = 

# 4) clean & filter 311 calls
    # a) first need to filter out coordinate pairs w/NA values 
    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view, 
        {selection_type}, 
        {where_clause}, 
        {invert_where_clause}
        )

        # note: need to figure out how to make this case-insensitive
    # c) create a new layer from this select
    # d) save new layer as blight_311_calls

blight_311_calls = 

# 5) clean phs lots
    # use arcpy.management.SelectLayerByAttribute()

# 6) join 311 calls, phs lots to vacant lots
    arcpy.analysis.SpatialJoin(
        target_features, 
        join_features, 
        out_feature_class, 
        {join_operation}, 
        {join_type}, 
        {field_mapping}, 
        {match_option}, 
        {search_radius}, 
        {distance_field_name}
        )

        # join one to many
        # keep all
    # name this layer city_owned_vacs_no_phs_w_complaints

# 7) filter vacant lots down
    arcpy.management.SelectLayerByAttribute(
        in_layer_or_view, 
        {selection_type}, 
        {where_clause}, 
        {invert_where_clause}
        )
    # filter to exclude null values in service_name
        # this removes lots w/o 311 complaints
    # will also need to filter for any w/values in phs-related column

# 8) clean shootings/gun crime (whichever you settle on)

# 9) create kde for shootings/gun crime

# 10) extract values to points

# 11) reclassify for ease of symbology (use Jenks breaks to handle skew/outliers)



# ----

# for visuals in report:
    # compare histograms of kde scores for city-owned lots vs. non-city owned lots
        # this can be used to hint at a more aggressive approach to vacancy enforcement
