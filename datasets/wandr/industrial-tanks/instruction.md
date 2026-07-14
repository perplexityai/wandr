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

## `industrial_tanks`

For 30+ manufacturers of industrial or commercial storage tanks serving the U.S. or North American market, name 3+ specific tank products, tank types, branded systems, or product families per manufacturer. For each manufacturer-product pair, supply 2+ different `source_role` groups from the closed set below, and within each source role supply 2+ different `claim_facet` evidence records, each supported by a public URL (1+ per evidence record).

Industrial tank sources often blur manufacturer literature, public project specifications, third-party listings, capability language, and facility context. Keep each record limited to what the cited page supports for the named manufacturer and tank product or family; do not turn the evidence into manufacturer ranking, procurement advice, engineering design, code-compliance verdicts, installation guidance, or compatibility guarantees.

The `source_role` values are:
- `official_product_literature`
- `public_project_or_owner_spec`
- `independent_listing_or_program`

The `claim_facet` values are:
- `capacity_or_dimensions`
- `construction_or_tank_type`
- `application_or_stored_medium`
- `standards_or_certification`
- `project_or_facility_context`

Eligible `official_product_literature` sources are manufacturer-controlled product pages, tank-type pages, catalogs, brochures, product literature PDFs, drawings, data sheets, or manufacturer case studies. Eligible `public_project_or_owner_spec` sources are public owner, public agency, utility, project-manual, bid, procurement, or specification pages that identify the submitted manufacturer-product as a project requirement, approved product, basis of design, installed system, or comparable project-scoped tank choice. Eligible `independent_listing_or_program` sources are non-manufacturer certification, listing, license, approval, testing, or association technology-program pages that identify the submitted manufacturer-product scope.

Non-manufacturer sources count only when the cited source itself ties the claim to a manufacturer, product family, tank type, trade designation, listing ID, license, approval, project/specification, named technology program, facility, or similarly concrete manufacturer-product scope. A manufacturer-controlled source cannot satisfy the public-project or independent-listing roles just because it mentions a project, standard, or certificate.

Top-10 rankings, SEO directories, supplier directories, broad market reports, distributor pages without manufacturer-product identity, generic standards pages, and broad listicles do not count. A generic AWWA, NFPA, API, UL, STI, FM, NSF, or owner-specification explainer is not product evidence unless it identifies the submitted manufacturer-product scope. Manufacturer-wide standards language should not be projected onto every product family unless the cited source itself scopes the language that way.

Requirements:
- The page must clearly tie `manufacturer` to `tank_product_family` as a manufacturer-scoped tank product, tank type, branded tank system, or product/application family.
- The page must match the submitted `source_role` and preserve that source's scope for the submitted manufacturer-product.
- The page must support the submitted `claim_facet`: numerical capacity, size, or dimensional evidence for `capacity_or_dimensions`; tank type, material, containment, or construction method for `construction_or_tank_type`; named application, use case, or stored medium for `application_or_stored_medium`; exact standards, certification, listing, approval, license, QA-program, or similar wording for `standards_or_certification`; or a concrete project, facility, owner, site, installation, or public-specification context for `project_or_facility_context`.

Write one JSON object per line to `results_industrial_tanks.jsonl`:
{"item": { "manufacturer": "<manufacturer>", "tank_product_family": "<tank_product_family>", "source_role": "<source_role>", "claim_facet": "<claim_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
