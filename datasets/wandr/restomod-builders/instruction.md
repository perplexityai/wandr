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

## `restomod_builders`

For 800+ classic-car restomod builders or clearly branded restomod programs, supply evidence for each of the 2 evidence types, with 1+ source URL per type. The builder universe is open; the point is public verification beyond the famous listicle core, not a buyer guide or ranking.

The evidence types are:
- `builder_identity`: a builder-owned site, branded-program page, official company profile, or similarly durable source that identifies the builder/program and shows public classic-vehicle modernization services.
- `output_or_program`: a project-specific, completed-build, active model/program, show/award, auction/listing, media, or high-signal public source tying the same builder/program to completed output or public build capability.

For downstream reading, optional factual notes can include the canonical builder or program name, headquarters or primary public location when available, country or region, platform or specialization, modernization type, official builder URL when known, source type, checked date, evidence signal, and boundary notes. Use 2026-06-29 as the checked date unless the source was checked later.

Useful modernization signals include:
- `engine or powertrain swap`
- `EV conversion or electromod`
- `chassis, frame, or suspension engineering`
- `brake, steering, electronics, HVAC, or drivability upgrades`
- `bespoke interior or comfort-system modernization`
- `body engineering, metal fabrication, or widebody work tied to a build`
- `turnkey re-engineered classic vehicle program`
- `completed restomod, pro-touring, outlaw, reimagined, or restored-and-enhanced build`

Source type should be factual, not promotional. Useful public source types include:
- `official_builder_site`
- `official_project_gallery`
- `branded_program_or_model_page`
- `show_or_award_page`
- `auction_or_listing_page_naming_builder`
- `automotive_media_profile_or_feature`
- `entity_specific_specialist_directory_or_profile`
- `public_video_or_social_with_clear_builder_build_identity`
- `other_public_source`

Boundary classes to keep out unless the page also proves turnkey restomod-builder substance:
- `restoration-only or concours shop`
- `ordinary repair or maintenance shop`
- `parts, chassis, kit, or platform supplier without turnkey build evidence`
- `dealer, marketplace, or auction house without in-house builder evidence`
- `continuation, replica, or body-shell program without modernized-classic builder evidence`
- `media/listicle brand, broad directory/listicle page, or private one-off project`

Public sources can include official builder sites, model/program pages, detailed project galleries, show or award pages, auction or listing pages that name the builder, automotive magazine profiles or features, entity-specific specialist directory profiles, and high-signal public video or social pages where the builder and build are clearly identified. Broad directories, listicles, and generic "best restomod" articles are discovery surfaces; an entity-specific profile from a directory, magazine, or social/video page counts only when the submitted page itself supports the claimed evidence role and modernization substance. Private or gated material, quote-request funnels, rankings, procurement advice, broad marketplace category pages, customer reviews without builder/build facts, and generic SEO pages are out of scope.

Requirements:
- The page must identify the claimed builder or branded program with enough public context to distinguish it from unrelated same-name shops, vehicle models, project names, owners, dealers, directories, or media brands.
- The submitted page itself must support the claimed `evidence_type`: `builder_identity` evidence should be builder-controlled or official/durable identity evidence for public restomod services or a branded program; `output_or_program` evidence should show a completed build, named project, active build/model program, show or award record, auction/listing attribution, media feature, or comparable public output/build-capability signal for the same builder.
- The page must support substantive modernization of classic vehicles by the claimed builder or program. Literal "restomod" wording is not required, but restoration-only, repair-only, cosmetic-only, parts-only, kit/platform-only, dealer-only, replica-only, continuation-only, directory-only, and private one-off evidence does not establish the bar.

Write one JSON object per line to `results_restomod_builders.jsonl`:
{"item": { "builder": "<builder>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
