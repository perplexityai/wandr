You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `bergen_county_nonprofit_landscape`
  - `bergen_county_nonprofit_landscape.diligence_evidence`

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

## `bergen_county_nonprofit_landscape`

For each of the 6 Bergen County nonprofit focus areas below, name 12+ operating nonprofit profiles per focus area, supplying a supporting page (1+ URL per profile).

This is a grantmaking and local-ecosystem landscape: a useful profile names an operating organization, shows a real Bergen County service or place binding, and pins why that organization belongs in the selected focus area. It is not a complete census of every 501(c)(3) in Bergen County, and registry-only evidence is not enough for the profile page.

Focus areas:
- **human_services_food_housing** -- food security, emergency assistance, housing stability, homelessness prevention, anti-poverty, legal / immigration help, or similar direct human services.
- **health_clinical_support** -- free or low-cost healthcare, mental health, disease-specific support, disability health services, recovery support, or public-health access.
- **youth_family_education** -- childcare, after-school, youth development, family support, literacy, mentoring, or education programs outside ordinary public-school administration.
- **senior_disability_services** -- older-adult services, aging-in-place support, disability services, caregiver support, residential support, or adult day programming.
- **arts_culture_civic** -- performing arts, museums, history, libraries, civic leadership, volunteerism, community media, or cultural access.
- **environment_animals** -- conservation, environmental education, open-space stewardship, animal welfare, rescue, adoption, or wildlife protection.

Private foundations, donor-advised funds, government agencies, public schools, for-profit providers, national organizations with no Bergen-specific chapter or program evidence, and pages that merely show a Bergen mailing address do not count as operating Bergen nonprofit profiles.

Requirements:
- The page must be materially about the named organization, its public programs, charity profile, local resource listing, funder relationship, public reporting, or substantive nonprofit activity.
- The page must identify the named organization as a nonprofit, charitable, tax-exempt, 501(c)(3), not-for-profit, public-benefit, community-action, or comparable operating organization.
- The page must tie the named organization to Bergen County, New Jersey, or to a Bergen County municipality through service area, program site, public resource listing, headquarters plus operating context, grant or service activity, or local community role.
- The page must support public programs, services, facilities, activities, or community functions that belong to the submitted focus area.

Write one JSON object per line to `results_bergen_county_nonprofit_landscape.jsonl`:
{"item": { "focus_area": "<focus_area>", "organization": "<organization>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `bergen_county_nonprofit_landscape.diligence_evidence`

Cross-tasknode identifier discipline: this task is for the same {= focus_org =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= focus_org =}+ Bergen County nonprofit profiles, cover 2+ public due-diligence evidence axes below — supplying a source (1+ URL per (organization, axis) finding).

The evidence axes are sparse by design: each organization does not need every axis, but a strong landscape should mix public registry, financial, funder, recent-activity, and accountability evidence rather than relying on one source family.

Evidence axes:
- **exemption_identity** -- public evidence that the organization is a tax-exempt charitable nonprofit, public charity, registered 501(c)(3), or comparable operating nonprofit.
- **budget_or_staff_scale** -- public revenue, expense, assets, staff, wage, budget, or scale evidence from a Form 990, annual report, audit, official impact report, or nonprofit data profile.
- **funding_or_grant_signal** -- public evidence of funding sources, government grants, foundation support, major donors, sponsorships, awarded grants, contracts, or direct public funding.
- **recent_activity_2024_2026** -- public 2024, 2025, or 2026 activity evidence such as an impact report, event, program update, grant cycle, annual report, news item, or public calendar.
- **governance_or_accountability** -- public accountability evidence such as board / leadership, audited financials, BBB / Charity Navigator / GuideStar profile, annual report, or published policies.

Each cited page should be final public evidence for the selected organization-axis finding. Avoid private-contact scraping and do not use Candid / GuideStar / other nonprofit-profile pages when the needed metric is hidden behind sign-in or paywall.

Requirements:
- The page must be final public evidence for the selected due-diligence axis, not merely a search result, generic directory shell, private-contact page, AI summary, paywalled-only nonprofit profile, or discovery lead.
- The page must tie the selected evidence to the same named organization as the Bergen nonprofit profile, without swapping in a national parent, unrelated affiliate, fiscal sponsor, or homonym.
- The page must support the selected evidence axis defined above, not a different axis or a weaker adjacent fact.

Write one JSON object per line to `results_bergen_county_nonprofit_landscape.diligence_evidence.jsonl`:
{"item": { "focus_area": "<focus_area>", "organization": "<organization>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
