const EMPTY_STRING = "";

export const mapboxAccessToken =
  "pk.eyJ1IjoibmxlYm92aXRzIiwiYSI6ImNsZXQ2Nzd3ZDBjZnYzcHFvYXhib2RqYzQifQ.PWg2LuNCH1E6-REjmYvdOg" ||
  EMPTY_STRING;

export const pgConnString = process.env.VACANT_LOTS_DB || EMPTY_STRING;

export const apiBaseUrl =
  process.env.NEXT_PUBLIC_VACANT_LOTS_API_BASE_URL || EMPTY_STRING;

export const finalDataset = "vacant_properties_end";

export const localTiles = true;
