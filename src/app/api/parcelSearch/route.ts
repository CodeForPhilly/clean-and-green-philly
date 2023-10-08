// route.ts
import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";
import { pgConnString, finalDataset } from "@/config/config";

const pool = new Pool({
  connectionString: pgConnString,
});

export const POST = async (req: NextRequest) => {
  const body = await req.json();
  const { xmin, ymin, xmax, ymax } = body;

  const query = `
    SELECT * FROM ${finalDataset}
    WHERE ST_Within(geometry, ST_MakeEnvelope($1, $2, $3, $4, 2272))
    LIMIT 20;
  `;

  try {
    const result = await pool.query(query, [xmin, ymin, xmax, ymax]);
    return NextResponse.json(result.rows, { status: 200 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};
