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

## `transparent_led_products`

For 35+ providers that publicly present transparent LED display products, name 1+ transparent LED product or series per provider, and supply 1+ public URL for each of the 3 evidence roles listed below.

The task is a public provenance dossier: it is about tying source-stated technical and public-use claims to named transparent LED products, not deciding which provider is best or which setup someone should buy. Product series are fine when the cited sources structure specs by series, variant, module, cabinet, or panel family. The provider should be the manufacturer, brand owner, or product provider responsible for the submitted product; rental houses, distributors, marketplaces, and media outlets do not become the provider just by listing someone else's product. Transparent OLED, transparent LCD, transparent TVs, generic LED walls with no transparency claim, supplier-ranking entries, buying guides, contact pages, and private quote pages do not count as transparent LED display products for this task.

Evidence roles:
- `official_spec`: provider-controlled product page, datasheet, or brochure with transparent LED identity and source-stated technical specs
- `application_trace`: product-specific trace of a named installation, event, customer, venue, production, public project, or rental-fleet acquisition/holding
- `editorial_notice`: non-provider-controlled editorial, trade, news, award, or exhibition coverage with product-specific context, not a seller or catalog listing

Public prices, source dates, and 3D / immersive capability count only when the cited source itself states them; their absence does not invalidate an otherwise eligible record.

Requirements:
- The page must clearly identify the submitted provider and product or series.
- The page must support that the submitted product or series is a transparent LED display, screen, panel, mesh, film, or comparable LED-based transparent display technology.
- The page must make its evidence-role fit visible. For `official_spec`, it must be provider-controlled and specification-bearing. For `application_trace`, it must tie the product or series to a named customer, venue, event, installation, production, public project, or rental-fleet acquisition/holding. For `editorial_notice`, it must be outside the provider's control and have editorial, trade, news, award, or exhibition context, not a seller, rental, distributor, marketplace, catalog, directory, ranking, listicle, buying guide, or provider press-release page.
- The page must contribute the evidence detail expected for its role. For `official_spec`, it must state at least one optical or pixel datum and at least one physical or configuration datum. For `application_trace`, it must describe the named use context and the product's role in it. For `editorial_notice`, it must carry a concrete product fact, launch fact, award/showing fact, or application fact about the product or series.

Write one JSON object per line to `results_transparent_led_products.jsonl`:
{"item": { "provider": "<provider>", "product": "<product>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
