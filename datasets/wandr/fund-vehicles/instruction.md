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

## `fund_vehicles`

For 80+ private-capital fund managers, name 2+ named fund vehicles per firm; for each fund vehicle and each of the 3 evidence facets listed below, supply 1+ URL on a page carrying public provenance for that facet.

The purpose is public fund-vehicle provenance, not fund performance analysis, LP mapping, legal-compliance assessment, investment recommendations, returns, DPI/IRR, or portfolio-quality judgment.

The evidence facets of interest, which we refer to as `evidence_facet`, are:
- `official_existence_or_close`: a firm- or fund-controlled public source states fund existence, close, size, vehicle identity, or a comparable fund fact.
- `regulatory_registration`: a public financial-regulator, filing, register, adviser, issuer, offering, or equivalent official public record names the vehicle, issuer, or registrant.
- `mandate_or_strategy`: a firm- or fund-controlled source, or an official public source, states the fund's asset class, stage, sector, geography, financing product, investment criteria, or comparable mandate.

A valid `firm` is a real venture, growth equity, private equity, private credit, secondaries, or comparable private-capital fund manager. Portfolio companies, bank product pages, ETF or mutual-fund issuers, accelerator directories, generic investor lists, and similar non-manager surfaces are outside scope.

A valid `fund_vehicle` is a named pooled or private fund vehicle tied to the claimed firm, such as a vintage fund, Fund II/III/IV, growth debt fund, secondaries fund, fund LP, or comparable vehicle. Strategy labels, product categories, portfolio companies, broad brand pages, and SPV-like deal names without fund-vehicle evidence are outside scope.

Requirements:
- The page must clearly identify the named fund vehicle and tie it to the claimed firm.
- The page must visibly earn the source role for the selected `evidence_facet`: for `official_existence_or_close`, it should be firm/fund controlled; for `regulatory_registration`, it should be a regulator, filing, register, adviser, issuer, offering, or equivalent official public record; for `mandate_or_strategy`, it should be firm/fund controlled or an official public source.
- The page must state the facet-specific finding as public provenance: existence, close, size, or vehicle identity for `official_existence_or_close`; public-record registration, filing, issuer, offering, or comparable record identity for `regulatory_registration`; asset class, stage, sector, geography, financing product, investment criteria, or comparable mandate for `mandate_or_strategy`.

Broad third-party databases, generic investor lists, press-wire republications, listicles, and outside news pages may be useful for discovery, but they usually do not carry the official, regulatory, or fund-controlled source role unless the page itself is the official public record or controlled source for the claimed facet.

Write one JSON object per line to `results_fund_vehicles.jsonl`:
{"item": { "firm": "<firm>", "fund": "<fund>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
