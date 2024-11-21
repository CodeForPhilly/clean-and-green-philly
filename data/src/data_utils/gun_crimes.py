from constants.services import GUNCRIME_SQL_QUERY


from data_utils.kde import apply_kde_to_primary


def gun_crimes(primary_featurelayer):
    return apply_kde_to_primary(primary_featurelayer, "Gun Crimes", GUNCRIME_SQL_QUERY)
