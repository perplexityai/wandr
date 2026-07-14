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

## `merchant_bank_platform_incubation_thesis`

For a practitioner evaluating a real-assets capital-markets business thesis, map public precedents for merchant banking in concept, but expressed through platform incubation, GP or manager stakes, and manager-hotel or seeding infrastructure.

Cover 8+ distinct thesis pillars. Each pillar should be a coherent business mechanism, not just a company name or generic investment slogan. For each pillar, name 2+ real public precedent entities: operating platforms, GP-stakes platforms, manager-stakes programs, seeding platforms, manager hotels, transactions, or comparable institutional strategies. For each precedent entity, cover each of the 7 evidence axes below, supplying a source (1+ public, attributable URL per axis).

For each cited source, include a concise finding and practitioner-use note for downstream reading; the source page and excerpts should carry the evidence.

Use these exact evidence-axis labels:

- **business_model** - what the precedent does and how the platform or stake is structured: evidence of the operating model, investment structure, customer or manager segment, product scope, or platform design.
- **capital_base** - committed capital, AUM, deal size, financing base, or scale of funds backing it: a named capital raise, investment amount, AUM figure, transaction value, financing capacity, or institutional capital base tied to the precedent or its market.
- **market_scale** - size, growth, demand, addressable market, or supply-demand imbalance: a quantified market size, activity level, pipeline, demand driver, or supply-demand constraint for the market the precedent pursues.
- **economics** - fee streams, margins, returns, revenue visibility, or ownership economics: evidence of fees, distributions, margins, cash-flow profile, return mechanics, revenue durability, carried-interest economics, or other investment economics.
- **originator_edge** - how a capital-markets, operator, investor, or advisor network creates deal flow: evidence that relationships, sourcing reach, advisor access, operator access, institutional investor access, or repeat capital formation is part of the precedent's edge.
- **value_creation** - post-investment or incubation support that helps the platform grow: evidence of operating support, business services, product launch, capital formation help, M&A, procurement, technology, recruiting, risk management, or other value creation mechanisms.
- **exit_pathway** - monetization path such as sale, IPO, SPAC, realization, recapitalization, or merger: evidence of a realized sale, public listing, SPAC, merger, recapitalization, realization, or other plausible monetization pathway for the platform or manager-stakes strategy.

The research should be useful to a practitioner evaluating whether a capital-markets platform can incubate or sponsor ancillary real-assets and alternative-asset businesses. Useful evidence includes market sizing, committed capital or AUM, investment economics, operating-support mechanisms, deal-flow or originator linkage, manager-stakes precedents, seeding or hedge-fund-hotel precedents, and exit or monetization pathways.

Use public, attributable sources: company disclosures, investor presentations, filings, press releases, reputable business or trade media, institutional research, and academic or industry material. Do not rely on generic blog summaries, search-result pages, AI-generated SEO pages, contact databases, unsourced social posts, or broad encyclopedia pages as final evidence.

Do not submit private deal flow, private contracts, personal contact information, leaked documents, or speculation about a specific individual. Public professional and deal context is acceptable when it is sourced and directly relevant to the precedent.

Requirements:

- The page must link the precedent entity to the claimed thesis pillar, or, for `market_scale`, quantify the market the precedent pursues.
- The page must provide evidence matching the selected evidence axis.
- The cited evidence must be concrete enough for thesis development, not just a generic statement that a market is interesting or a company exists.

Write one JSON object per line to `results_merchant_bank_platform_incubation_thesis.jsonl`:
{"item": { "thesis_pillar": "<thesis_pillar>", "precedent_entity": "<precedent_entity>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
