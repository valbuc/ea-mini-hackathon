// Vercel serverless function — POST /api/subscribe
//
// Persists a subscriber (email, optional name, current filter preferences)
// to Vercel Postgres. Existing emails are upserted so a user can refine
// their preferences by re-submitting the form.
//
// Schema (run once via the Vercel dashboard SQL editor):
//
//   CREATE TABLE IF NOT EXISTS subscribers (
//     id          SERIAL PRIMARY KEY,
//     email       TEXT NOT NULL UNIQUE,
//     name        TEXT,
//     preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
//     created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
//     updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
//   );
//   CREATE INDEX IF NOT EXISTS subscribers_email_idx ON subscribers(email);

import { sql } from "@vercel/postgres";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
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
