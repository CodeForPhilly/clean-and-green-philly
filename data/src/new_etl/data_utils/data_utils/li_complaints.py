from constants.services import COMPLAINTS_SQL_QUERY


from data_utils.kde import apply_kde_to_primary


def li_complaints(primary_featurelayer):
    return apply_kde_to_primary(
        primary_featurelayer, "L and I Complaints", COMPLAINTS_SQL_QUERY
    )
