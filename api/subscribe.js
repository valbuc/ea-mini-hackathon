// Vercel serverless function — POST /api/subscribe
//
// Persists a subscriber (email, optional name, current filter preferences)
// to a Neon Postgres database. Existing emails are upserted so a user can
// refine their preferences by re-submitting the form.
//
// Schema (run once via the Neon SQL editor — see api/_schema.sql):
//
//   CREATE TABLE IF NOT EXISTS subscribers (
//     id          SERIAL PRIMARY KEY,
//     email       TEXT NOT NULL UNIQUE,
//     name        TEXT,
//     preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
//     created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//     updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
//   );

import { neon } from "@neondatabase/serverless";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Vercel's Neon integration injects DATABASE_URL; older Vercel Postgres
// projects also expose POSTGRES_URL. Fall back so either flow works.
const connectionString = process.env.DATABASE_URL || process.env.POSTGRES_URL;
const sql = connectionString ? neon(connectionString) : null;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  if (!sql) {
    console.error("No DATABASE_URL / POSTGRES_URL env var configured.");
    return res.status(500).json({ error: "Database not configured" });
  }

  let body = req.body;
  if (typeof body === "string") {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  const email = typeof body.email === "string" ? body.email.trim().toLowerCase() : "";
  const name = typeof body.name === "string" ? body.name.trim() : null;
  const preferences = body.preferences && typeof body.preferences === "object" ? body.preferences : {};

  if (!EMAIL_RE.test(email) || email.length > 320) {
    return res.status(400).json({ error: "Valid email required" });
  }
  if (name && name.length > 200) {
    return res.status(400).json({ error: "Name too long" });
  }

  try {
    await sql`
      INSERT INTO subscribers (email, name, preferences)
      VALUES (${email}, ${name}, ${JSON.stringify(preferences)}::jsonb)
      ON CONFLICT (email) DO UPDATE SET
        name        = EXCLUDED.name,
        preferences = EXCLUDED.preferences,
        updated_at  = NOW();
    `;
    return res.status(200).json({ success: true });
  } catch (err) {
    console.error("Subscribe insert failed:", err);
    return res.status(500).json({ error: "Could not save subscription" });
  }
}
