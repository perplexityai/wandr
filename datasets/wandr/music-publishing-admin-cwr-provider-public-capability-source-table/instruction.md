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

## `music_publishing_admin_cwr_provider_public_capability_source_table`

For 75+ music-publishing administration provider-product entries, name both the provider and product/module/tool/library, and cover 3+ of the capability facets below per provider-product; for each provider-product and facet, supply a public source URL (1+ per facet) whose page source-states that specific capability for the same product.

The purpose is a public capability-provenance table for music publishing administration / CWR-adjacent products as of June 25, 2026, not a vendor ranking, recommendation, partner shortlist, purchase guide, implementation guide, legal/accounting guide, or contact list.

Capability facets:
- `cwr_works_registration`: the product prepares, generates, imports, exports, validates, submits, delivers, accepts, or otherwise works with CWR / Common Works Registration / works-registration data.
- `royalty_accounting`: the product handles music royalty accounting, income ingestion, royalty processing, splits/terms application, payment calculation, or royalty statements.
- `rights_catalog_admin`: the product manages music works, repertoire, catalog metadata, publishing shares, splits, agreements, rights, contract terms, or related catalog-administration data.
- `society_or_endpoint_integration`: the product names specific societies, CMOs, PROs, mechanical-licensing bodies, collection/registration endpoints, DSPs, or similar music-rights destinations/sources as supported integrations, delivery targets, collection sources, or connected endpoints.
- `developer_api_or_library`: the product or tool exposes public API documentation, SDKs, package/repository documentation, developer docs, or library functionality tied to music publishing administration, CWR, royalties, rights, or catalog workflows.

Valid provider-product entries are productized software suites, modules, developer tools, libraries, or public tooling surfaces in music publishing administration, CWR/common-works registration, music royalty accounting, rights/catalog administration, or closely adjacent music-rights workflows. Pure recorded-music distributors, PROs/CMOs acting only as societies, generic CRM/accounting tools, book/media-rights tools without music-publishing relevance, financing/payments-only services, and service-only consultancies without a public software/tool surface are outside the intended provider-product universe.

Sources should be public, accessible, and usable as normal pages. Strong source surfaces include official product pages, feature pages, help-center articles, public docs/API docs, integration pages, public repositories/package pages, standards pages, society/hub pages, and reputable music-industry trade sources when the page role fits the facet. Generic software directories, best-of/listicle pages, AI-answer pages, lead databases, press-wire republications, and scraper profiles do not establish a product capability by themselves.

Requirements:
- The page must clearly identify or bind the named provider-product, module, developer tool, library, or public tooling surface.
- The page should visibly fit the submitted capability facet's source role. For example, product/feature/help/docs pages can fit product-owned capability facets; integration pages can fit endpoint evidence; repository/package/API/developer documentation can fit `developer_api_or_library`; standards or society pages can fit only when they substantively identify the relevant product/tool/channel or the facet-specific context being claimed.
- The page must source-state a concrete, facet-specific capability for the submitted provider-product. Generic "music software", "global rights", "worldwide collection", "works with everyone", or homepage tagline language is not enough unless the page also carries a concrete capability detail for the submitted facet.

Write one JSON object per line to `results_music_publishing_admin_cwr_provider_public_capability_source_table.jsonl`:
{"item": { "provider_name": "<provider_name>", "product_name": "<product_name>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
