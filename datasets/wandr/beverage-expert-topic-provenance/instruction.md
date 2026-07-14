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

## `beverage_expert_topic_provenance`

For each of the 8 beverage-innovation topic areas below, identify 17+ public person-topic expertise claims and cover each of the 3 evidence facets for every person-topic claim with a source (i.e. 1+ URL). A person-topic claim is a named individual, a public affiliation or context, and source-stated expertise or work connected to the topic; the same person can appear under more than one topic only when that topic is separately evidenced.

This is public provenance for beverage innovation expertise, not an interview list, contact directory, ranking, lead list, or trend recommendation.

The topic areas of interest, which we refer to as `topic_area`, are:
- `sustainable_packaging`: beverage packaging sustainability, recycled or renewable materials, lower-impact package design, or packaging lifecycle work.
- `refill_reuse_or_circular_packaging`: refill or reuse systems, returnable beverage packaging, circular packaging models, deposit or loop pilots, or other beverage circularity work.
- `paper_bottle_or_fiber_packaging`: paper or fiber bottles, fiber-based liquid packaging, or barriers, liners, closures, and scale-up work for beverage or liquid products.
- `low_no_alcohol`: low-alcohol, non-alcoholic, alcohol-free, or alcohol-alternative beverages and category or product development.
- `functional_ingredients`: functional beverage ingredients and formulation, including adaptogens, nootropics, probiotics, prebiotics, botanicals, electrolytes, proteins, fibers, or comparable ingredient applications.
- `brewing_or_fermentation_science`: brewing, malting, fermentation science, sake, cider, beer science, or upcycled brewing stream work.
- `beverage_processing_or_equipment`: beverage processing, filling, aseptic filling, cold or hot filling, packaging or filling equipment, automation, production technology, or factory-scale beverage operations.
- `beverage_startup_or_brand_innovation`: beverage startup, founder, operator, brand, product, category, or emerging-format innovation.

The evidence facets of interest, which we refer to as `evidence_facet`, are:
- `role_profile`: a person-centered profile, biography, staff/faculty/team, speaker, guest, or comparable role page that gives public identity plus topic-specific beverage role context for the person. A product launch, company news story, market article, or project page that merely names or quotes the person is not role-profile evidence.
- `topic_authority`: a concrete topic-specific authority anchor that states the person's direct responsibility, leadership, authorship, inventorship, technical ownership, research ownership, formulation / process / product-development responsibility, credential, or comparable public authority for named beverage-topic work. A founder title, seniority label, speaker selection, quoted opinion, or broad employer context is not enough by itself.
- `public_contribution`: a public-facing contribution centered on the person as author, named speaker, presenter, interviewee, podcast guest, inventor, publication author, patent contributor, project lead, panelist, or comparable contributor on the topic. A company/product article, launch note, roster, or biography that only mentions or quotes the person is not enough.

The person should be a real, identifiable public individual with source-stated work in the submitted beverage topic rather than an organization, anonymous account, generic team, contact record, influencer shell, investor-only profile, generic executive, or lead-profile placeholder. Pages should be public, accessible, and usable as evidence; contact aggregators, people-data or org-chart pages, lead-generation pages, RFQ or contact pages, market-report SEO pages, generic ranked lists, and login or app shells are outside the evidence scope. The three facets are distinct evidence roles: generic speaker rosters, team pages, broad person profiles, company/product articles, founder blurbs, and quote-bearing news stories should not be reused across facets unless the cited page independently carries the person-centered role profile, the explicit authority anchor, and the centered public contribution required for the specific facet.

Requirements:
- The page must clearly identify the named person and connect them to the submitted topic area through a beverage-sector context.
- The page must identify the person's public affiliation or context at the page time, such as a company, organization, university, project, event, program, or equivalent setting, enough to disambiguate the person.
- The page should have source-role cues appropriate to the submitted `evidence_facet`: a person-centered profile, biography, staff/faculty/team, speaker, guest, or comparable role surface for `role_profile`; a topic-specific project, program, patent, publication, research, technical, formulation, process, product-development, or expert-context surface that states the person's authority role for `topic_authority`; and a dedicated session, talk, interview, Q&A, podcast episode, bylined article, publication, patent, named project, panel, video, or comparable public-output surface centered on the person's contribution for `public_contribution`.
- The page must contribute a concrete facet-scoped evidence point: public identity plus topic-specific beverage role or affiliation context for `role_profile`; a named topic-specific workstream, responsibility, project, publication, patent, technical role, program, credential, formulation / process / product-development role, authorship, inventorship, leadership, or comparable person-scoped authority for `topic_authority`; and a public-facing contribution centered on the person and the submitted topic for `public_contribution`, with enough detail to show what the contribution was about and what role the person had in it.

Write one JSON object per line to `results_beverage_expert_topic_provenance.jsonl`:
{"item": { "topic_area": "<topic_area>", "person": "<person>", "affiliation": "<affiliation>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
