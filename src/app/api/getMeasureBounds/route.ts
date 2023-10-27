// route.ts
import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";
import { pgConnString, finalDataset } from "@/config/config";

export const dynamic = "force-dynamic";

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
  const boundQuery = `SELECT MIN(${p}), MAX(${p}) FROM ${finalDataset};`;

  try {
    const result = await pool.query(boundQuery);
    return NextResponse.json(result.rows[0], { status: 200 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
};
