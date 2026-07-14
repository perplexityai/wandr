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

## `us_cardiac_surgery_signals`

For 12+ US cardiac-surgery procedure segments, supply dated public evidence signals. Procedure segments must be procedure families, procedure approaches, combined-operation categories, or source-scoped broad adult-cardiac-surgery totals. For each segment, cover 4+ evidence-signal labels and provide 1+ source URL for each row.

These rows are factual evidence inputs for understanding public market signals, not a market-size model, clinical recommendation, provider recommendation, investment thesis, or product strategy memo.

Evidence-signal labels:
- `procedure_volume`
- `disease_or_patient_pool`
- `economic_or_payment`
- `device_or_installed_base`
- `robotic_specific_or_limit`
- `methodology_scope_or_conflict`

For each row, report the source type, publication date or data year, metric or claim name, metric value/range when present, geography, procedure or patient population, denominator/scope, methodology note, and any caveat needed to keep the source from being overread. Robotic-specific evidence is valuable when directly supported, but a procedure segment does not need a robotic-specific source to count.

Sources should be public and source-role appropriate: registry/statistical sources, CMS/AHRQ or other public utilization/payment data, peer-reviewed epidemiology/utilization/economics literature, FDA or official device documentation, public company filings or official product claims when labeled as company-authored, and hospital/health-system pages only for local program, local procedure, local volume/experience, or local robotic-availability claims. Proprietary market reports, analyst databases, forecast/TAM pages, investment or valuation commentary, medical advice, provider recommendations, generic robotic pages without cardiac procedure context, and broad cardiovascular product pages without a surgery/procedure link do not count.

Requirements:
- The page must connect the cited fact, metric, or caveat to the claimed cardiac-surgery procedure segment or to the directly treated disease/patient pool for that segment.
- The page must support the claimed `evidence_signal` label at the row's scope.
- The row must preserve the page's source role, date or data period, geography, population/procedure scope, denominator or methodology, metric value when present, and caveat without expanding what the source can support.

Write one JSON object per line to `results_us_cardiac_surgery_signals.jsonl`:
{"item": { "procedure_segment": "<procedure_segment>", "evidence_signal": "<evidence_signal>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
