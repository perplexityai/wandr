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

## `taipei_car_detailing_shops`

For 30+ shops, cover the 3 evidence facets listed below for each shop by supplying a source (i.e. 1+ URL under each facet) which exposes a focused, substantive finding clearly scoped to the facet in question.

The goal is to surface the strongest Taipei shops in this trade — the ones whose offering, customer reception, and social presence each leave a real, verifiable mark — rather than a bare directory listing.

Evidence facets:
- `service_offering`: the shop's own public statement of which of these services it performs and how it presents that work
- `customer_sentiment`: public customer reaction to the shop's work or service experience
- `social_engagement`: the shop's public social presence and the real audience engagement on it

Requirements:
- The page must clearly identify the named shop. The page URL or title may stand in for this shop identity, but every other requirement below must be carried by the load-bearing evidence in the page body text itself, not left to be inferred from the URL slug or page title.
- The page must credibly tie the shop to a Taipei-area location or service market — a Taipei/New Taipei district, address, or branch line, or other clear Taipei-area operating signal — appearing in the excerpted body text.
- The page must make its facet-appropriate source role visible in the excerpted body text. For `service_offering`, this comes from shop-owned page or account identity text presenting the work — a service menu, price list, service-category headings, branch or 門市 listing, or owned social/profile identity naming the shop. For `customer_sentiment`, the page must be recognizable as a review or user-reaction surface, e.g. through reviewer names, review dates, star or score counts, "評論" / "評價" / "reviews" wording, forum-thread or recommendation-roundup framing, or platform wording unambiguously indicating user-generated reactions. For `social_engagement`, the page must read as the shop's own social account surface, e.g. through a profile header, handle, follower or 粉絲 count, post feed, or per-post like / comment / view counts.
- The page must expose a focused finding clearly scoped to the named shop and evidence facet, present in the excerpted body text. For `service_offering`, this means a concrete service signal — a named tinting / PPF / ceramic-coating offering, a service-package or price detail, a specialization claim, or a stated technique or product line. For `customer_sentiment`, it means a specific rating pattern, review-volume signal, named praise, complaint, or recurring customer observation. For `social_engagement`, it means a concrete engagement signal — a follower-count figure, a post's like / comment / view tally, a saved-work or case post drawing reactions, or another real-audience-interaction detail, not a bare subscriber number standing alone.

Write one JSON object per line to `results_taipei_car_detailing_shops.jsonl`:
{"item": { "shop": "<shop>", "service_facet": "<service_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
