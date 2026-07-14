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

## `us_outplacement_provider_public_capability_provenance`

Identify 100+ providers as US-facing outplacement or career-transition providers; for each provider, cover each of the 3 capability facets listed below with a public capability-provenance source (i.e. 1+ URL per facet).

The purpose is public, source-stated capability provenance, not provider ranking, agency recommendation, procurement or pricing advice, outreach, lead scoring, LinkedIn harvesting, contact enrichment, decision-maker identification, emails, or phone collection.

Capability facets:
- `official_service`: a provider-controlled service, capability, program, or product page source-stating an in-scope service line such as outplacement, career transition, redeployment/internal mobility for displaced workers, executive transition, or layoff career coaching.
- `delivery_or_reach`: a provider-controlled or provider-specific page showing how or where the service is delivered, such as delivery model, geography/service region, buyer or employee segment, program structure, coaching model, technology/platform, virtual/in-person model, or comparable reach signal.
- `client_or_public_use_signal`: a case study, concrete client/outcome page, public contract/vendor record, employer disclosure, HR marketplace/profile page, or reputable HR trade/analyst article tying the provider to a concrete public use, engagement, program, client context, or outcome.

A valid `provider` is a real public provider of outplacement, career-transition, redeployment, executive-transition, layoff-career-support, or comparable workforce-transition services with a US-facing service, market, employer, client, contract, or public-use context. Pure staffing firms, job boards, public workforce boards, generic career coaches, broad HR consultants, directories, ranking/listicle publishers, contact databases, and lead-enrichment pages do not count without source-stated outplacement or career-transition provider capability. The cited page itself must visibly carry enough public content to evaluate the capability claim.

Requirements:
- The page must clearly identify the named provider.
- The page must establish the US-facing outplacement or career-transition service scope: a US service/market/region context, US employer/client/contract/disclosure context, or a provider-controlled US-facing service page for outplacement, career transition, redeployment/internal mobility for displaced workers, executive transition, layoff career coaching, or comparable workforce-transition support.
- The page should visibly earn the source role appropriate to `capability_facet`: for `official_service`, a provider-controlled service/capability/program/product surface; for `delivery_or_reach`, a provider-controlled or provider-specific delivery, geography, program, coaching, technology/platform, or buyer/employee segment surface; for `client_or_public_use_signal`, a provider-specific case, client/outcome, public contract/vendor, employer disclosure, HR marketplace/profile, or reputable HR trade/analyst surface. Generic rankings, SEO listicles, broad directories, marketplace search results, and analyst/vendor pages used only for recommendation or ranking context do not count.
- The page must state a concrete facet-scoped finding: for `official_service`, the in-scope service line or capability; for `delivery_or_reach`, the delivery, reach, platform, coaching, region, population, program-structure, or buyer/employee segment detail; for `client_or_public_use_signal`, the concrete client, public use, engagement, contract, employer context, outcome, case, or comparable provider-specific use signal.

Write one JSON object per line to `results_us_outplacement_provider_public_capability_provenance.jsonl`:
{"item": { "provider": "<provider>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
