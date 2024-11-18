const EMPTY_STRING = '';

export const maptilerApiKey =
  process.env.NEXT_PUBLIC_MAPTILER_KEY || EMPTY_STRING;

export const useStagingTiles = false;

export const googleCloudBucketName =
  process.env.GOOGLE_CLOUD_BUCKET_NAME || 'cleanandgreenphl';
