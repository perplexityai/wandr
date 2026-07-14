You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `ai_capacity_opportunities`
  - `ai_capacity_opportunities.organization_ai_capacity_sources`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `ai_capacity_opportunities`

For each of the 4 route families listed below, cover 20+ mission-driven or public-interest organizations, and for each organization identify 1+ public AI-capacity opportunity or standing participation route; supply a public source (i.e. 1+ URL per route) that supports the route.

The useful work is public provenance, not career matching. Contacts, emails, phone numbers, named recruiters, private outreach routes, fit ranking, application strategy, procurement recommendations, and pay adequacy judgments are not route evidence.

Route families:
- `career_or_contractor_role`: an employee, fixed-term, intern, contractor, or consultant role connected to the organization's AI-capacity work
- `procurement_rfp_eoi_or_individual_consultancy`: a tender, request for proposal, expression of interest, vendor call, or individual-consultancy call for AI-capacity services or deliverables
- `fellowship_paid_program_or_training_call`: a fellowship, stipend-supported programme, paid training call, cohort programme, or comparable time-limited public call
- `standing_roster_pool_or_public_contribution_route`: a standing expert roster, consultant pool, vendor pool, online volunteer route, civic-tech contribution route, or recurring participation pool

Organizations ought to be public-interest or mission-driven bodies such as IGOs, public agencies, nonprofits, charities, think tanks, research institutes, advocacy groups, standards bodies, professional associations, civic-tech or data-for-good communities, public-interest education groups, and comparable organizations. Within one route family, different roles, calls, notices, or programmes from the same organization still belong to the same organization. Generic for-profit AI rater marketplaces, data-labeling gig platforms, staffing portals, salary-estimate pages, ordinary learner-facing courses without an engagement route, grants to organizations, and commercial vendor marketing pages are out of scope. Pages should be public, accessible, and usable; a bare app shell, login screen, search-results page, or contact directory is not enough.

Requirements:
- The page must clearly identify the organization and the named opportunity or standing route.
- The page must tie the route to AI education, AI literacy, AI evaluation, responsible AI, AI governance, digital inclusion, data/AI-for-good, AI capacity-building, or comparable public-interest AI work.
- The page must demonstrate the claimed `route_family`: for `career_or_contractor_role`, a role, contract, internship, employment, or consultancy opening; for `procurement_rfp_eoi_or_individual_consultancy`, a procurement notice, RFP, EOI, tender, vendor call, or individual-consultancy call; for `fellowship_paid_program_or_training_call`, a fellowship, stipend-supported programme, paid training call, cohort, or comparable public call; for `standing_roster_pool_or_public_contribution_route`, a standing roster, pool, public contribution route, online volunteer route, or recurring participation mechanism.
- The page should make its provenance role visible: an official or organization-controlled page, an official multi-agency portal, an organization-branded hosted ATS/programme page, or a labeled secondary page that visibly identifies the opportunity owner and route can work; generic job-search results, salary-estimate pages, SEO listicles, social reposts, and unowned contact directories do not provide enough provenance.
- The page must state that the route is remote, home-based, online, global, multi-country, or otherwise broadly accessible to external participants, vendors, consultants, roster members, or volunteers beyond a single local onsite workplace. Public tender/EOI/vendor/consultant access, standing roster eligibility, and volunteer participation terms can satisfy this when page-stated. A local-only onsite work location, route title, deadline, reference number, duration, budget, salary, stipend, contact block, or application link alone is not enough. Only page-stated access facts count; do not infer remote/global eligibility from a public webpage, online form, or AI-capacity topic.

Write one JSON object per line to `results_ai_capacity_opportunities.jsonl`:
{"item": { "route_family": "<route_family>", "organization": "<organization>", "opportunity_name": "<opportunity_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `ai_capacity_opportunities.organization_ai_capacity_sources`

Cross-tasknode identifier discipline: this task is for the same {= organization =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= organization =}+ mission-driven or public-interest organizations, cover each of the 2 AI-capacity context roles listed below; for each (`organization`, `capacity_evidence_role`) pair, supply an organization-context source (i.e. 1+ URL).

AI-capacity context roles:
- `mission_or_strategy`: an organization-level mission, remit, strategy, profile, initiative overview, or comparable page tying the organization to public-interest AI-capacity work
- `concrete_ai_capacity_work`: a public project, programme, report, standard, curriculum, training, tool, working group, portfolio item, community, or comparable work output showing the organization's AI-capacity activity beyond one opportunity ad

The cited page itself must carry organization-level AI-capacity context. A vacancy, procurement notice, fellowship application page, roster listing, or volunteer listing whose AI content is limited to a single opportunity is not enough; an organization-level programme, initiative, portfolio, report, standard, curriculum, working group, or strategy page can work even when it also points to ways to participate. Generic contact pages, source directories, job-board indexes, lead lists, rankings, applicant guidance, and pages used only for outreach or application mechanics are out of scope.

Requirements:
- The page must clearly identify the organization.
- The page must establish the required `capacity_evidence_role`: for `mission_or_strategy`, an organization-level mission, remit, strategy, profile, initiative overview, or comparable organization-context surface; for `concrete_ai_capacity_work`, a concrete project, programme, report, standard, curriculum, training, tool, working group, portfolio item, community, or comparable work-output surface.
- The page must state role-specific public-interest AI-capacity substance: for `mission_or_strategy`, the organization's AI education, AI literacy, AI evaluation, responsible AI, AI governance, digital inclusion, data/AI-for-good, AI capacity-building, standard-setting, research, or comparable AI-capacity mission/remit/strategy; for `concrete_ai_capacity_work`, a concrete public work item in one of those AI-capacity areas.

Write one JSON object per line to `results_ai_capacity_opportunities.organization_ai_capacity_sources.jsonl`:
{"item": { "organization": "<organization>", "capacity_evidence_role": "<capacity_evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
