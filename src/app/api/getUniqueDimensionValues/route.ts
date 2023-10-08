// route.ts
import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";
import { pgConnString, finalDataset } from "@/config/config";

const pool = new Pool({
  connectionString: pgConnString,
});

export const GET = async (req: NextRequest) => {
  const searchParams = req.nextUrl.searchParams;
  const p = searchParams.get("p");
  if (typeof p !== "string") {
    return NextResponse.json(
      { error: "Parameter p must be a string" },
      { status: 400 }
    );
  }
  const distinctQuery = `SELECT DISTINCT "${p}" FROM ${finalDataset} ORDER BY "${p}" ASC;`;

  try {
    const result = await pool.query(distinctQuery);
    const valuesArray = result.rows.map((row) => row[p] || "(null)");
    return NextResponse.json(valuesArray, { status: 200 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};
