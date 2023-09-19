import { NextRequest, NextResponse } from "next/server";
import { db } from "@/app/api/db/db";

export const GET = async (req: NextRequest, { params }: { params: any }) => {
  const { z, x, y } = params;

  const connection = await db.connect();
  try {
    const tileData = await connection.one(
      `SELECT ST_AsMVT(tile, 'vacant_properties', 4096, 'geometry') FROM (
        SELECT 
          ST_AsMVTGeom(
            ST_Transform(geometry, 3857),
            ST_TileEnvelope($1, $2, $3)
          ) AS geometry,
          *
        FROM vacant_properties_end
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
    return new NextResponse(error.message, { status: 500 });
  } finally {
    connection.done();
  }
};
