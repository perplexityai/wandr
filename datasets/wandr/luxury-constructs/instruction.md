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

## `luxury_constructs`

Find 16+ luxury construct alignments where the same construct topic and comparison focus can be evidenced from Kantar and from each of three adjacent public-source families. For each construct alignment, supply 4+ source-role URLs, one for every evidence role listed below, with each URL independently supporting its role's side of the shared alignment.

A construct alignment is not a document summary or a generic theme such as "luxury market." It names a specific luxury construct topic plus the basis for comparison: a definition or boundary, construct dimension, consumer segment, methodology/scope, market universe, or public access/methodology state that can be compared across the Kantar anchor and the adjacent evidence roles. Comparable does not mean identical wording, but each role's page should make the same construct topic and comparison focus visible without unsupported synthesis.

Evidence roles:
- `kantar_anchor`: Kantar-owned, Kantar BrandZ, Kantar Marketplace, BrandSnapshot, Kantar inspiration, Kantar country/regional/localized, or officially hosted Kantar asset evidence.
- `consulting_or_data_provider_comparator`: Reputable consulting, data-provider, consumer-research, or market-intelligence evidence outside Kantar.
- `trade_or_association_comparator`: Trade-association, industry-body, Altagamma-style, or public industry-report evidence outside Kantar.
- `academic_or_public_research_comparator`: Peer-reviewed, university, institutional, or public-research evidence outside Kantar.

Positive evidence needs exact luxury language from the source. Definition/boundary alignments need definition, qualification, inclusion, or exclusion language. Construct-dimension alignments need construct language such as exclusivity, craftsmanship, heritage, status, sustainability, experience, meaning, quality, selectivity, or similar. Consumer-segment alignments need buyer, cohort, attitudinal, spending, or luxury-customer language. Methodology/scope alignments need methods, sampling, measurement, valuation, survey, data-availability, market/category/geography, goods/services, ranking, company-universe, or industry-universe language tied to luxury analysis. Public access or methodology-absence alignments count only when the page is clearly luxury-relevant and the public surface itself supports a visible access state, absence of definition, absence of public methodology, stale/gated access, unclear scope, or conflicting scope.

Requirements:
- The page must communicate its source identity and fit the claimed evidence role. `kantar_anchor` must be a Kantar-owned or officially hosted Kantar public surface. The three comparator roles must be non-Kantar sources in the stated adjacent family.
- The page must discuss luxury as a brand, category, consumer, market, measurement, or research construct. A page that merely mentions a luxury brand in unrelated news, SEO copy, or brand-promotion commentary does not count.
- The page must state explicit luxury evidence matching the submitted construct topic and comparison focus. A market or ranking universe is not automatically a definition; generic BrandZ or brand-equity methodology is not a luxury methodology/scope alignment unless the page ties that methodology to luxury analysis; ordinary positive claim language is not a public access or methodology-absence state.
- The page must support enough context to compare its evidence with the same construct alignment on the other source roles: date or publication state, market/geography/category scope where present, source/access/methodology state, and construct or boundary meaning without unsupported synthesis.
- Do not reuse the same broad public report page under many construct alignments by relabeling thin market-universe or ranking mentions. Each alignment needs a distinct construct topic and comparison focus, and each role URL needs source text that actually bears that alignment.

Write one JSON object per line to `results_luxury_constructs.jsonl`:
{"item": { "construct_topic": "<construct_topic>", "comparison_focus": "<comparison_focus>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
