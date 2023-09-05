from classes.featurelayer import FeatureLayer
from constants.services import DELINQUENCIES_QUERY


def deliquencies(primary_featurelayer):
    tax_deliquencies = FeatureLayer(
        name="Property Tax Delinquencies", carto_sql_queries=DELINQUENCIES_QUERY, use_wkb_geom_field="the_geom"
    )

    red_cols_to_keep = ['opa_number', 
                    'total_due', 
                    'is_actionable',
                    'payment_agreement', 
                    'num_years_owed', 
                    'most_recent_year_owed', 
                    'total_assessment',
                    'sheriff_sale', 'geometry']
    
    tax_deliquencies.gdf = tax_deliquencies.gdf[red_cols_to_keep]

    primary_featurelayer.spatial_join(tax_deliquencies)

    return primary_featurelayer
