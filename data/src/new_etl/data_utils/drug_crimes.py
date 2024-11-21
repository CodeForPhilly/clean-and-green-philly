from ..constants.services import DRUGCRIME_SQL_QUERY


from new_etl.data_utils.kde import apply_kde_to_primary


def drug_crimes(primary_featurelayer):
    return apply_kde_to_primary(
        primary_featurelayer, "Drug Crimes", DRUGCRIME_SQL_QUERY
    )
