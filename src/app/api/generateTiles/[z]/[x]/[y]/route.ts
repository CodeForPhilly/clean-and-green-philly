import { NextRequest, NextResponse } from "next/server";
import { db } from "@/app/api/db/db";
import { finalDataset } from "@/config/config";

export const GET = async (req: NextRequest, { params }: { params: any }) => {
  const { z, x, y } = params;

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
    return new NextResponse(tileData.st_asmvt, {
      headers: {
        "Content-Type": "application/vnd.mapbox-vector-tile",
      },
    });
  } catch (error: any) {
    console.error(error);
    return new NextResponse(error.message, { status: 500 });
  }
};
