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

## `transduction_orgs`

For each of the 3 role-exclusive organization types listed below, name 25+ public organizations, and for each organization cover each of the 3 evidence facets with a page-specific source (1+ URL per facet). Organizations should have public source-stated ex-vivo lentiviral, gamma-retroviral, retroviral, or directly related viral-vector cell-engineering capability as of March 19, 2026.

This is a public capability-provenance task, not a procurement, ranking, outreach, contact, clinical, legal, financial, or commercialization-advice task.

Organization types:
- `therapeutic_program_sponsor`: commercial or nonprofit therapy sponsors/developers publicly tied to a named gene-modified cell therapy program, product, or trial. A hospital, institute, or university can be submitted here only when the cited evidence presents it as the sponsor/developer of a named therapeutic program or trial, not merely as a GMP facility, vector-service provider, or research group.
- `cdmo_ctdmo_provider`: CDMO/CTDMO, vector-manufacturing, cell-therapy manufacturing, or platform-service providers offering LVV/RVV, transduction, or gene-modified cell-therapy manufacturing services to other organizations. Sponsors/developers count here only when the source states a separate provider/service role.
- `academic_hospital_gmp_program`: academic, hospital, or nonprofit GMP facilities, translational programs, cell-processing programs, vector cores, or research groups whose cited role is providing GMP, vector, transduction, cell-processing, translational, or research capability. Do not use this bucket for the same entity when the source is only a sponsor/developer program page or only a commercial CDMO service page.

Evidence facets:
- `official_capability`: an organization-controlled capability, service, facility, platform, pipeline, product, or program page that states the in-scope capability in the claimed organization-type role.
- `program_product_trial`: source evidence centered on a named program, product, trial, registry, pipeline entry, publication, abstract, customer collaboration, or manufactured clinical program tying the organization to the relevant cell-engineering work. For CDMO/CTDMO providers, this should identify a named customer/sponsor collaboration, clinical program, manufactured program, case study, registry, or publication that names the provider/service role; a generic official service page alone is not enough.
- `process_facility_corroboration`: a source with concrete facility, GMP suite, vector/transduction process, manufacturing, release-testing, publication, conference, registry, or reputable biotech-article corroboration. This must be a distinct source role from `official_capability` and `program_product_trial`; it cannot be only the same official marketing/platform page recast under another label.

Use pages dated or contextually usable on or before March 19, 2026. Undated stable organization-controlled pages can count when they do not visibly postdate the cutoff. Directories, market reports, generic CDMO listicles, search/result pages, contact pages, and generic CAR-T or cell-therapy pages without explicit vector/transduction/cell-engineering evidence do not count.

Requirements:
- The page must clearly tie the evidence to the claimed organization in the claimed organization-type role.
- The page must explicitly connect the organization to in-scope ex-vivo viral-vector cell engineering: lentiviral, gamma-retroviral, or retroviral transduction of cells; a lentiviral/retroviral gene-modified cell therapy or program; or LVV/RVV production or process capability specifically tied to ex-vivo cell therapies.
- The page must fit the claimed evidence facet's source role.
- For a given organization, use distinct URLs and distinct source roles for the three evidence facets. Do not reuse the same page, a near-duplicate of the same page, or a generic corporate/service page across facets.

Write one JSON object per line to `results_transduction_orgs.jsonl`:
{"item": { "organization_type": "<organization_type>", "organization": "<organization>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
