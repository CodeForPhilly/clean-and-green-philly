import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export const GET = async (req: NextRequest, { params }: { params: any }) => {
  const { z, x, y } = params;

  try {
    const tilePath = path.join(
      process.cwd(),
      "public",
      "tiles",
      z.toString(),
      x.toString(),
      `${y}.pbf`
    );

    if (fs.existsSync(tilePath)) {
      const tile = fs.readFileSync(tilePath);

      return new NextResponse(tile, {
        headers: {
          "Content-Type": "application/vnd.mapbox-vector-tile",
        },
      });
    } else {
      return new NextResponse(null, { status: 204 }); // 204 No Content
    }
  } catch (error: any) {
    console.error(error);
    return new NextResponse(error.message, { status: 500 });
  }
};
