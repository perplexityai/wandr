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

## `cgt_cryopreservation_bag_distributor`

For at least 16+ country or territory markets, name at least 4+ public local channel surfaces per market that carry cell-and-gene-therapy-relevant cryopreservation or freezing bag products, and cover the 2 evidence facets listed below for each market/channel pair with a source (i.e. 1+ URL under each facet).

Evidence facets:
- `channel_product_fit`
- `local_market_channel_signal`

`channel_product_fit` is for public evidence that the submitted channel, channel catalog, reseller surface, marketplace/local supplier page, or public institutional supplier source is tied to a named cryopreservation or freezing bag product or product family.

`local_market_channel_signal` is for public evidence that the submitted channel is tied to the submitted market and to a local route role: distributor, reseller, importer, local catalog/storefront, marketplace supplier, public institutional supplier, or clearly labeled manufacturer-direct/local affiliate.

Rows are neutral public source evidence only. They should not rank vendors, recommend a purchase route, guarantee availability, extract prices or contact details, provide outreach targets, or give clinical or lab-protocol guidance. Current public pages and exact source-dated pages both count; a missing publication date is not itself a failure.

Requirements:
- The page must identify the submitted channel or a channel-owned/listing context for that channel.
- The page must make its facet-appropriate source role visible. For `channel_product_fit`, the source role must be a channel-specific product page, channel catalog/storefront, reseller or marketplace supplier listing, public institutional supplier page, or a manufacturer/locator page that publicly names the submitted channel or market route; a generic manufacturer product page is not enough by itself. For `local_market_channel_signal`, the source role must visibly tie the submitted channel to the submitted market and a public route role.
- The page must expose the facet-specific evidence. For `channel_product_fit`, it must name a qualifying flexible cryopreservation/freezing bag or bag set, not just cryovials, rigid cryocases, cryogenic boxes/racks, freezing media or DMSO, tanks/freezers, bag-freezing presses, cassettes, general cell-culture/bioprocess bags, transfer bags, collection-only bags, or broad equipment categories. For `local_market_channel_signal`, it must show the submitted market and route role for the submitted channel without relying only on a contact form, phone/email listing, broad market report, or unsupported availability claim.

Write one JSON object per line to `results_cgt_cryopreservation_bag_distributor.jsonl`:
{"item": { "market": "<market>", "channel": "<channel>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
