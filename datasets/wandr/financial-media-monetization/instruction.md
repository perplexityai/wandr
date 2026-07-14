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

## `financial_media_monetization`

For at least 120+ financial-media, investing-newsletter, stock-research/tool, market-data, or adjacent investor-information publishers, supply public monetization-provenance artifacts. Cover at least 3 artifact roles per publisher, with at least 1 concrete artifact/surface and 1+ URL per role.

This is public business-model provenance, not business-model inference. A row ties a publisher, an artifact role, and a concrete public surface to a source-stated or source-observed monetization, product, placement, disclosure, or paid-relationship fact. MarketBeat is a useful anchor, but the coverage should not center on MarketBeat or on any one media kit.

Artifact roles:
- `official_product_surface`: publisher-owned product, pricing, premium-service, newsletter, tool, market-data, membership, or subscription surface.
- `ad_or_sponsorship_surface`: publisher-owned advertiser, media-kit, sponsorship, ad-product, audience, rate, email, podcast, event, or brand-studio surface.
- `paid_relationship_artifact`: public sponsored-content example, sponsored newsletter/example issue, affiliate/performance offer, partner/lead-generation funnel, native-ad placement, or similar paid-relationship artifact.
- `policy_disclosure_surface`: disclosure, terms, affiliate policy, sponsored/native-content policy, advertising disclosure, or comparable page that source-states commercial relationship rules.
- `filing_or_investor_context`: SEC filing, annual report, investor presentation, earnings release, or comparable parent-company material that ties revenue mechanisms to the publisher, brand, segment, or portfolio with an explicit attribution limit.

Each artifact should be public and factual. Name the monetization or relationship channel being evidenced, the concrete product/ad/newsletter/disclosure/filing surface, the source class or role, any source date or observed/checked date needed for time-sensitive observations, and any no-official-source / no-monetization-source / no-disclosure-source / no-example-source / no-date / name-conflict / attribution-limit state that the cited public artifact itself supports. You may include an auxiliary confidence label as row context; confidence is not part of the provenance bar.

Exclude replication playbooks, competitive strategy, financial advice, compliance advice, publisher rankings, ad-sales recommendations, sales-contact lookup, emails, phone numbers, contact enrichment, private newsletter issues, and non-public archives.

Requirements:
- The page must clearly tie the artifact to the named publisher, publisher-owned brand, or relevant parent/segment when the row is explicitly parent-contextual.
- The page must fit the claimed `artifact_role` and make the artifact/source role visible.
- The page must support a concrete monetization or paid-relationship provenance fact as source-stated or source-observed public evidence, not merely generic industry inference.
- The page must support the row's provenance framing: source class or role, concrete surface/product/placement/disclosure/filing detail, any claimed disclosure evidence or attribution limit, any claimed missing/conflict state, and a date or checked-date frame for volatile prices, audience claims, sponsorship examples, ad units, or observed page modules.

Write one JSON object per line to `results_financial_media_monetization.jsonl`:
{"item": { "publisher": "<publisher>", "artifact_role": "<artifact_role>", "artifact_surface": "<artifact_surface>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
