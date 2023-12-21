### conditions needed for property access:

# ownership--city or private
# if "city_agency_owner" == "PLB" ~ "land bank"
# elif "city_agency_owner" == NA ~ "private owner"
# else "city, but too complicated"
    
# sold within last six months
# sale_date <= 6 months ago

# facing foreclosure (e.g., is the foreclosure column a Y)
# if "sheriff_sale" == "Y"

# has l&i violations for vacant, unsafe, and notorious

# has tax debt or delinquency?
# total_due != NA

# is it land or a building?
# if "parcel_type" == "Lot"
# else "parcel type" == "Building"

# what does it cost?
# if "market_value" < 1000 ~ "buy property"
# else "private land use agreement"