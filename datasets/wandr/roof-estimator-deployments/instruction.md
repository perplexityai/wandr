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

## `roof_estimator_deployments`

For 4+ provider families, cover public contractor-branded deployments of instant roof estimate / instant roof quote flows: for each provider family, name 30+ distinct contractor deployments, with 1+ public URL for each deployment.

The useful evidence is downstream deployment evidence, not vendor marketing. Provider families are open-set named platforms or provider-branded flows; Roofr, RoofQuote PRO / Roofle, Instant Roofer, and SkyQuote are examples, not a fixed menu. Contractor deployments should be real roofing or home-exterior contractor contexts, including provider-hosted app pages when the public page names the contractor and flow.

Public source text used for the row should be visible before any login, private address submission, contact-form submission, or lead-capture step. Vendor demos, official provider product pages, software directories, review pages, listicles, generic search/listing pages, and ordinary contact forms do not count as deployment evidence.

Requirements:
- The page must identify the contractor or contractor-branded deployment context and enough market / location context to distinguish the deployment.
- The page must visibly offer a homeowner-facing instant roof estimate, instant roof quote, roof estimator, or comparable fast roof-pricing flow.
- The page must publicly attribute the flow to the submitted provider family, or expose a provider-hosted app / provider-branded URL that names the contractor and flow.
- The page must expose at least one concrete homeowner-flow claim or caveat, such as satellite / AI measurement, address-first flow, quote timing in seconds or minutes, no call / no appointment / no waiting before seeing a range, preliminary estimate status, inspection confirmation, material / package / financing options, follow-up workflow, or similar source-supported flow substance.

Keep the output to public deployment provenance. Do not submit product recommendations, vendor rankings, review sentiment, pricing advice, estimate-accuracy verdicts, implementation advice, contractor outreach, lead scoring, contact enrichment, or source material obtained by entering a private address or personal contact information.

Write one JSON object per line to `results_roof_estimator_deployments.jsonl`:
{"item": { "provider_family": "<provider_family>", "contractor_name": "<contractor_name>", "market_or_location": "<market_or_location>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
