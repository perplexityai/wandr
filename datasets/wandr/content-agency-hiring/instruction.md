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

## `content_agency_hiring`

For 20+ agencies, cover each of the 6 hiring-intelligence facets listed below by supplying a source (i.e. 1+ URL under each facet) that supports a current application-ready profile for a recognized media, content-marketing, performance-media, creative, or digital agency hiring in both project-management and client-success / client-services role families. Each agency must be a real client-service agency of this kind, not an in-house brand team, pure staffing firm, software vendor, job board, or general consulting firm with only incidental marketing services.

The aim is an employer target map for agency-side project-management and client-success applications, with enough context to screen fit before applying.

Hiring-intelligence facets:
- `project_manager_opening`: a current open role in project management, production management, delivery management, program management, campaign operations, or a closely similar agency-delivery role.
- `client_success_opening`: a current open role in client success, account management, client services, customer success, client strategy, relationship management, or a closely similar client-portfolio role.
- `company_size`: a source giving the agency's approximate current scale, such as employee count, headcount range, office/team size, or global network size.
- `content_specialization`: a source describing the agency's core media/content specializations, such as SEO, editorial content, paid media, video, social, influencer, B2B, ecommerce/D2C, lifecycle, analytics, creative, or integrated campaigns.
- `market_standing`: a source showing recognized market presence, such as an agency ranking, award/shortlist, directory profile, named client roster, substantive case-study portfolio, or industry-list treatment.
- `careers_channel`: the agency's official careers page, jobs board, applicant-tracking-system board, recruiting contact page, or other official application channel.

Agency-owned pages, official applicant-tracking-system postings, recognized employer/company profiles, industry rankings, award pages, case-study portfolios, and professional profile surfaces can qualify when they visibly earn the selected facet. Pay ranges and named recruiting or hiring-manager contacts are useful answer data when the qualifying page exposes them, but a posting or careers page without those optional fields can still qualify.

Requirements:
- The page must clearly identify the named agency.
- The page itself must be a source surface that earns the selected `hiring_facet`, not an aggregator stub, scraped repost, or listicle that merely points elsewhere. For the two opening facets it should read as an official posting, careers listing, or recruiting channel for the agency; for the remaining facets it should be the agency's own profile, capability, recognition, or application surface as that facet describes.
- The page must expose a concrete finding scoped to the named agency and the selected `hiring_facet`. For the two opening facets this means a specific named role title; for the remaining facets it means the tangible signal that facet calls for, not a generic claim or self-promotional tagline.
- For `project_manager_opening` and `client_success_opening`, the page must show that the role is currently open or accepting applications. Archived, closed, filled, expired, or "no longer accepting applications" postings do NOT count.

Write one JSON object per line to `results_content_agency_hiring.jsonl`:
{"item": { "agency": "<agency>", "hiring_facet": "<hiring_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
