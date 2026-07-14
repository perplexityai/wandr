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

## `financial_institution_ai_outcome_evidence`

For 140+ named financial-institution AI, automation, proactive-banking, underwriting, member-retention, embedded-finance, or contact-center initiatives, supply one public source for each of the 2 evidence sides (i.e. 1+ URL per side).

Each `institution_initiative` should identify both the named financial institution and a specific initiative, program, vendor relationship, named capability, or deployed AI / automation product. The initiative should be more specific than a generic AI strategy or technology category.

The evidence sides of interest are:
- `outcome_claim`: a public page naming the financial institution and initiative and stating a concrete source-stated quantitative outcome. Vendor-owned case studies, webinars, customer stories, or vendor-authored announcements can count here when the source ownership is clear.
- `non_vendor_corroboration`: a non-vendor source that acknowledges the same initiative, vendor relationship, or deployed capability in its own voice. It does not need to repeat the same metric digit as the outcome claim.

Quantitative outcomes can include containment, wait-time reduction, calls automated, hours saved, onboarding time, approval or auto-decision rates, approved loan volume, delinquency movement, engagement, balance lift, transaction or deposit volume, proactive insights, CSAT / NPS, abandonment, product adoption, or similar public outcome figures.

Modeled ROI calculators, worksheet templates, payback models, aggregate consultant ranges, anonymous cases, unsourced listicles, PR-copy syndication, vendor libraries mislabeled as independent, generic AI strategy pages, planned pilots without deployment evidence, implementation advice, targeting, outreach, lead scoring, contact enrichment, and vendor recommendations do not satisfy the task.

Requirements:
- The page must identify the named financial institution and the same specific initiative, relationship, deployed capability, or product named by `institution_initiative`.
- The page must have the source role required by `evidence_side`: a source-owned public outcome claim for `outcome_claim`, or non-vendor own-voice corroboration for `non_vendor_corroboration`.
- The page must contribute the evidence required by `evidence_side`: a concrete source-stated quantitative outcome for `outcome_claim`, or acknowledgment of the same initiative, relationship, or deployed capability for `non_vendor_corroboration`.

Write one JSON object per line to `results_financial_institution_ai_outcome_evidence.jsonl`:
{"item": { "institution": "<institution>", "initiative": "<initiative>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
