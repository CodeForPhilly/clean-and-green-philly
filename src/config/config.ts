const EMPTY_STRING = '';

export const mapboxAccessToken =
  'pk.eyJ1IjoibmxlYm92aXRzIiwiYSI6ImNsZXQ2Nzd3ZDBjZnYzcHFvYXhib2RqYzQifQ.PWg2LuNCH1E6-REjmYvdOg';

export const maptilerApiKey =
  process.env.NEXT_PUBLIC_MAPTILER_KEY || EMPTY_STRING;

export const useStagingTiles = false;

export const googleCloudBucketName =
  process.env.GOOGLE_CLOUD_BUCKET_NAME || 'cleanandgreenphl';
