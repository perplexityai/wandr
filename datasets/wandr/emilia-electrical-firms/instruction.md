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

## `emilia_electrical_firms`

For 100+ firms with public evidence of industrial electrical engineering, automation, controls, MV/LV, panels, MEP, machine/equipment-electrical, or plant-electrical capability tied to Emilia-Romagna, supply a source for each of the 3 evidence facets below, with at least 1+ URL under each firm/facet.

This is a public provenance task, not a supplier recommendation, ranking, outreach list, contact collection, compliance assessment, or procurement guide. Use only source-stated facts; sector/application labels are useful when the source states them, not when they are inferred from the region or industry cluster.

Evidence facets:
- `official_industrial_capability`: a firm-controlled official page or firm-authored brochure that states the firm's relevant industrial electrical, controls, MV/LV, panel, MEP, machine-electrical, plant-electrical, PLC/HMI/SCADA, or electrical-automation capability. Generic machinery, mechatronics, "automation", or civil-electrical copy is not enough unless the page states the electrical/control/panel/plant-electrical capability.
- `emilia_romagna_identity`: a public source that states the firm has a headquarters, operating site, registered office, plant, or source-described operating presence in Emilia-Romagna.
- `independent_capability_workproof`: a non-firm-controlled public source that names the firm and gives a concrete electrical/automation/control/MEP/MV-LV/panel/plant-electrical capability, project, sector application, tender/award, trade-fair profile, chamber/association profile, reputable engineering article, or comparable independent capability attestation. Official firm pages, official brochures, LinkedIn pages, generic directories, scraped listicles, and contact/RFQ pages do not count for this facet.

Sources should be public, accessible, and source-backed. Thin existence directories, contact-only listings, phone/email pages, job postings by themselves, professional-register entries for individual engineers, residential-only electrician pages, and generic service blurbs without the facet's required signal do not count. Do not reuse one official homepage, about page, brochure, or all-purpose profile as all evidence for a firm; the independent workproof facet must come from a separate non-firm-controlled source.

Requirements:
- The page must clearly identify the named firm.
- The page should make its source role fit the declared `evidence_facet`.
- The page must contribute the declared facet's evidence: official industrial capability, Emilia-Romagna identity, or independent capability workproof.

Write one JSON object per line to `results_emilia_electrical_firms.jsonl`:
{"item": { "firm": "<firm>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
