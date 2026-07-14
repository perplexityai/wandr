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

## `restaurant_uniforms`

For 280+ multi-unit restaurant chains, restaurant-chain parents, franchise co-ops, or restaurant operators, name 1+ outside uniform/workwear supplier or program partner for each and supply 1+ URL for each chain/partner pair. Each cited source should connect the named restaurant entity and named partner in a chain-specific uniform, workwear, apparel, footwear, rental/laundry, online ordering, material-technology, or design-program context.

The table is about public evidence of restaurant uniform programs and supplier relationships, not procurement advice. Date the relationship when the source permits it. Useful partner roles include:
- uniform rental or managed laundry
- direct apparel or crew-uniform supplier
- chefwear, apron, kitchen, or back-of-house workwear supplier
- footwear or slip-resistant shoe program partner
- uniform designer, agency, manufacturer, distributor, or franchise ordering portal
- material-technology or sustainability-program partner

Source variety matters because the best evidence is scattered. Useful public source families include:
- official restaurant-chain newsroom, sustainability, franchise, supplier, or employee-uniform pages
- supplier pages, customer/client pages, FAQs, case studies, client rosters, and ordering portals
- workwear or uniform-industry award pages and award profiles
- franchise co-op supplier announcements, approved-supplier materials, FDDs, and registry filings
- trade press, local business press, and legal/labor sources that name the relationship
- SEC, investor-relations, or annual-report sources when they enrich public-company or parent context

These source families are discovery paths, not a closed menu. Generic supplier pages that only say they serve restaurants, anonymous "national restaurant chain" case studies, named restaurant evidence for non-uniform services, employee photos without a named partner link, login-only social/forum fragments, generic search-result/directory/listing pages without the uniform/workwear relationship tie, and broad restaurant filings that mention suppliers generally are out of scope as standalone evidence. Supplier customer/client roster pages can work when they themselves tie the restaurant entity to the uniform/workwear partner relationship.

When the cited page supports them, summarize the chain/operator, parent or franchise co-op, geography, partner role, uniform/workwear scope, program or relationship, relationship/program date or dated relationship evidence, source type, and any public-company ticker/parent context visible on the page. Public-company status is auxiliary context, not an eligibility filter.

Requirements:
- The page must identify the named restaurant chain/operator in a restaurant-chain, franchise, parent/operator, or multi-unit context.
- The page must identify the named supplier or program partner as an outside party distinct from the restaurant chain/operator.
- The page must explicitly connect that partner to the chain/operator in a uniform, workwear, apparel, footwear, rental/laundry, ordering, material, or design-program context.
- The page must expose a tangible program or relationship detail, such as partner role, approved-supplier status, garment or workwear scope, staff role, geography, unit or team-member scale, relationship/program date, launch/event date, a dated source that anchors when the relationship was evidenced, ordering/payment model, material technology, or award-program framing.

Write one JSON object per line to `results_restaurant_uniforms.jsonl`:
{"item": { "restaurant_chain": "<restaurant_chain>", "supplier_partner": "<supplier_partner>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
