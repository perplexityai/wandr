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

## `pgh_cle_tech_company_provenance`

For each of the 2 regional scopes below, cover 300+ distinct AI, robotics, autonomy, software, data, cybersecurity, IoT, advanced-manufacturing, healthcare, edtech, or comparable technology product companies per region; for each (`region`, `company`) pair and each of the 3 evidence facets below, supply URL evidence (1+ public URL per facet) on a page about that specific company and facet.

Regional scopes:
- `greater_pittsburgh_swpa`: Greater Pittsburgh and Southwestern Pennsylvania, including source-stated local anchors such as Pittsburgh-area headquarters, offices, labs, facilities, university or accelerator ties, or product/development presence.
- `greater_cleveland_neo`: Greater Cleveland and Northeast Ohio, including source-stated local anchors such as Cleveland-area headquarters, offices, labs, facilities, university, hospital, accelerator, or portfolio ties, or product/development presence.

Evidence facets:
- `regional_presence`: public evidence that the company has a source-stated anchor in the declared region.
- `product_reality`: public evidence that the company has a concrete product, platform, product line, shipped software, or shipped hardware offering.
- `technology_character`: public evidence that a source states the company's technology character or product category, such as AI, robotics, autonomy, software, data/analytics, cybersecurity, IoT, advanced manufacturing technology, healthcare technology, edtech, or a comparable technology-product category.

Companies should be operating companies with a concrete product, platform, product line, shipped software, or shipped hardware identity. The sources should stay descriptive and public-evidence-backed: official company pages, product/about/careers/location pages, press releases, accelerator or portfolio pages, university or hospital commercialization pages, government/economic-development pages, and reputable news or industry pages can all work when they visibly earn the declared facet. Discovery directories can help, but a directory/listing page only counts when it contains company-specific evidence for the chosen facet.

Do not use contacts, people-search pages, email/phone lookups, lead lists, vendor rankings, company scores, outreach angles, sales-prioritization claims, procurement recommendations, investment recommendations, or "best/top vendor" framing as evidence. Do not infer AI or product status from generic "innovation", "technology", or "digital transformation" language.

Requirements:
- The page must clearly identify the named company.
- The page should make its facet-appropriate source role visible. For `regional_presence`, the page should be a company-specific regional, location, portfolio, accelerator, university, hospital, economic-development, careers, official, or reputable-news surface. For `product_reality`, the page should have product-specific framing such as an official product page, product documentation, launch page, product news, customer/product story, regulatory or product announcement, or comparable source. For `technology_character`, the page should source-state the company's technology or product category. Generic rankings, contact/person lookup pages, sponsored lead lists, service-provider directories, and thin logo/member lists do not count when they lack company-specific facet evidence.
- The page should expose a focused, company-specific finding for the declared facet. For `regional_presence`, it should source-state an anchor in the declared region. For `product_reality`, it should show a concrete product, platform, product line, shipped software, or shipped hardware offering. For `technology_character`, it should source-state the company's technology character or product category rather than leaving that classification to inference.

Write one JSON object per line to `results_pgh_cle_tech_company_provenance.jsonl`:
{"item": { "region": "<region>", "company": "<company>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
