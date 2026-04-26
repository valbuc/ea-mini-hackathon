# ImpactFeed

> Discoverable, EA-aware tracking of EU public consultations (extensible to other jurisdictions), with cause-area filtering and impact scoring so individuals and experts can act where it counts most.

Built for the **EAGx Stockholm 2026 mini hackathon** — 1 hour, 3 people.

---

## 1. The Problem

Lawmakers in the EU and most democracies are **constitutionally obliged** to consult citizens, experts, and civil society before adopting new laws or regulations. In the EU this is codified in [Article 11 of the Treaty on European Union](https://commission.europa.eu/about/service-standards-and-principles/transparency/consultations_en) and operationalised through the [Have Your Say](https://have-your-say.ec.europa.eu/index_en) portal, which has hosted every Commission consultation since November 2018.

In theory, this is one of the highest-leverage points an EA-aligned individual or expert can act: a well-argued submission can directly shape the wording of a law that affects hundreds of millions of people. In practice, the consultation pipeline is broken at almost every stage:

| Problem | What the evidence says | Source |
|---|---|---|
| **Citizens don't know consultations exist** | The European Commission's own 2019 Stocktaking identifies "lack of knowledge on behalf of the EU citizens with regards to the participatory opportunities" as the #1 problem of the consultation regime. | [European Court of Auditors — Have Your Say special report (2019)](https://op.europa.eu/webpub/eca/special-reports/public-participation-14-2019/en/) |
| **Dense legalese blocks ordinary participation** | Studies of EU consultations show citizen participation drops sharply when consultation documents use complex/technical language. | ['Have Your Say' in practice (Tandfonline, 2025)](https://www.tandfonline.com/doi/full/10.1080/23745118.2025.2471877) |
| **Lobbyists and industry dominate** | "Very limited participation of citizen groups… reduces the diversity of viewpoints and expertise provided to policymakers, potentially resulting in policy decisions less attentive to the public interest." | [Conceptualizing consultation approaches (Springer, 2020)](https://link.springer.com/article/10.1007/s11077-020-09382-3) |
| **Black-box afterward** | Citizens have no visibility into how their input was weighed, leaving little incentive to engage again. | [Public Consultations Unpacked (European Law Blog)](https://www.europeanlawblog.eu/pub/public-consultations-unpacked-the-commissions-participatory-regime-under-the-2021-better-regulation-agenda/release/1) |
| **Analysis is enormously expensive** | The UK government estimates manual analysis of its consultations consumes ~75,000 working days and **£20m / year**. | [AI tool 'Consult' — UK government case study](https://www.openaccessgovernment.org/ai-tool-consult-used-for-first-time-to-analyse-public-responses-in-government-consultation/192733/) |
| **AI-generated comment floods are an emerging threat** | Generative models can flood consultations with synthetic-but-plausible comments, drowning out genuine input. | [How AI/LLMs may impact transparency (WFD)](https://www.wfd.org/news/how-artificial-intelligence-and-large-language-models-may-impact-transparency) |

The EA community is well-positioned to do something about this: many of the most consequential consultations (AI governance, biosecurity, animal welfare, global health) are exactly the cause areas where EA-aligned experts have outsized counterfactual value — *if they know the consultation is happening*.

Today, **they usually don't**. The EA Forum surfaces individual consultations occasionally and ad-hoc (e.g. UK aid review, hen cages), but there is no systematic tracker.

---

## 2. The Existing Landscape

There are useful tools in this space, but each is built for a different audience. None aggregates *across jurisdictions* with an *EA cause-area lens* and an *opportunity-for-impact score*.

| Tool | Discovers consultations | Cross-jurisdiction | EA cause-aware | Impact-scored | Citizen-side | Free / OSS |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| [EU "Have Your Say" portal](https://have-your-say.ec.europa.eu/index_en) | ✅ EU only | ❌ | ❌ | ❌ | ✅ | ✅ |
| [gov.uk consultations](https://www.gov.uk/government/publications) | ✅ UK only | ❌ | ❌ | ❌ | ✅ | ✅ |
| EC directorate newsletters ([Digital](https://digital-strategy.ec.europa.eu/en/newsletters), [R&I](https://research-and-innovation.ec.europa.eu/news/stay-connected_en) etc.) | ✅ siloed by topic | ❌ | ❌ | ❌ | ✅ | ✅ |
| [Consult (UK Incubator for AI)](https://ai.gov.uk/our-work/government/) | ❌ (analyses responses) | ❌ | ❌ | ❌ | ❌ (gov-side) | ❌ |
| [Talk to the City (AI Objectives Inst.)](https://ai.objectives.institute/talk-to-the-city-landing) | ❌ (analyses responses) | ❌ | ❌ | ❌ | ❌ (gov-side) | ✅ |
| [PolicyPulse (academic)](https://arxiv.org/html/2505.23994v1) | ❌ (analyses discussions) | ❌ | ❌ | ❌ | ❌ (researcher-side) | ✅ |
| Quorum / Plural Policy (commercial) | ✅ broad | ✅ | ❌ | ❌ | ❌ (lobbyist-side) | ❌ |
| [EA Forum — Policy topic](https://forum.effectivealtruism.org/topics/policy) | Ad-hoc, occasional | Partial | ✅ | ❌ | ✅ | ✅ |
| **ImpactFeed (this project)** | ✅ EU at MVP, multi-jurisdiction post-v0 | ✅ (extensible) | ✅ | ✅ | ✅ | ✅ |

The wedge: **discovery + EA cause classification + opportunity score + opt-in alerts**, citizen-and-expert-facing, open source.

---

## 3. Our Idea

Build a tool that:

1. **Crawls** the websites and feeds of the EU Commission ("Have Your Say") for active consultations. Designed to extend to other jurisdictions (national EU member-state portals, UK, US federal rulemaking, etc.) post-v0.
2. **Aggregates** the results into a structured store.
3. **Classifies** each consultation against a borrowed [80,000 Hours / EA Forum](https://forum.effectivealtruism.org/topics/policy) cause-area taxonomy (multi-label).
4. **Scores** "opportunity for impact" using an LLM judgment against an explicit rubric — and **shows the reasoning** so users can override it.
5. **Publishes** through a clean website + opt-in email digests, with subscribers selecting cause areas and minimum impact thresholds.

Long-term (explicitly **out of MVP**): an opt-in expert directory that surfaces relevant consultations to subscribed experts. **No** automated cold outreach — that path is borderline spam, hurts trust, and runs into [EU AI Act](https://artificialintelligenceact.eu/) transparency obligations.

---

## 4. The 1-Hour Hackathon Build

### 4.1 What we ship in 60 minutes

A working **demo**, not a deployed product. The story: *"Here's a real list of open EU consultations, classified by EA cause area and scored for impact, with the reasoning you can read."*

### 4.2 Audience

EA-aligned individuals and individual experts (e.g. a biosecurity researcher who would respond to a relevant consultation if prompted). **Not** EA orgs with their own policy teams (v2 audience). **Not** the general public.

### 4.3 Initial cause areas (narrow on purpose)

Two only, multi-label:

- **AI governance & safety** — active EU AI Act delegated and implementing acts provide steady consultation flow.
- **Animal welfare / factory farming** — the EU regularly consults on cage bans, welfare labelling, transport rules.

Anything else → **Other** bucket, not surfaced in alerts.

### 4.4 Data source (v0)

**EU Have Your Say** only. No documented public API, so:

- **Plan A:** quick BeautifulSoup scrape of the open-consultations listing.
- **Plan B (fallback):** if the portal is JS-heavy / fights us inside 15 minutes, hand-curate ~10 real open consultations into `consultations.json`. The pipeline + UI is the demo, not the scraper.

Other jurisdictions (national EU member-state portals, UK, US federal rulemaking, etc.) are post-v0.

### 4.5 Impact scoring

LLM-judged (Claude), 1–5, with a written rationale visible to the user. Single number, multidimensional rubric:

| Dimension | What it captures |
|---|---|
| **Scope** | How many people / animals / future generations are affected? |
| **Reversibility** | Is this a one-shot decision or revisable later? |
| **Tractability** | Is the consultation genuinely open to influence, or rubber-stamping? |
| **Urgency** | Deadline proximity — and is there time for a quality response? |
| **Counterfactual** | Will EA-aligned voices likely otherwise be heard? (low → higher score) |

One Claude call per consultation: input is title + summary + cause tags + rubric; output is `{score: 1-5, rationale: string, dimension_notes: {...}}`. Scores are **not authoritative** — they are visible-reasoning suggestions users can disagree with.

### 4.6 Tech stack

| Layer | v0 (shipped) | Post-hackathon |
|---|---|---|
| Pipeline | Python + Anthropic SDK (Claude Opus 4.7), Pydantic structured output, prompt caching | Same |
| Consultation store | JSON (`data/scored.json`, committed) | Postgres |
| Scraper schedule | Run locally on demand | GitHub Actions cron, daily |
| Frontend | Single static `index.html` + vanilla JS, Inter font | Astro (post-v0) |
| Subscriber store | **Neon Postgres** (via Vercel Storage marketplace; `subscribers` table, see `api/_schema.sql`) | Same |
| Subscribe API | Vercel serverless function `api/subscribe.js` (Node, `@neondatabase/serverless`) | Same + send-digest cron |
| Hosting | **Vercel** (static + functions) | Same + custom domain |

---

### 4.6.1 Local development

```bash
# 1. Python deps + .env (one-time)
pip install -r requirements.txt
cp .env.example .env  # then fill in ANTHROPIC_API_KEY

# 2. Score consultations (re-run whenever data/consultations.json changes)
python -m pipeline.classify_and_score   # writes data/scored.json

# 3a. Static-only preview (no /api/subscribe — form submissions will fail)
python -m http.server 8000              # open http://localhost:8000/

# 3b. Full local stack (static + /api/subscribe). Requires the Vercel CLI.
cd api && npm install && cd ..          # install function deps once
npx vercel link                         # link to your Vercel project
npx vercel env pull api/.env.local      # pull DATABASE_URL into the function env
npx vercel dev                          # open http://localhost:3000/
```

### 4.6.2 Deploying to Vercel

One-time setup, ~5 minutes:

1. **Push to GitHub** (already done if you're reading this on github.com).
2. Go to [vercel.com/new](https://vercel.com/new), **Import** this repo. Framework preset: *Other*. Build settings: leave default. Click *Deploy*. The first deploy will make the static frontend live; `/api/subscribe` will return 500 until the database is connected.
3. In the project dashboard → **Storage** → *Create database* → **Postgres** (this provisions a managed Neon Postgres via Vercel's marketplace) → pick a region close to you → *Connect*. Vercel auto-injects `DATABASE_URL` (and friends) as env vars on all functions.
4. Open the new database → **Query** tab → paste the contents of `api/_schema.sql` and run it. (One `CREATE TABLE`, one `CREATE INDEX`.)
5. Trigger a fresh deploy (*Deployments* → ⋯ → *Redeploy*) so `/api/subscribe` picks up the new env vars.

After that, every push to `main` redeploys automatically.

To inspect subscribers: Vercel dashboard → your database → Query → `SELECT * FROM subscribers ORDER BY created_at DESC;`

### 4.7 60-minute task split (3 people)

| Time | Person A — Data | Person B — LLM | Person C — UI |
|---|---|---|---|
| 0–10 | Repo setup, scaffold dirs | Repo setup, draft scoring prompt | Repo setup, scaffold static page |
| 10–40 | Scrape Have Your Say → `consultations.json` (or hand-curate 10 if scraper fights you) | `classify_and_score.py`: reads JSON, calls Claude, writes `scored.json` | Page reads `scored.json`; filter by cause + min score; click row → show rationale |
| 40–50 | Help wherever stuck | Help wherever stuck | Add Tally subscribe embed |
| 50–60 | Integration test, demo dry-run | Integration test, demo dry-run | Integration test, demo dry-run |

### 4.8 Out of scope for v0 (deferred deliberately)

- Expert outreach bot and any automated cold contact
- Other jurisdictions: national EU member-state portals, UK, US federal rulemaking, etc. (post-v0)
- SQLite / database (JSON suffices for ~tens of consultations)
- Real email sending — subscriptions are persisted to Postgres, but no digest is mailed yet (v1 = Resend, weekly Monday digest)
- Cron / hosting for the scraper (v1 = GitHub Action)
- Multilingual (EU consultations are normally available in English)
- "Did my comment matter?" — scrape final adopted text, LLM-map which submitted themes survived (v3)
- AI-generated comment / astroturf detection on the response side
- User accounts (preferences encoded in the subscribe form)

### 4.9 Sustainability / handoff

TBD. Identify a partner before / during the hackathon so the project doesn't die at demo day. Candidates: EA Forum moderators, an EA policy org (e.g. Center for Long-Term Resilience), Apart Research, or a 80,000 Hours team member.

---

## 5. License

[MIT](LICENSE).

---

## 6. Status

🚧 **Pre-build.** Specs locked, ready to start the 60 minutes.
