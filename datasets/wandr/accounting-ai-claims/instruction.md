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

## `accounting_ai_claims`

For 18+ AI-positioned accounting or finance automation platforms, supply 3+ concrete workflow claims per platform. For each claim, cover each of the 2 evidence families below with 1+ public URL. Each claim should state what a named product, platform, module, or agent does in an accounting or finance workflow.

Evidence families:
- `shipped_change`: vendor-controlled or vendor-authorized evidence that the capability is recently shipped, launched, updated, documented, or publicly available since the date window below.
- `use_or_ecosystem`: field, customer, marketplace, partner, advisor, implementation, review, or independent-public evidence that corroborates the same workflow beyond a generic vendor product page.

For `shipped_change`, the page must carry a visible publication, release, update, documentation, version, launch, marketplace-availability, or similar currency signal on or after 2024-01-01. A static generic product page with no visible date, version, or availability/change cue is too thin for this family even when it states the capability.

For `use_or_ecosystem`, the page must show the same workflow in field, customer, marketplace, partner, advisor, implementation, review, or independent-public context. A generic vendor product, module, feature, docs, or release page cannot fill this family by itself; a named customer case study, public app-store listing, partner implementation page, practitioner writeup, user-review surface, or comparable adoption/ecosystem page can work when it gives claim-bearing text.

Sources must be public, accessible, and usable. Generic listicles, buyer guides, SEO comparisons, broad thought leadership, educational GAAP/IFRS/tax explainers, quote-only outcome pages, image-only logo grids, login screens, and pages that merely say a tool is AI-powered or integrated do not count. Developer/API pages count only when they expose accounting or finance workflow objects or actions, not merely generic API availability.

The same public page may support several distinct claims only when each claim has its own concrete action-level support on the page. Each submitted URL must satisfy the evidence family named for that submission.

Keep standards, integrations, security, pricing, regions, and suitability as explicit observations only when the page itself says them; they are not substitutes for the workflow claim.

Requirements:
- The page must clearly identify the named platform, product, module, or agent in an accounting or finance automation context.
- The page must support the submitted workflow claim as a concrete product capability in that platform context.
- The page must satisfy the submitted evidence family's source role for the same workflow claim.
- The claim evidence must say what the product, module, or agent does in the workflow, rather than only saying it is AI-powered, time-saving, enterprise-ready, secure, integrated, or suitable for a customer segment.

Write one JSON object per line to `results_accounting_ai_claims.jsonl`:
{"item": { "platform": "<platform>", "workflow_claim": "<workflow_claim>", "evidence_family": "<evidence_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
