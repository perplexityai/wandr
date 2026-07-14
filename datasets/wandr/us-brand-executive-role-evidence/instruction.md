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

## `us_brand_executive_role_evidence`

For each of the 4 role families, supply current public role evidence for 44+ named executives or founder/public role holders at eligible consumer-facing companies or brands; for every such (`company_or_brand`, `person`) relationship and each of the 2 evidence sides, supply 1+ URL whose page independently supports the person, company or brand, current title, founder/public role, or leadership role, and role-family fit as of 2026-06-26.

The role families are:
- `chief_executive`: CEO, president and CEO, brand president, division/studio president, or equivalent public top executive for the company or brand.
- `top_marketing_brand`: CMO, chief brand officer, chief marketing/growth/communications leader, chief customer officer where brand or marketing scope is explicit, or equivalent top brand and marketing leadership.
- `top_creative_design`: chief creative officer, chief design officer, executive creative director, creative director, head/VP of design, studio chief creative officer, or equivalent senior brand-side creative/design leader whose role source places them over creative direction, product/industrial/packaging design, brand design, design studio output, or consumer experience/store design.
- `founder_public_role`: founder or co-founder currently presented in a public founder, executive, chair, strategic, or comparable leadership role for the company or brand.

The evidence sides, which we refer to as `evidence_axis`, are:
- `brand_controlled`: an official brand/company leadership page, officer bio, newsroom announcement, investor page, annual/proxy report, official brand story or product/design page, official regional brand site, or comparable brand-controlled public source.
- `independent_dated`: a reputable independent business, advertising, design, retail, entertainment, trade, association, award/event, profile/interview, podcast/show-note, or news source with a visible publication date or dated event context.

LinkedIn-only evidence, people-search/contact pages, scraped executive directories, generic rank/list pages without a direct role claim, unsupported search snippets, PR-wire copies as independent evidence, stale former-role pages, role-transition speculation, future-effective roles not yet active on 2026-06-26, and pages about private outreach/contact enrichment do not count.

Eligible companies or brands are consumer-facing and either U.S.-headquartered, have an official U.S. business or U.S. regional brand presence, or are global consumer brands with substantial U.S. market operations. The submitted relationship should keep global corporate, U.S. regional, parent-company, sub-brand, studio, or division scope clear; a globally obvious consumer brand does not need every role page to restate its U.S. market operations, but U.S.-regional, parent/sub-brand, studio/division, or otherwise ambiguous scope needs explicit page support.

Requirements:
- The page should fit the selected `evidence_axis`: official brand/company control for `brand_controlled`, or independent publisher/event standing plus a visible date or dated context for `independent_dated`.
- The page must identify `company_or_brand` at the submitted scope; U.S.-regional, parent/sub-brand, studio/division, or otherwise ambiguous scopes must be explicit on the page.
- The page must name `person` and tie that person to the claimed company or brand in an executive, founder, or senior leadership context.
- The page must state the person's current title, founder/public role, or current leadership role as of 2026-06-26; an old appointment article alone does not prove currentness, and a future-effective transition does not count before its effective date.
- The page's title, role description, or remit must fit the selected `role_family`.

Write one JSON object per line to `results_us_brand_executive_role_evidence.jsonl`:
{"item": { "role_family": "<role_family>", "company_or_brand": "<company_or_brand>", "person": "<person>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
