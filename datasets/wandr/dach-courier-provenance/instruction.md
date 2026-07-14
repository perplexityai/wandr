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

## `dach_courier_provenance`

For each of the 3 countries listed below, supply fragmented public-provenance evidence for 35+ country-scoped courier, express, parcel, same-day, overnight, messenger, postal-parcel, or closely comparable delivery brands/operators; for each brand/operator, cover each of the 4 provenance facets listed below with a source (i.e. 1+ URL) that exposes a focused public-provenance finding for that facet.

The task is neutral public brand/operator provenance. Procurement advice, supplier ranking, marketing strategy, outreach, contact enrichment, lead scoring, investment analysis, legal/compliance adequacy, safety adequacy, ratings-as-quality judgment, and similar evaluative conclusions are outside the task.

Countries:
- **Germany** (also written as: Deutschland, DE, Federal Republic of Germany, Bundesrepublik Deutschland)
- **Austria** (also written as: Austria, Osterreich, Oesterreich, AT, Republic of Austria)
- **Switzerland** (also written as: Schweiz, Suisse, Svizzera, CH, Swiss Confederation)

Provenance facets:
- `operator_structure`: page-visible provenance for how the public brand, regional asset, operator, legal entity, parent, licensee, station, predecessor, successor, or comparable operating identity fits together
- `public_standing_trace`: a non-owned public standing trace that records the brand or operator as a delivery provider, member, participant, listed provider, or comparable public logistics actor
- `counterparty_network_trace`: a relationship-specific trace connecting the brand or operator to a named counterparty, network, partner, locker/platform, customer, cooperation, carrier-integration, or similar delivery ecosystem link
- `independent_profile_trace`: a third-party editorial, trade, company-profile, history, acquisition, market, or comparable public profile trace with entity-specific delivery or operator substance

A `courier_brand` ought to be a real public brand, operator, or regional public asset tied to in-scope delivery service in the submitted country. Regional variants can count separately only when page evidence shows a distinct regional public asset, operator identity, domain, or service geography; the same brand can count separately across countries when the country-scoped presence is supported. Same-acronym or same-string entities outside DACH courier, parcel, express, same-day, overnight, messenger, postal-parcel, or closely comparable delivery scope do not count; generic freight, warehousing, letter-only mail, software/carrier-list, food-delivery-only, passenger-transport, and company-list entries need direct page evidence of the in-scope delivery role rather than only a name, category, or contact listing. Basic official presence and service scope help establish the entity, but they are not by themselves the provenance facets requested below.

Requirements:
- The page must clearly identify the named brand, operator, or regional public asset.
- The page must tie that brand, operator, or public asset to the submitted country, a region within that country, the DACH market, or a country-scoped in-scope delivery service.
- The page must make its facet-appropriate source role visible. For `operator_structure`, it should carry an explicit brand-to-operator, operator-to-public-asset, parent/group, licensee, franchise/station, predecessor/successor, regional-unit, publication-identity, or comparable structure/lineage context; a footer company name or contact address without a relationship anchor is not enough. For `public_standing_trace`, it should be a non-owned public standing context that records the brand/operator as a provider, member, participant, listed operator, or comparable logistics actor; private lead pages and bare contact cards do not carry this role. For `counterparty_network_trace`, it should be a relationship-specific page involving another named organization, network, platform, partner, customer, or cooperation connected to the brand/operator's delivery work. For `independent_profile_trace`, it should be a third-party editorial, trade, profile, history, acquisition, market, or comparable public profile context rather than the brand/operator's own service marketing.
- The page must expose a concrete finding scoped to the selected facet. For `operator_structure`, this is the page-visible operating, legal, parent, licensee, regional, transition, or lineage relationship; for `public_standing_trace`, the provider/member/participant/listed-operator standing and the public body or organization carrying it; for `counterparty_network_trace`, the named counterparty or network relationship and its delivery-relevant role; for `independent_profile_trace`, an entity-specific public profile, history, editorial/trade, acquisition, market, or service-detail finding. Bare contact details, rating scores, rankings, lead prompts, prices, review sentiment, supplier recommendations, credit/finance facts, generic list placement, official homepage copy, or text that only repeats a name and service category do not carry the finding by themselves.

Write one JSON object per line to `results_dach_courier_provenance.jsonl`:
{"item": { "country": "<country>", "brand": "<brand>", "provenance_facet": "<provenance_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
