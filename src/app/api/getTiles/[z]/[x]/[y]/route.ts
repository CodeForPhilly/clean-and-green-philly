import { NextRequest, NextResponse } from "next/server";
import { useLocalTiles } from "@/config/config";
import getLocalTiles from "./getLocalTiles";
import generateTiles from "./generateTiles";

export const GET = async (req: NextRequest, { params }: { params: any }) => {
  const { z, x, y } = params;

  if (isNaN(z) || isNaN(x) || isNaN(y)) {
    return new NextResponse(null, { status: 400 });
  }

  try {
    if (useLocalTiles) {
      const tile = getLocalTiles(z, x, y);
      if (tile) {
        return new NextResponse(tile, {
          headers: {
            "Content-Type": "application/vnd.mapbox-vector-tile",
          },
        });
      } else {
        return new NextResponse(null, { status: 204 });
      }
    } else {
      const tile = await generateTiles(z, x, y);
      return new NextResponse(tile, {
        headers: {
          "Content-Type": "application/vnd.mapbox-vector-tile",
        },
      });
    }
  } catch (error: any) {
    console.error(error);
    return new NextResponse(error.message, { status: 500 });
  }
};
