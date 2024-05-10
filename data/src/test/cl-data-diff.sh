# sanity test data-diff command line call

data-diff \
  $VACANT_LOTS_DB \
  public.vacant_properties \
  backup_.vacant_properties \
  -k opa_id \
  -k parcel_type \
  -c '%' \
  -m 'backup_.vacant_properties_diff' \
  --stats 
