import pgPromise from "pg-promise";
import { pgConnString } from "@/config/config";

const pgp = pgPromise();

export const db = pgp(pgConnString);
