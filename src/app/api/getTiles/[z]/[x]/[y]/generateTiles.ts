import { db } from "@/app/api/db/db";
import { finalDataset } from "@/config/config";

const generateTiles = async (z: number, x: number, y: number) => {
  try {
    const tileData = await db.one(
      `SELECT ST_AsMVT(tile, 'vacant_properties', 4096, 'geometry') FROM (
        SELECT 
          ST_AsMVTGeom(
            ST_Transform(geometry, 3857),
            ST_TileEnvelope($1, $2, $3)
          ) AS geometry,
          *
        FROM ${finalDataset}
        WHERE ST_Intersects(
          ST_Transform(geometry, 3857),
          ST_TileEnvelope($1, $2, $3)
        )
      ) AS tile;`,
      [z, x, y]
    );
    return tileData.st_asmvt;
  } catch (error: any) {
    console.error(error);
    throw new Error(error.message);
  }
};

export default generateTiles;
