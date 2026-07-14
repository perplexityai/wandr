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

## `us_robotics_ai_seed_funding`

For 160+ US-based startups in robotics, autonomy, drones, industrial automation, embodied/physical AI, or applied AI/ML tied to physical-world systems, identify the specific seed or pre-seed funding event (`funding_event`) for each company and supply one source for each of the 2 public evidence roles, with each source documenting that same event (i.e. 1+ URL per role).

This is a funding-provenance task, not a startup ranking, investor-screening table, contact list, founder-profile table, sales/outreach target list, or recommendation surface. Do not include founder contacts, emails, LinkedIn harvesting, lead scores, procurement advice, investor attractiveness claims, or outreach guidance.

The evidence roles, referred to as `evidence_role`, are:
- `official_disclosure`: an issuer-controlled, funding-participant-controlled, accelerator-controlled, SEC/EDGAR, or issuer-attributed newswire/legal disclosure surface.
- `independent_or_ecosystem_report`: a third-party funding-news, vertical/regional press, credible tracker/database, or ecosystem page that independently reports the event rather than merely copying or syndicating the same issuer press release.

Round amounts, investors, source dates, geography, and category labels should be source-stated when reported. If a public source omits amount or investor details, leave those facts unclaimed or mark them as not public on that page instead of inferring them.

Requirements:
- The page should fit the claimed `evidence_role`: issuer-attributable for `official_disclosure`, and genuinely third-party or independently curated for `independent_or_ecosystem_report`.
- The page must state that the claimed company raised, closed, secured, announced, or otherwise publicly disclosed a seed or pre-seed funding event. Later rounds alone do not count, and bundled raises count only when the seed/pre-seed component is clear.
- The page must source-state US presence for the company, such as headquarters, incorporation, office, operating base, or comparable US operations.
- The page must source-state an in-scope robotics, autonomy, drone, industrial automation, embodied/physical AI, or applied AI/ML category tied to physical-world systems. Generic software AI or AI-infrastructure language is insufficient unless the page ties it to physical-world sensing, action, automation, robotics, autonomy, drones, or comparable embodied systems.
- Any reported round details, such as stage, date, amount, investors, source date, geography, category, or missing/conflict notes, should be stated by the page or explicitly left unclaimed/not-public for that page.

Write one JSON object per line to `results_us_robotics_ai_seed_funding.jsonl`:
{"item": { "company": "<company>", "funding_event": "<funding_event>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
