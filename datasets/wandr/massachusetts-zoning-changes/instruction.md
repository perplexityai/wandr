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

## `massachusetts_zoning_changes`

For 60+ Massachusetts municipalities, supply source-backed evidence for 2+ adopted zoning-change actions per municipality and each of the 3 evidence sides listed below (1+ URL per zoning change and evidence side). In-scope actions were adopted, approved, or made effective within January 1, 2020 through June 15, 2026 and created, removed, renamed, expanded, contracted, or materially changed a zoning district, overlay district, or zoning-map boundary.

The useful unit is one municipal action with a traceable public paper trail: an article, ordinance or bylaw amendment, zoning-map amendment, section addition, or section change. Treat later amendments, map updates, repeals or reenactments, and separate articles as separate zoning changes when public records separate them, even if they implement the same policy or district program.

Evidence sides:
- `adoption_record`: official town/city meeting or council action, adopted ordinance or bylaw, warrant/report with final action, attorney-general approval, municipal clerk record, official municipal adoption summary, or comparable adoption/approval/effective-action surface showing the change was adopted, approved, or made effective during January 1, 2020 through June 15, 2026
- `codified_text`: current or historical bylaw/ordinance text, adopted article text, or legal-code page showing the operative zoning language created or changed by that action
- `geographic_impact`: zoning map, GIS layer, map exhibit, parcel or street list, textual boundary description, named corridor or station area, subdistrict list, acreage plus mapped boundary, or planning-board exhibit concretely locating the affected area for that action

Sources should be public municipal, state, legal-code, GIS, meeting-record, or officially hosted planning surfaces. Legal-code history notes can help bind a changed section to an action, but they do not by themselves satisfy `adoption_record`. Third-party news coverage, campaign pages, generic planning landing pages, broad state compliance summaries, and bare pointers to another map do not count by themselves.

Requirements:
- The page must clearly tie the evidence to the named municipality.
- The page must identify the specific zoning change as the same adopted action, district, overlay, article, ordinance amendment, bylaw amendment, section addition or amendment, or zoning-map amendment rather than only discussing zoning policy in general.
- The page must carry the evidence required for `evidence_side`: for `adoption_record`, a final adopted/approved/effective action with a date within January 1, 2020 through June 15, 2026; for `codified_text`, operative district, overlay, or map-amendment language; for `geographic_impact`, concrete affected-area geography such as a map/GIS view, parcels, streets, corridor, station area, subdistricts, acreage plus mapped boundary, or textual boundary. Codified-text and geographic-impact pages need not restate the adoption date unless they affirmatively contradict the claimed target-period action.

Write one JSON object per line to `results_massachusetts_zoning_changes.jsonl`:
{"item": { "municipality": "<municipality>", "zoning_change": "<zoning_change>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
