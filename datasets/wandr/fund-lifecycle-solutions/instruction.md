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

## `fund_lifecycle_solutions`

Build a public-source provenance atlas for late-life private-fund and GP-led liquidity providers. For each `role_family` below, identify 8+ US-linked firms or professional-services platforms and cover the 3 evidence types for each firm-role with public sources (i.e. 1+ URL under each evidence type). The same firm can appear in multiple role families only when the public role evidence is genuinely distinct.

Role families:
- `replacement_gp_fiduciary`: replacement GP, successor GP, interim manager, independent fiduciary, delegated manager, or comparable control/oversight role for distressed, disputed, illiquid, tail-end, or late-life private funds.
- `wind_down_tail_end`: end-of-fund-life wind-down, tail-end asset realization, managed exit, portfolio liquidation, fund closure, legacy-disposal, or private-fund liquidation support.
- `gp_led_capital`: capital provider, lead/co-lead investor, preferred-equity provider, or liquidity-capital platform for GP-led secondaries, continuation vehicles, fund recapitalizations, tender offers, or similar private-fund liquidity solutions.
- `continuation_advisory`: transaction, secondary, capital, or restructuring adviser for GP-led continuation vehicles, fund recapitalizations, tender offers, restructurings, or private-fund liquidity processes.
- `fund_restructuring_counsel`: legal counsel or legal practice evidence for investment-fund restructuring, GP-led conflicts, LPAC/governance process, continuation vehicles, successor-GP mechanics, or fund recapitalizations.
- `fund_admin_ops`: fund administration, operational wind-down, liquidation operations, investor/distribution operations, or compliance support specifically for fund closure, fund liquidation, or managed wind-down.
- `valuation_fairness`: valuation provider, fairness-opinion provider, independent valuation adviser, or financial-opinion role in continuation-vehicle, GP-led, fund restructuring, or late-life private-fund settings.

Evidence types:
- `capability_claim`: public source-worded capability language tied to the claimed role family.
- `practice_provenance`: public evidence that the firm has practiced, launched, advised, counselled, invested, administered, valued, been appointed in, or otherwise publicly participated in the claimed role family. Case studies, named engagements, deal releases, law-firm matter releases, public appointments, SEC or Form ADV language, public LP materials, court/public restructuring documents, and credible trade articles can all work when the role is concrete.
- `us_nexus`: public evidence that the firm or platform is US-linked, such as US headquarters or offices, a US fund/client/transaction, SEC adviser registration, US-facing service language, or US public filing context.

For each source, preserve the public provenance: source-worded role language, source class, source date or observed date, public engagement or filing context when stated, US-nexus detail when relevant, confidence, scope or identity caveat, and any source-grounded missing/conflict state such as `no_official_claim`, `no_named_engagement`, `no_date`, `name_conflict`, `no_public_aum`, `source_scope_unclear`, or `none`. AUM/AUA is optional and should only be included when public, source-stated, and clearly labeled as firm-wide, platform-wide, strategy-specific, or source-scope-limited.

Requirements:
- The page must clearly identify the claimed firm or a source-tied acquired/controlled brand of that firm.
- For `capability_claim` and `practice_provenance`, the page must tie the firm to the claimed role family with private-fund lifecycle substance. Generic "private equity", "secondaries", "fund administration", "restructuring", "liquidation", "GP capital", or "asset management" language is not enough without late-life private-fund, GP-led continuation/liquidity, replacement-GP, wind-down, fund restructuring, tail-end, fund liquidation, or role-equivalent substance.
- For `us_nexus`, the page must provide a public US link for the same firm or platform. A global firm with no visible US tie on the source does not satisfy this evidence type.
- The source shape must match the evidence type. Syndicated copies of the same release can be useful context but should not be treated as a different-nature practice source. Paywalled snippets, private databases, contact-only pages, and bare ranking/list pages do not count as proof.
- Keep the work to public capability provenance. Do not provide contacts, emails, phone numbers, LinkedIn-driven lead discovery, outreach targets, lead scores, LP strategy advice, fund recommendations, manager rankings, investment advice, or private database extraction.

Write one JSON object per line to `results_fund_lifecycle_solutions.jsonl`:
{"item": { "role_family": "<role_family>", "firm": "<firm>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
