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

## `azerbaijan_transport_climate`

Build an Azerbaijan climate-relevant transport source-provenance atlas. Cover 8+ source families; for each source family, document 48+ distinct source records, each with 1+ cited source URL.

A `source_record` is a distinct Azerbaijan-specific instrument, official claim, measure, implementation record, standard or fiscal item, market or registry interface, voluntary declaration, conflict lead, or no-evidence finding tied to climate-relevant transport. The record must be visibly anchored on the cited page by a record-specific title, section, table, project, declaration, registry/listing entry, search surface, status line, or checked conflict/absence target. The record should preserve the source's own wording for status, date, conditionality, version, adoption, effectiveness, implementation state, registry state, or absence/conflict state. Do not decide whether something is legally binding, enforceable, credit-eligible, investable, or strategically advisable.

Source families:
- `unfccc_reporting`: NDC versions, national communications, BUR/BTR/transparency reports, UNFCCC party submission pages, or comparable climate reporting/transparency records.
- `national_policy`: Azerbaijan national strategy, presidential, cabinet, ministry, or agency policy pages and plans.
- `legal_decree`: Azerbaijan legal texts, decrees, orders, codes, regulations, or official legal databases.
- `standards_fiscal`: Official standards, taxonomy, tax, customs, finance, vehicle, fuel, or fiscal-incentive records.
- `implementation_agency`: Ministry, agency, operator, or public-entity implementation records for transport measures or infrastructure.
- `market_registry`: Article 6, PACM/CDM, host-party forms, registry, market-mechanism, I-REC/E, or national authority market-interface records.
- `voluntary_declaration`: Official COP, presidency, ministry, or authority pages for declarations, initiatives, pledges, or signatory/status records.
- `secondary_conflict_lead`: Secondary discovery or conflict records used only when framed as secondary and official evidence is unavailable, absent, or contradicted.

All listed source families are mandatory. Do not substitute an easier family for `market_registry`, `voluntary_declaration`, or `secondary_conflict_lead`; those harder surfaces must be documented in their own families.

Article 6, PACM/CDM, host-party, registry, market-mechanism, and national authority market-interface records belong under `market_registry` even when the cited page is UNFCCC-controlled. Use `unfccc_reporting` for NDCs, national communications, BUR/BTR/transparency reports, UNFCCC party submission pages, and comparable climate reporting/transparency records.

Official primary sources include authority-controlled UNFCCC pages/PDFs, Azerbaijan government/ministry/agency pages, president.az, e-qanun.az, CBAR, I-TRACK/Evident/I-REC, UNFCCC Article 6/PACM/CDM pages, COP29 official pages, and comparable authority records. Secondary sources are discovery, context, or conflict leads unless the row is in `secondary_conflict_lead` and is explicitly framed as secondary-only because official evidence is unavailable, absent, or contradicted. Azerbaijani originals and source-language excerpts count; English summaries do not replace an available official original.

Requirements:
- The page must communicate its source family and issuer/source authority: official primary-source character for all families except `secondary_conflict_lead`, and secondary-source character when that family is used.
- The page must make the submitted `source_record` record-specific rather than a broad source-family bucket, generic sector topic, or repeated slice of the same hub page. A broad PDF, registry, declaration bundle, or authority website may support multiple records only when each row cites a visibly different instrument, section, measure, declaration, registry/status check, or checked absence/conflict target from that source.
- The page must substantively connect the record to Azerbaijan and climate-relevant transport: road vehicles, public transport, rail/metro, aviation or maritime boundaries, fuel or vehicle standards, fiscal incentives, charging, electrification, transport emissions, implementation actions, reporting targets, market mechanisms, voluntary declarations, or an explicit checked absence/conflict around those topics.
- The page must provide the source's own status/date/conditionality language where such language exists, such as document type, source language, adoption/effective/status date, target year/version, implementation timing, registry approval status, or comparable provenance wording.
- The record's evidence state must match the cited page without advisory overclaiming: affirmative records state what the source says; conflict records identify the conflicting claim or source-language tension; no-evidence records cite the checked official surface or authority result and frame the result as absence of cited official evidence rather than a legal conclusion.

Write one JSON object per line to `results_azerbaijan_transport_climate.jsonl`:
{"item": { "source_family": "<source_family>", "source_record": "<source_record>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
