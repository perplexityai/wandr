Solve the following task and write the results to the specified JSONL file.

## Universal rules

The following rules apply to every task below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets.

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `pediatric_daf_grant_foundations`

For 30+ orgs as pediatric hospital foundations, children's-health research centers, or children's-health nonprofits that solicit outside philanthropic funding, cover the 3 evidence facets listed below for each org by supplying a source (i.e. 1+ URL under each facet) which exposes a focused, substantive, tangible finding clearly scoped to the facet in question.

The aim is to assemble a grant-prospecting picture of who funds children's health and how an early-stage health project would approach each one.

Evidence facets:
- `giving_engagement`: the org's own published route for an outside funder, partner, or project to give to or formally engage with the org — a "ways to give", "institutional partnerships", "corporate / foundation giving", or development-contact surface, including the named team, channel, or address through which engagement is initiated.
- `funding_priorities`: the org's own statement of what its current philanthropic dollars are directed toward — the strategic focus areas, named programs, research themes, or populations its grantmaking or fundraising prioritizes right now.
- `fiscal_sponsorship`: the org's own statement of whether it offers fiscal sponsorship — operating an outside early-stage or pre-501(c)(3) project under its charitable umbrella — including the eligibility terms or intake route, or an explicit statement that it does not provide it.

The sources should be fully public, accessible, and usable (e.g. not paywall-guarded, donor-portal logins, or member-only screens).

Requirements:
- The page must clearly identify the named org as a children's-health-directed foundation, research center, or nonprofit. These are separately-denoted orgs: distinct foundations under one hospital network, and a research center versus a separately-incorporated nonprofit, count as different orgs even when they collaborate, so a finding on one does not carry over to another (a hospital and its own dedicated foundation or giving arm are the one same org).
- The page should make its facet-appropriate source role visible. For `giving_engagement`, this comes from page-role cues marking it as the org's own giving or partnership surface, such as "Ways to Give", "Institutional Partnerships", "Corporate / Foundation Giving", "Partner with us", or "Contact Development" headings, a development or philanthropy team title, or a giving-inquiry contact block. For `funding_priorities`, it should read as the org's own priorities, strategic-plan, grantmaking-focus, or research-themes surface, e.g. through "Our Priorities", "Strategic Plan", "What We Fund", "Areas of Focus", or named-program / impact-area framing on the org's own pages. For `fiscal_sponsorship`, it should read as a fiscal-sponsorship, sponsored-projects, incubation, or project-eligibility surface, e.g. through "Fiscal Sponsorship", "Sponsored Projects", "Become a Project", FAQ or eligibility headings, or a clear statement on the org's own pages of whether sponsored projects are hosted.
- The page should expose a focused finding clearly scoped to the named org and evidence facet. For `giving_engagement`, this means a concrete engagement route — a named development or partnerships contact, an institutional-giving channel, a partnership tier or program, or a specific way-to-give an outside funder can act on. For `funding_priorities`, it means a specific current funding direction — a named focus area, strategic priority, funded program, research theme, or target population the org's philanthropy is directed at. For `fiscal_sponsorship`, it means a definite answer with substance — the eligibility terms, project criteria, fees, or intake route for becoming a sponsored project, or an explicit on-page statement that the org does not offer fiscal sponsorship.

Write one JSON object per line to `results_pediatric_daf_grant_foundations.jsonl`:
{"item": { "org": "<org>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
