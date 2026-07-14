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

## `saas_customer_partnerships`

For 60+ B2B SaaS, cloud-software, security, data, developer, or workflow-automation vendors (not generic consulting agencies or media publishers), find 3+ named customer, integration, marketplace, or technology-partner companies per original company where the relationship is publicly acknowledged back; for each such (`company`, `other_company`) pair and each of the 2 sides of the relationship supply a corroborating source (i.e. 1+ URL).

Vendor sites can make broad customer-logo claims cheaply; the reciprocal acknowledgement is what separates a plausible ecosystem relationship from one-sided marketing.

The relationship sides define the corroborating sources' bars, which we refer to as `source_type`; these are:
- `quote`: a page published by `company` itself that names `other_company` as a customer, integration, partner, marketplace listing, implementation story, or named ecosystem relationship. The bar is lenient: case studies, customer pages, integration directories, marketplace pages, logo walls, press releases, partner announcements, documentation pages, and "trusted by" banners all count when the counterparty is clearly named.
- `backquote`: a page published by `other_company` itself where it independently acknowledges the same relationship. The bar is stricter: procurement pages, engineering/blog posts, app-marketplace pages, integration docs, customer stories, security/vendor pages, joint announcements, or implementation notes count when they say something meaningful about using, integrating with, buying from, or partnering with `company`. A generic logo wall or undifferentiated tool-list mention on the backquote side does NOT count.

Requirements:
- Each URL must be on the hosting party's own domain or an officially-controlled channel. Third-party news outlets, press-wire republications, scraping mirrors, and unrelated aggregators don't count. A marketplace listing (AppExchange, AWS/Azure/GitHub Marketplace, Chrome Web Store, and the like) counts only when it is visibly issued or maintained by the hosting party — an auto-generated directory card or third-party catalog entry doesn't.
- The page must explicitly name the opposite party, or display a named logo / marketplace card / integration title for it. Vague category references like "leading data warehouses" don't count even when the intended counterpart is guessable.
- The relationship must be acknowledged at the bar appropriate to the row's `source_type` — lenient for `quote`, strict for `backquote` — per the definitions above. A one-item-in-a-comma-separated-list mention on the `backquote` side doesn't count.

Write one JSON object per line to `results_saas_customer_partnerships.jsonl`:
{"item": { "company": "<company>", "other_company": "<other_company>", "source_type": "<source_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
