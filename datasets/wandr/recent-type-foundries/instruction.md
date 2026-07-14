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

## `recent_type_foundries`

For 150+ type foundries or foundry-like public type ventures that became publicly visible during January 1, 2024 through June 26, 2026, supply evidence for each of the 2 evidence kinds and at least 1+ URL per kind. The public venture can be an independent foundry, solo type practice, design-studio foundry arm, educational or student foundry, institutional foundry, marketplace-native foundry, or broader design practice with a public type catalog.

The evidence kinds are:
- `identity_active`: a foundry-owned, official marketplace / distributor, or entity-specific durable profile / catalog source for the foundry-like entity that also shows active catalog, public typeface availability, type services, or comparable public availability.
- `dated_event`: a dated public source for a recent event such as founding, public launch, storefront/catalog launch, first retail typeface, distributor or marketplace onboarding, rebrand, or an explicitly ambiguous/conflicting date claim.

For each source, report the foundry geography when public, entity type, official or durable identity URL, observed date or year where one is being claimed, date semantics, source type, source publication date or visible date, checked date, active-availability signal, confidence, and any missing / corroboration / conflict state. Use 2026-06-26 as the checked date unless the source was checked later.

Date semantics should use these meanings when they fit:
- `founding`
- `public_launch`
- `storefront_or_catalog_launch`
- `first_retail_typeface`
- `distributor_or_marketplace_onboarding`
- `rebrand_or_continuation`
- `ambiguous_or_conflicting`

Source type should be factual, not promotional. Useful public sources include official foundry pages, dated launch posts, type or design publications, curated type databases, institutional news, distributor or marketplace pages, release feeds, and corroborated public social posts. Private or gated communities, contact enrichment, prospecting data, pricing / licensing advice, font-shopping recommendations, popularity rankings, visual quality judgments, and brand critique are out of scope. Editorial lists, year-founded indexes, roundup/news hubs, and directory list pages can be discovery surfaces, but the cited evidence still needs factual entity-specific identity or event support.

Requirements:
- The page must identify the claimed foundry or foundry-like entity and give enough public context to distinguish it from a typeface family, a distributor, a generic design studio with no public type offering, or a private portfolio fragment.
- The page must fit the claimed `evidence_kind`: `identity_active` evidence should be a foundry-owned page, official marketplace / distributor profile, or entity-specific durable profile / catalog page that shows active catalog, public typeface availability, type services, or comparable public availability; `dated_event` evidence should show a dated event or date claim in the target window.
- The page must make the event date semantics or active-public status clear enough to classify what the source date proves. A publication date, founded year, product release date, storefront launch date, distributor onboarding date, and rebrand date are different claims unless the source ties them together.
- Broad year-founded pages, directory indexes, news roundups, search / category pages, and other multi-foundry hub pages cannot satisfy `identity_active` merely because they list a foundry, link to its site, or imply that listed foundries are active. Such pages can support `dated_event` only when the row-specific text for the submitted foundry actually supports the observed date or year and the submitted date semantics.
- The record must preserve ambiguity and false-positive states: conflicting dates, social-only or marketplace-only leads, missing official dates, old foundries with recent platform events, first typefaces that predate a foundry launch, distributor joins mistaken for founding, and duplicate / rebrand / continuation cases should be labeled rather than recast as clean new foundings.

Write one JSON object per line to `results_recent_type_foundries.jsonl`:
{"item": { "foundry": "<foundry>", "evidence_kind": "<evidence_kind>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
