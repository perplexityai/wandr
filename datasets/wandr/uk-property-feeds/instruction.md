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

## `uk_property_feeds`

For 12+ distinct public source products, providers, portal feed surfaces, feed programs, or source domains, supply UK-relevant property listing feed-in documentation and interoperability evidence. Under each source product/provider, cover 2+ property listing destinations it sends or supports listings into, cite 1+ concrete public integration surface for that source-destination pair, and cover 2+ distinct source-stated evidence facets from the list below with 1+ source URL.

The destination set must include these anchor destinations:
- Rightmove
- Zoopla
- OnTheMarket

After those anchors, the destination set is open: source-linked residential, lettings, new-homes, overseas, commercial, regional, or specialist property-listing destinations can count when the cited source ties them to UK-relevant listing syndication. Do not satisfy the source-product/provider floor by splitting one provider into page-title, destination, or minor branding variants; each source-product/provider value should be a distinct source-side product family, provider, portal-owned feed program, or source domain.

The destinations are property portals or listing sites where estate agents, housebuilders, CRMs, websites, plugins, or feed brokers send listings to be displayed. A source product/provider value should name the source-side product, provider, feed program, or domain, not the destination itself. A portal-owned feed surface such as Rightmove ADF can count as a source product/provider when the page itself is the public source for sending listings into that portal.

Valid integration surfaces include portal-owned developer/support/feed pages, vendor or CRM help-center pages, WordPress/plugin documentation, feed-broker pages, housebuilder implementation articles, and similar public sources. A source must state a substantive feed-in fact; a generic logo wall or "integrates with" list is not enough on its own.

The evidence facets, referred to as `evidence_facet`, are:
- `format_transport`: source-stated feed format, transport, protocol, API shape, certificate, endpoint, FTP, polling/sync cadence, or comparable mechanics
- `setup_operations`: source-stated setup, approval, account, branch ID/code, test/live workflow, logging, portal-account, or operating-control evidence
- `listing_content_policy`: optional source-stated listing-field, material-information, status/category, cost, volume-limit, current/legacy, public no-spec, or contact-support posture evidence

`listing_content_policy` is a valid optional facet when the source states such facts, but field lists, material-information details, costs, rate/volume limits, BLM status, currentness, and public-spec/contact-support posture are not required for every destination or integration surface.

Broad multi-destination source hubs count only when the cited page source-locally ties the claimed facet fact to the destination, or to a named destination group that includes it. Source-local means the destination or named group and the facet fact appear in the same sentence, bullet, table row, list entry, heading-scoped section, named package description, or equivalent local unit. A generic provider capability plus a separate logo wall, portal roster, or destination list elsewhere on the page is not enough.

Useful provenance to report when visible: the destination, the source product/provider or portal surface, the source class, the feed direction, the source-stated detail being claimed for the facet, any current/legacy or support posture, and any source date or observed-date cue.

Out of scope: consumer listing-search APIs, scraper/data-extraction APIs, generic real-estate API catalogs, lead-generation APIs, vendor recommendations or rankings, partner-contact discovery, outreach, sales strategy, contact enrichment, and legal-compliance advice. Material-information fields can be recorded only as source-stated feed/listing-field evidence, not as legal advice.

Requirements:
- The page must identify the claimed destination as the property listing recipient or listing destination.
- The page must identify or embody the claimed source product, provider, portal feed surface, or source domain.
- The page must identify or embody the claimed integration surface and tie it to that destination.
- The page must state or clearly imply feed-in direction: listings or property data move from an agent, housebuilder, CRM, website, plugin, feed broker, or provider into the destination.
- The page must state a facet-specific feed documentation or interoperability fact matching `evidence_facet`.
- The facet-specific fact must be source-locally tied to the claimed destination or to a named destination group that includes it.

Write one JSON object per line to `results_uk_property_feeds.jsonl`:
{"item": { "source_product_or_provider": "<source_product_or_provider>", "destination": "<destination>", "integration_surface": "<integration_surface>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
