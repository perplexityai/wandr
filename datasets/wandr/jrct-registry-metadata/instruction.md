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

## `jrct_registry_metadata`

For each of the 5 jRCT recruitment-status buckets, supply official record-detail evidence for 15+ distinct jRCT records with that source-stated status, covering each of the 4 registry facets below and supplying 1 URL per record-facet row. Facets require the specified current official detail surface and row-specific field evidence; do not satisfy multiple facets from generic repeated detail-page snippets.

Recruitment-status buckets:
- `Pending`
- `Recruiting`
- `Suspended`
- `Not Recruiting`
- `Complete`

Registry facets:
- `jp_status_date_update`: Japanese detail-page jRCT number, Japanese recruitment/progress status, initial publication or registration date, final publication or last modified date when shown, and a source-scoped same/different/blank update-date relationship
- `en_design_phase_model`: English detail-page study type, phase/classification when public, and at least two source-stated study-design model fields such as allocation, masking, control, assignment, purpose, observation model, or time perspective
- `jp_condition_intervention`: Japanese detail-page target disease/condition, intervention presence or absence, and intervention/no-intervention description using source labels
- `result_publication_state`: completion date, observation-period end date, result-summary posting date/block, or explicit local blank/dash/no-public-result marker; publication state/date only, not result substance

Sources should be current official jRCT/MHLW record-detail pages on `jrct.mhlw.go.jp`. Use the Japanese `https://jrct.mhlw.go.jp/latest-detail/<jRCT...>` page for `jp_status_date_update` and `jp_condition_intervention`. Use the English `https://jrct.mhlw.go.jp/en-latest-detail/<jRCT...>` page for `en_design_phase_model`. Use either current English or Japanese detail page for `result_publication_state`. Search pages are only useful for discovery. Old `jrct.niph.go.jp` URLs, CSV or download endpoints, bulk exports, scraped mirrors, sponsor or hospital pages, journal articles, press releases, ClinicalTrials.gov, ICTRP trial pages, UMIN, ChiCTR, CRIS, CTRI, aggregators, and trial-matching or recruitment sites do not count as record evidence.

Keep the work to neutral public registry metadata provenance. Public sponsor, institution, investigator, or contact-like fields may appear on jRCT pages, but do not collect contact details, outreach details, rankings, or lead lists. Do not provide participation guidance, recruitment targeting, eligibility screening, treatment recommendations, clinical recommendations, safety or efficacy interpretation, adverse-event interpretation, medical/legal/compliance advice, investment framing, dashboards, alerts, or strategy advice.

Requirements:
- The page must directly show the submitted jRCT number and a source-stated recruitment/progress status matching the submitted recruitment-status bucket.
- The page must directly show the source-stated registry field labels and values for the submitted registry facet.
- For `jp_status_date_update`, the Japanese detail page must show `jRCT番号`, Japanese `進捗状況`, `初回公表日` or `登録日`, and `最終公表日` or a local blank/not-shown update-date cell. Preserve whether the final/update date is the same as, different from, or blank relative to the initial/registration date; do not infer currentness from a title, search result, or URL alone.
- For `en_design_phase_model`, the English detail page must show `Study Type`, phase/classification when public or a local blank/N/A marker when reported, and at least two concrete `Study Design` model fields such as allocation, masking, control, assignment, purpose, observation model, or time perspective.
- For `jp_condition_intervention`, the Japanese detail page must show `対象疾患名`, `介入の有無`, and `介入の内容 / Intervention(s)` or the local no-intervention marker.
- For `result_publication_state`, the page must show completion date, observation-period end date, result-summary posting date/block, or an explicit blank/dash/no-public-result marker. Blank or no-public-result states only work when the page shows a local blank, dash, no-public-result marker, or captured result-publication block where that field is conventionally shown.

Write one JSON object per line to `results_jrct_registry_metadata.jsonl`:
{"item": { "recruitment_status": "<recruitment_status>", "jrct_number": "<jrct_number>", "registry_facet": "<registry_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
