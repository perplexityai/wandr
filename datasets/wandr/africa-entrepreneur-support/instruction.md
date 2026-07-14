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

## `africa_entrepreneur_support`

For 10+ African countries, cover each of the 5 support roles listed below with at least 5+ named public support actors or programs per country-role cell; for each (`country`, `support_role`, `actor`) combination, supply an actor/program-scoped public source (i.e. 1+ URL) showing the actor/program, the country or market tie, the support role, and the impact / small-and-growing-business / social-enterprise relevance.

This is public ecosystem-infrastructure provenance, not a startup ranking, funding tracker, investment screen, grant-application guide, contact list, outreach workflow, lead score, dashboard, alert, or strategy recommendation.

Support roles:
- `accelerator_or_incubator`: a structured accelerator, incubator, cohort, venture-studio, or incubation program that develops entrepreneurs or ventures
- `innovation_hub_or_venture_builder`: a hub, lab, coworking / maker / prototyping space, venture builder, or founder-support platform that helps entrepreneurs build enterprises
- `capital_grant_or_dfi_program`: a grant, non-dilutive finance, impact-investment facility, DFI-backed program, foundation facility, or public/private capital-support program
- `government_academic_or_public_program`: a government, university, public agency, or publicly backed institutional program supporting entrepreneurship, innovation, SGBs, or ventures
- `ecosystem_builder_network_or_research_initiative`: a network, association, ecosystem builder, research/mapping initiative, or capacity-building body strengthening entrepreneur-support ecosystems

The submitted actor ought to be a named real organization, program, fund or facility, hub, institution, initiative, network, research body, or ecosystem body that supports entrepreneurs or enterprises. A venture receiving support does not count as the actor unless the same named entity is also shown supporting other entrepreneurs or enterprises. The same actor can appear in multiple country-role cells only when the page supports the distinct country and role in each cell. Sources should be fully public, accessible, and usable.

Requirements:
- The page must clearly identify the named actor or program.
- The page should communicate that the source is actor/program-scoped evidence: an official page for the named actor/program; an official operator, host, sponsor, or funder page for the named program; or a genuinely dedicated public profile, report section, database entry, or article section focused on that named actor/program. Broad country ecosystem guides, country startup directories, maps, listicles, or database pages do not satisfy this requirement when the actor appears only as one item among many country resources.
- The page must tie the actor or program to the submitted African country or market through a source-stated presence, eligibility scope, chapter/location, portfolio or support activity, country coverage, report entry, or comparable country-level market link.
- The page must show the selected support role. For `accelerator_or_incubator`, it should show accelerator, incubator, cohort, venture-development, or incubation support. For `innovation_hub_or_venture_builder`, it should show a hub, lab, coworking / maker / prototyping space, venture-building, or founder-support platform role. For `capital_grant_or_dfi_program`, it should show grant, non-dilutive finance, investment-facility, DFI-backed, foundation, public-capital, or comparable capital-support activity. For `government_academic_or_public_program`, it should show a government, university, public-agency, or publicly backed institutional program role. For `ecosystem_builder_network_or_research_initiative`, it should show network, ecosystem-building, research/mapping, association, or capacity-building activity for the entrepreneur-support ecosystem.
- The page must connect the actor or program to entrepreneurship, startups, small and growing businesses, social enterprise, impact ventures, inclusive economic development, or concrete public-interest enterprise sectors such as climate, health, agriculture, education, women/youth inclusion, financial inclusion, workforce development, or comparable impact domains.

Write one JSON object per line to `results_africa_entrepreneur_support.jsonl`:
{"item": { "country": "<country>", "support_role": "<support_role>", "actor": "<actor>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
