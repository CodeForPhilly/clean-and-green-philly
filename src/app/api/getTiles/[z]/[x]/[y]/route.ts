import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";
import { Storage } from "@google-cloud/storage";
import { localTiles } from "@/config/config";

const storage = new Storage();
const bucketName = "cleanandgreenphillytiles";

export const GET = async (req: NextRequest, { params }: { params: any }) => {
  const { z, x, y } = params;

  try {
    if (localTiles) {
      // Existing logic for local tiles
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
    } else {
      console.log("Fetching from Google Cloud Storage");
      // Logic to fetch from Google Cloud Storage
      const file = storage.bucket(bucketName).file(`tiles/${z}/${x}/${y}.pbf`);
      const [exists] = await file.exists();

      if (exists) {
        const [buffer] = await file.download();
        return new NextResponse(buffer, {
          headers: {
            "Content-Type": "application/vnd.mapbox-vector-tile",
          },
        });
      } else {
        return new NextResponse(null, { status: 204 }); // 204 No Content
      }
    }
  } catch (error: any) {
    console.error(error);
    return new NextResponse(error.message, { status: 500 });
  }
};
