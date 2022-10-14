# setup 

      # manually set virtual environment
      # https://code.visualstudio.com/docs/python/environments
      {
        "python.defaultInterpreterPath": "c:/Users/Nissim/AppData/Local/ESRI/conda/envs/arcgispro-py3-vacant-lots-project/python39/python.exe"
      }

      # import statements
      import csv
      import arcpy
      import sys
      import os

      # set working directory
      working_directory = "c:/Users/Nissim/Desktop/Vacant Lots Project/vacant-lots-proj"

      # Set environment CRS to NAD 1983 (2011) StatePlane Pennsylvania South FIPS3702 (US Feet)
      arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 (2011) StatePlane Pennsylvania South FIPS3702 (US Feet)")

# import vacant lots

      # import vacant land indicators from maps.phl.data AGO as vac_land_indicators
      featureLayer = arcpy.MakeFeatureLayer_management("https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Vacant_Indicators_Land/FeatureServer/0",
                                                      "vac_land_indicators")

      # select by attribute for only city-owned lots
      arcpy.SelectLayerByAttribute_management("vac_land_indicators", 'SUBSET_SELECTION', 
                                              "OWNER1 LIKE '%PHILA%' And OWNER1 NOT LIKE '%SCHOOL%' And OWNER1 NOT LIKE '%LLC%' And OWNER1 NOT LIKE '%INC%' And OWNER1 NOT LIKE '%ARCH%' And OWNER1 NOT LIKE '%J%' And OWNER1 NOT LIKE '%CHURCH%' And OWNER1 NOT LIKE '%INVESTMENT%' And OWNER1 NOT LIKE '%ROXBOARD%' And OWNER1 NOT LIKE '%PROPERTY%' And OWNER1 NOT LIKE '%REAL ESTATE%' And OWNER1 NOT LIKE '%ELECTRIC%' And OWNER1 NOT LIKE '%ALLEGHANY%' And OWNER1 NOT LIKE '%SUBURBAN%' And OWNER1 NOT LIKE '%REVENUE%' And OWNER1 NOT LIKE '%TR%' And OWNER1 NOT LIKE '%MONOPOLY%'")

      # Write the selected features to a new feature class
      arcpy.CopyFeatures_management("vac_land_indicators", 'city_vac_land')

      #remove old layer
      arcpy.DeleteFeatures_management("city_vac_land_w_phs")

# phs land care

      # import crimes from maps.phl.data AGO as crimes
      featureLayer = arcpy.MakeFeatureLayer_management("https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/PHS_CommunityLandcare/FeatureServer/0",
                                                      "land_care")

# merge vac lots and land care

      # join phs land care to city vacant land
      arcpy.SpatialJoin_analysis("city_vac_land", "land_care", "city_vac_land_w_phs")

      # select by attribute for only null values in Comm_Partn column
      # NOTE: it is probably better to figure out how to do this by creating a new in_phs_lc column
      # but first I have to figure out how to do this
      arcpy.SelectLayerByAttribute_management("city_vac_land_w_phs", 'SUBSET_SELECTION', "Comm_Partn IS NULL") 
                                              
      # write the selected features to a new feature class
      arcpy.CopyFeatures_management("city_vac_land_w_phs", "city_non_phs_van_land")

# 311 calls

      # import 311 calls from maps.phl.data AGO as li_311_complaints
      featureLayer = arcpy.MakeFeatureLayer_management("https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/COMPLAINTS/FeatureServer/0",
                                                      "li_complaints")

      # select by attribute for only blight
      arcpy.SelectLayerByAttribute_management("li_complaints", 'SUBSET_SELECTION', 
                                              "CASESTATUS LIKE '%OPEN%' And COMPLAINTDATE >= timestamp '2022-04-06 00:00:00' And COMPLAINTCODENAME LIKE '%weeds%' Or COMPLAINTCODENAME LIKE '%rubbish%' Or COMPLAINTCODENAME LIKE '%garbage%' Or COMPLAINTCODENAME LIKE '%tire%' Or COMPLAINTCODENAME LIKE '%debris%' Or COMPLAINTCODENAME LIKE '%clean%' Or COMPLAINTCODENAME LIKE '%waste%' Or COMPLAINTCODENAME LIKE '%vegetation%' Or COMPLAINTCODENAME LIKE '%blight%' Or COMPLAINTCODENAME LIKE '%dumping%' Or COMPLAINTCODENAME LIKE '%scrap%'")

      # write the selected features to a new feature class
      arcpy.CopyFeatures_management("li_complaints", 'blight_complaints')

# gun crime

      # import crimes from maps.phl.data AGO as crimes
      featureLayer = arcpy.MakeFeatureLayer_management("https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/INCIDENTS_PART1_PART2/FeatureServer/0",
                                                      "crime")

      # select by attribute for only firearm crimes
      arcpy.SelectLayerByAttribute_management("crime", 'SUBSET_SELECTION',
                                              "UPPER(TEXT_GENERAL_CODE) = 'AGGRAVATED ASSAULT FIREARM' OR UPPER(TEXT_GENERAL_CODE) = 'ROBBERY FIREARM' AND DISPATCH_DATE_TIME >= timestamp '2021-10-06 00:00:00'")

      # Write the selected features to a new feature class
      arcpy.CopyFeatures_management("crime", 'recent_gun_crime')

      from arcpy.sa import *

      gun_crime_kde = KernelDensity("recent_gun_crime", "", 50, 5280, "SQUARE_FEET", "", "PLANAR")
      
      
      # https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/calculate-field.htm
      # https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/calculate-field-examples.htm
      # https://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/removelayer.htm
      
