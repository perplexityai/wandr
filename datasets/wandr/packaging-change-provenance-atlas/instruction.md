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

## `packaging_change_provenance_atlas`

For 110+ named OTC and adjacent consumer-health product packaging format transitions within January 1, 2020 through April 3, 2026, cover each of the 3 evidence facets listed below by supplying a public page (i.e. 1+ URL under each facet) that substantiates the same named physical packaging change. Each packaging change is identified by company or brand, product, product line, or tightly scoped product category, and the physical packaging format transition; the same case reported under company or brand aliases counts as the same change.

The useful public record here is packaging provenance, not packaging advice: source-stated dates, metrics, drivers, barriers, consumer-research details, or rollout details can appear as finding context, while inferred consumer adoption, health or regulatory advice, safety or suitability conclusions, supplier recommendations, market strategy, and broad commentary that does not substantiate a named packaging change are outside the task.

Evidence facets:
- `company_disclosure`: a company-controlled, brand-controlled, or official-source-owned disclosure of the named packaging change.
- `format_substantiation`: a packaging partner or supplier case study, pact/certifier/standards-source case page, or technical case source that substantiates the named case's material or format construction.
- `independent_coverage`: independent trade or packaging press, a public consumer-research case study, a public recall/regulatory notice, or other non-brand coverage independently documenting the named transition as packaging-fact evidence.

Packaging changes ought to be real physical packaging format or material transitions for OTC, consumer-health, VMS/supplement, oral-care, dermocosmetic, lip/first-aid, or adjacent consumer-health products or product lines. Generic corporate sustainability goals, recycling campaigns, supplier capabilities, material platforms, market trends, product catalog entries, and broad packaging-policy statements are not packaging changes by themselves. Sources must be public, accessible, and page-evaluable, with the cited page visibly carrying enough content to evaluate the claimed company, product scope, format transition, date, and facet role. The page-stated publication date, launch/change date, or rollout date must fall within January 1, 2020 through April 3, 2026. Press-wire echoes or one article reused across facets work only when the page role and packaging finding genuinely match the claimed facet.

Requirements:
- The page must identify the named company or brand and product, product line, or tightly scoped product category.
- The page must identify a concrete physical packaging format transition, such as a material or structure change, refill/reuse primary system, recyclable tube, canister, blister, pouch, sachet, PCR, fiber, paper, aluminum, or comparable packaging format change.
- The page should make its facet-appropriate source role visible. For `company_disclosure`, the page should communicate company, brand, or official-source control. For `format_substantiation`, it should read as partner, supplier, pact/certifier/standards, or technical case evidence tied to the named case rather than only a generic material capability. For `independent_coverage`, it should read as non-brand packaging-fact coverage rather than brand-controlled disclosure or press-wire republication.
- The page should expose a facet-specific packaging finding about the named transition. For `company_disclosure`, this means source-stated disclosure such as launch, rollout, target conversion, scale, or stated reason for the named case. For `format_substantiation`, it means construction, material, recyclability, certification, partner, or performance detail tied to the named case. For `independent_coverage`, it means an independently reported packaging fact, date, rollout, consumer-research, notice, or coverage detail tied to the named transition.

Write one JSON object per line to `results_packaging_change_provenance_atlas.jsonl`:
{"item": { "company": "<company>", "product": "<product>", "format_change": "<format_change>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
