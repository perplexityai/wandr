You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `european_private_software_scale_metrics`
  - `european_private_software_scale_metrics.public_scale_metrics`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `european_private_software_scale_metrics`

For 120+ European private software or fintech companies, name each company with its `country_or_hq` label and supply an authoritative public identity source (i.e. 1+ URL per company). Use 2026-04-28 as the target as-of anchor for the company universe; rely on each source's own stated date, filing period, or publication frame rather than relative "latest" wording.

Companies in scope are privately held operating companies or groups headquartered, incorporated, regulated, or substantively operating in Europe or the UK, whose business is software, SaaS, cloud, enterprise / application software, developer / data software, payments, banking, fintech infrastructure, or comparable software-enabled financial technology.

Eligible identity sources include company-controlled pages and filings, statutory registries, regulator records, annual reports, official investor / owner pages or announcements, and similarly authoritative public pages. Do not prove private status from silence or lack of exchange-listing evidence.

Requirements:
- The page must clearly identify the named company or group and tie it to the submitted `country_or_hq` through headquarters, registered office, incorporation, regulator country, or comparable operating-country evidence.
- The page must support the company's software or fintech category.
- The page must source-state private-company status through privately held wording, private limited / non-public legal form, registry status, investor-backed or private-ownership framing, or equivalent evidence.

Write one JSON object per line to `results_european_private_software_scale_metrics.jsonl`:
{"item": { "company": "<company>", "country_or_hq": "<country_or_hq>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `european_private_software_scale_metrics.public_scale_metrics`

Cross-tasknode identifier discipline: this task is for the same {= company =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= company =}+ companies, supply public scale-metric evidence for at least 1 of the metric kinds below per company, with 1+ URL for each company-metric kind. Revenue / ARR evidence is the strongest family, but it is not required for every company when another source-stated operating scale metric is available.

Metric kinds:
- `revenue_or_arr`: turnover, revenue, ARR, recurring revenue, cloud ARR, or similar source-stated financial operating scale.
- `workforce_or_customer_scale`: employees / FTEs, customers, users, clients, seats, or comparable company-wide scale facts.
- `transaction_or_usage_scale`: payment volume, transaction count, GMV-like operating volume, product usage volume, product activity volume, or comparable operating throughput.

The page should state a concrete numeric metric for the named company or group and, where meaningful, the metric's period or as-of frame. Strong sources include official financial pages, annual reports, statutory filings / accounts, official company or investor announcements, regulator materials, and reputable attributed press.

Do not use modeled profile-database estimates, paywalled or unsupported range tiles, valuation-to-revenue inference, ARR / MRR modeling, funding amounts, valuations, rankings, investment advice, lead scoring, contact lookup, outreach, or enrichment as operating scale metrics.

Requirements:
- The page must tie the metric statement to the named company or recognizable parent / trading group.
- The page must state a concrete numeric operating scale metric matching `scale_metric_kind`, with the source's period or as-of frame where that context is meaningful.

Write one JSON object per line to `results_european_private_software_scale_metrics.public_scale_metrics.jsonl`:
{"item": { "company": "<company>", "country_or_hq": "<country_or_hq>", "scale_metric_kind": "<scale_metric_kind>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
