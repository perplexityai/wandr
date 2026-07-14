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

## `solar_rri_providers`

For 500+ U.S. residential rooftop solar providers that publicly offer solar panel removal and reinstallation, detach/reset, or solar reroof R&R services, supply evidence for each of the 2 evidence types and at least 1+ URL per type. Include providers from many states or metro markets; Philadelphia and the Delaware Valley are useful seed regions, but the provider universe is open.

The evidence types are:
- `rri_service`: a primary provider source, usually the provider's own page or official profile, that explicitly offers residential rooftop solar panel removal and reinstallation, detach/reset, or solar reroof R&R.
- `public_accountability`: a separate non-company public source showing provider-specific public facts such as local or regional operation, registration, license, certification, program participation, permit activity, trade recognition, or comparable accountability signal.

For downstream reading, include the canonical provider name, legal name or DBA when the source reveals one, official company URL when known, home region or service regions, provider archetype, R&R scope or accountability signal, independent source type when relevant, public registration or credential ID when relevant, pricing or process detail if public, checked date, confidence, and source notes. Use 2026-06-29 as the checked date unless the source was checked later.

Useful R&R service language includes:
- `solar panel removal and reinstallation`
- `solar removal and reinstall`
- `solar detach and reset`
- `solar reroof R&R`
- `remove, store, and reinstall panels for roof work`
- `remove and replace panels during roof repair or replacement`
- `temporary solar array removal with recommissioning or system testing`

Useful provider archetypes include:
- `solar-native installer`
- `solar service or R&R specialist`
- `roofer with explicit solar R&R coordination`
- `roof-and-solar integrated contractor`
- `national or multi-state solar service provider`
- `mixed residential/commercial provider with residential rooftop evidence`

Independent source type should be factual, not promotional. Useful independent source types include:
- `state contractor registry or registration search`
- `municipal license or contractor lookup`
- `certification or credential directory`
- `vetted public program roster`
- `utility or interconnection program list`
- `public permit record or permit database`
- `trade publication or industry ranking`
- `industry association member directory`
- `provider-specific public directory profile`
- `other independent public accountability source`

Public sources can include provider service pages, official provider profiles, state contractor registries, municipal license lookups, certification directories, public program rosters, utility or interconnection lists, public permit records, trade publications, industry association pages, and provider-specific public directory profiles. Directory, credential, recognition, and public-profile pages are useful only when they are provider-specific and public enough to identify the submitted company or organization. Generic solar installer lists, review-only pages, customer reviews, and search results can help discovery or secondary context, but they do not prove the R&R offering unless the page itself contains explicit, provider-specific R&R proof; they also do not prove public accountability unless the page carries a concrete provider-specific accountability fact. Private lead-enrichment databases, quote-request funnels that do not identify a real provider, procurement advice, rankings, and "best provider" recommendations are out of scope.

Requirements:
- The page must identify the claimed provider, or bridge the submitted trade name to a legal/DBA name, with enough public context to distinguish it from unrelated same-name companies.
- The page must fulfill the claimed `evidence_type`: `rri_service` evidence should be a primary provider source for the R&R offering, while `public_accountability` evidence should come from a separate non-company public source for the submitted provider.
- The page must support concrete provider substance at the claimed evidence type. For `rri_service`, it should explicitly show residential rooftop solar panel removal and reinstallation, detach/reset, or solar reroof R&R for roof repair, roof replacement, relocation, or comparable homeowner work. For `public_accountability`, it should show a concrete public accountability fact for the same provider, not just a name-only profile, generic installer listing, or customer-opinion page.

Write one JSON object per line to `results_solar_rri_providers.jsonl`:
{"item": { "provider": "<provider>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
