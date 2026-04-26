# EA Consultation Tracker

> Working title — discoverable, EA-aware tracking of EU and national public consultations, with cause-area filtering and impact scoring so individuals and experts can act where it counts most.

Built for the **EAGx Stockholm 2026 mini hackathon**.

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
| **EA Consultation Tracker (this project)** | ✅ EU + UK at MVP | ✅ (extensible) | ✅ | ✅ | ✅ | ✅ |

The wedge: **discovery + EA cause classification + opportunity score + opt-in alerts**, citizen-and-expert-facing, open source.

---

## 3. Our Idea

Build a tool that:

1. **Crawls** the websites and feeds of the EU Commission ("Have Your Say") and UK government (gov.uk consultations) for active consultations.
2. **Aggregates** the results into a structured database.
3. **Classifies** each consultation against a borrowed [80,000 Hours / EA Forum](https://forum.effectivealtruism.org/topics/policy) cause-area taxonomy (multi-label).
4. **Scores** "opportunity for impact" using an LLM judgment against an explicit rubric — and **shows the reasoning** so users can override it.
5. **Publishes** through a clean website + opt-in email digests, with subscribers selecting cause areas and minimum impact thresholds.

Long-term (explicitly **out of MVP**): an opt-in expert directory that surfaces relevant consultations to subscribed experts. **No** automated cold outreach — that path is borderline spam, hurts trust, and runs into [EU AI Act](https://artificialintelligenceact.eu/) transparency obligations.

---

## 4. MVP Specification

### 4.1 Audience

EA-aligned individuals and individual experts (e.g. a biosecurity researcher who would respond to a relevant consultation if prompted). **Not** EA orgs with their own policy teams (they're a v2 audience), and **not** general public.

### 4.2 Data sources (v1)

- **EU "Have Your Say"** — all open consultations and "calls for evidence"
- **UK gov.uk consultations** — all open consultations

Both are scraped (no documented public API for Have Your Say). Update cadence: **TBD — see Open Questions**.

### 4.3 Cause-area taxonomy (v1, narrow)

Borrowed and trimmed from 80,000 Hours / EA Forum. Multi-label.

Initial scope (deliberately narrow per project decision): **TBD — see Open Questions**, picked from:
- AI governance & safety
- Biosecurity & pandemic preparedness
- Animal welfare / factory farming
- Global health & development
- Existential risk governance (broader)
- EA-meta / institutional decision-making

Anything not matching any tag → bucketed as **Other** and not surfaced in alerts.

### 4.4 Impact scoring

LLM-judged (Claude), 1–5, with a written rationale visible to the user. Score is a *single number* but the rubric is explicit and multidimensional:

| Dimension | What it captures |
|---|---|
| **Scope** | How many people / animals / future generations are affected? |
| **Reversibility** | Is this a one-shot decision or revisable later? |
| **Tractability** | Is the consultation genuinely open to influence, or rubber-stamping? |
| **Urgency** | Deadline proximity — and is there time for a quality response? |
| **Counterfactual** | Will EA-aligned voices likely otherwise be heard? (low → higher score) |

Implementation: a single Claude call per consultation with the consultation text + rubric + cause tags, returning `{score: 1-5, rationale: string, dimension_notes: {...}}`. Scores are **not authoritative** — they are visible-reasoning suggestions users can disagree with.

### 4.5 Surfaces

- **Web** — list view, filterable by cause area + min score + deadline; detail page per consultation showing original link, summary, score, rationale, deadline.
- **Email digest** — opt-in. Users select cause areas and minimum score. Cadence: **TBD — see Open Questions**.
- **RSS** — one feed per cause area as a low-effort secondary surface.

### 4.6 Out of scope for v1 (deferred deliberately)

- Expert outreach bot (and any automated cold contact)
- National sources beyond EU + UK (Germany, France, etc. → v2)
- Multilingual (EU consultations are normally available in English at the Commission level)
- Tracking whether a consultation actually influenced final law (great v3 idea: scrape final adopted text, LLM-map which submitted themes survived)
- AI-generated comment / astroturf detection on the response side
- User accounts (MVP uses stateless email signup; preferences encoded in the signup form)

### 4.7 License

**MIT** (matches existing repo `LICENSE`). Open source — easier for EA Forum / 80k Hours to adopt or fork.

### 4.8 Sustainability / handoff

Identify a partner before the hackathon ends so the project doesn't die at demo day. Candidates: EA Forum moderators, an EA policy org (e.g. Center for Long-Term Resilience), Apart Research, or a 80,000 Hours team member. **TBD — see Open Questions**.

---

## 5. Open Questions

These need your input before we lock the spec:

1. **Project name** — `EA Consultation Tracker` is a working title. Better suggestions?
2. **Initial cause areas (2–3)** — narrow scope was chosen. Which two or three? Recommendation: AI governance + biosecurity, since both have active EU regulatory pipelines (AI Act follow-ons, EU biosecurity strategy).
3. **Tech stack** — recommend: Python (scraping + LLM calls) + SQLite/Postgres + Astro or Next.js for the static-ish site + Buttondown or Resend for email. Acceptable, or different preference?
4. **Hosting** — Vercel / Netlify / Fly / a VPS?
5. **Update cadence for the scraper** — daily? twice-daily? more?
6. **Email digest cadence** — weekly Monday? Or instant per-consultation alert above a score threshold?
7. **Hackathon timing & team** — when is EAGx Stockholm 2026, how many days, solo or with a team?
8. **Domain name** — do you want one registered, or `.github.io` / Vercel preview for the demo?
9. **Sustainability partner** — anyone in mind to hand this off to post-hackathon?

---

## 6. Status

🚧 **Pre-build.** Specs in flight. See *Open Questions* above.
