import pgPromise from "pg-promise";
import { pgConnString } from "@/app/config/config";

const pgp = pgPromise();

export const db = pgp(pgConnString);
