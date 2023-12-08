import fs from "fs";
import path from "path";

const getLocalTiles = (z: number, x: number, y: number) => {
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

      return tile;
    } else {
      return null;
    }
  } catch (error: any) {
    console.error(error);
    throw new Error(error.message);
  }
};

export default getLocalTiles;
