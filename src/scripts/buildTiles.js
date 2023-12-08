const { Pool } = require("pg");
const fs = require("fs");
const path = require("path");

const pgConnString = process.env.VACANT_LOTS_DB || EMPTY_STRING;
const finalDataset = "vacant_properties_end";

// PostgreSQL connection settings
const pool = new Pool({
  connectionString: pgConnString,
});

// Bounding box and zoom levels
const boundingBox = {
  minLat: 39.81873786024889,
  maxLat: 40.185092236527396,
  minLon: -75.42842835904274,
  maxLon: -74.8545199004561,
};
const zoomLevels = { minZoom: 10, maxZoom: 16 };

// Calculate tile range for given lat/lon
const long2tile = (lon, zoom) =>
  Math.floor(((lon + 180) / 360) * Math.pow(2, zoom));
const lat2tile = (lat, zoom) =>
  Math.floor(
    ((1 -
      Math.log(
        Math.tan((lat * Math.PI) / 180) + 1 / Math.cos((lat * Math.PI) / 180)
      ) /
        Math.PI) /
      2) *
      Math.pow(2, zoom)
  );

// Function to query and save a tile from PostGIS
const queryAndSaveTile = async (z, x, y) => {
  const query = `SELECT ST_AsMVT(tile, 'vacant_properties', 4096, 'geometry') FROM (
        SELECT 
          ST_AsMVTGeom(
            ST_Transform(geometry, 3857),
            ST_TileEnvelope(${z}, ${x}, ${y})
          ) AS geometry,
          *
        FROM ${finalDataset}
        WHERE ST_Intersects(
          ST_Transform(geometry, 3857),
          ST_TileEnvelope(${z}, ${x}, ${y})
        )
      ) AS tile;`;
  const client = await pool.connect();
  try {
    const res = await client.query(query);
    const tileData = res.rows[0].st_asmvt;
    const tilePath = path.join(
      __dirname,
      "..",
      "..",
      "public",
      "tiles",
      `${z}`,
      `${x}`
    );
    const fileName = `${y}.pbf`;
    const filePath = path.join(tilePath, fileName);
    fs.mkdirSync(tilePath, { recursive: true });
    fs.writeFileSync(filePath, tileData);
  } catch (error) {
    console.error(error);
    throw error;
  } finally {
    client.release();
  }
};

// Download all tiles
const downloadAllTiles = async () => {
  for (let z = zoomLevels.minZoom; z <= zoomLevels.maxZoom; z++) {
    const minX = long2tile(boundingBox.minLon, z);
    const maxX = long2tile(boundingBox.maxLon, z);
    const minY = lat2tile(boundingBox.maxLat, z);
    const maxY = lat2tile(boundingBox.minLat, z);
    console.log(`Downloading tiles for zoom level ${z}`);

    for (let x = minX; x <= maxX; x++) {
      for (let y = minY; y <= maxY; y++) {
        try {
          await queryAndSaveTile(z, x, y);
        } catch (error) {
          console.error(`Failed to download tile z${z}-x${x}-y${y}: ${error}`);
        }
      }
    }
  }
};

downloadAllTiles().catch((error) => {
  console.error(error);
  process.exit(1);
});
