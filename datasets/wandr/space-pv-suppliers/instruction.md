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

## `space_pv_suppliers`

Build an as-of 2026-06-29 public provenance set for 75+ supplier-role entries in the spacecraft photovoltaic supply chain. A supplier-role is an organization plus a concise role it publicly performs, such as making space solar cells, supplying CIC/SCA assemblies, integrating solar panels or arrays, providing space-PV materials/components, or testing/qualifying space-PV hardware. For each supplier-role, cover each of the 3 evidence facets below with a source (i.e. 1+ URL per facet).

The task is about public evidence, not vendor selection. Do not rank suppliers, recommend purchases, collect contacts, estimate prices or lead times, advise on export controls, or assert compliance/security adequacy beyond what the public source states.

Evidence facets:
- `official_capability`: a first-party or parent-controlled product, capability, datasheet, brochure, or equivalent page showing the supplier's space-PV role.
- `space_grade_or_qualification`: technical, datasheet, standard, qualification, test, or environment evidence showing space-grade, orbit, AM0, radiation, thermal-vacuum, ECSS/ESCC/AIAA-style, QPL-style, or comparable space-qualification substance.
- `independent_standing`: non-first-party evidence such as a space-agency, mission/customer/program, reputable industry article, technical paper, labeled public directory, or similar independent source that identifies the supplier's role.

Eligible supplier roles should be directly tied to spacecraft, satellites, orbital or deep-space missions, AM0/orbit/radiation space environments, space-qualified PV, space solar cells, CICs/SCAs, spacecraft solar panels/arrays, or directly enabling space-PV materials/components. Generic terrestrial PV manufacturers, ordinary solar installers, spacecraft operators that only buy solar hardware, marketplaces, and unsupported "space-ready" marketing are out of scope.

When source dates, page/source class, confidence qualifiers, missing states, or conflicts are visible, preserve that context in the record. Missing date information is a deficit to note, not automatic disqualification.

Requirements:
- The page must clearly identify the submitted supplier organization.
- The page must show that the organization performs the submitted role in the spacecraft PV supply chain, with an explicit space, spacecraft, satellite, orbit, AM0, radiation, qualification, mission, or comparable space-PV tie.
- The page should visibly fit the submitted evidence facet's source role.
- The page should provide facet-specific evidence for the submitted supplier-role.

Write one JSON object per line to `results_space_pv_suppliers.jsonl`:
{"item": { "supplier": "<supplier>", "role": "<role>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
