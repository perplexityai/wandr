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

## `mortgage_calculator_surfaces`

For 65+ distinct public consumer-facing provider sites that publish mortgage or home-loan calculator pages, name 1+ calculator surface per provider site. For every calculator surface, supply 1+ URL for each of the 2 evidence axes.

The goal is to map consumer calculator pages that act as acquisition surfaces for lenders, brokers, marketplaces, real-estate portals, publishers, affiliate lead generators, or comparable commercial actors.

Evidence axes:
- `calculator_action`: the calculator page itself shows a mortgage/home-loan calculator and a visible commercial action, such as compare rates, apply, prequalify, view rates, request a quote, contact a loan officer, or get an offer.
- `commercial_identity`: a separate identity, disclosure, licensing, about, legal, affiliate, advertising, or registry page identifies the mortgage lead-generation, lending, brokerage, affiliate, advertising, marketplace, or named partner role that commercially benefits from the surface.

Each provider site should be a distinct public brand or web property presenting the calculator surface. Extra calculator pages from the same site do not replace breadth across different providers. For publisher, portal, affiliate, or marketplace pages, make the mortgage commercial role precise rather than treating generic site identity, a lender partner, and an advertiser relationship as interchangeable.

Requirements:
- The page must tie the evidence to the submitted provider site and calculator surface. For `calculator_action`, the cited URL must be the calculator page itself or a clearly equivalent normalized version. For `commercial_identity`, the cited URL must tie separate identity or disclosure evidence to the same provider site, the same calculator surface, or a named mortgage beneficiary behind that surface.
- The page must communicate the source role for its evidence axis: for `calculator_action`, that it is the calculator page itself; for `commercial_identity`, that it is a distinct URL from the calculator page, such as a same-provider legal / licensing / about / disclosure page, a mortgage affiliate or advertising disclosure, or a recognized licensing / business registry page identifying the provider, beneficiary, or relationship.
- The page must show the axis-specific evidence. For `calculator_action`, this means a mortgage, refinance, home-loan payment, or home-affordability calculator plus a visible commercial action such as compare rates, apply, prequalify, view rates, request a quote, contact a loan officer, or get an offer. The action only needs to be visible on the cited page; the destination after clicking does not need to be reachable. For `commercial_identity`, this means a concrete mortgage commercial identity or relationship signal such as NMLS / licensing information, FDIC / Equal Housing Lender language, direct-lender language, licensed broker or lead-generator language, mortgage affiliate / advertising compensation disclosure, mortgage marketplace or rate-shopping language, or a named lender / partner relationship.

Write one JSON object per line to `results_mortgage_calculator_surfaces.jsonl`:
{"item": { "provider_name": "<provider_name>", "provider_site": "<provider_site>", "calculator_page_url": "<calculator_page_url>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
