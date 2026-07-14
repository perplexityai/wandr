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

## `onboarding_gamification`

For each of the 7 product areas below, cover 20+ products. For each product, cover 2+ distinct evidence facets from the closed facet list below; under each selected facet, supply 1+ product-specific evidence item and 1+ URL that substantiates an observable gamified onboarding, activation, product-learning, proficiency, or agent/admin-configuration mechanic.

Product areas:
- `saas_productivity`: collaboration, productivity, project/work management, docs, communication, or workspace SaaS with public onboarding/proficiency feedback mechanics.
- `crm_support`: CRM, customer-support, helpdesk, success, or service operations products with public agent/admin/customer onboarding feedback mechanics.
- `marketing_sales`: marketing automation, sales engagement, analytics, ecommerce enablement, or growth SaaS with public setup/proficiency feedback mechanics.
- `developer_api_docs`: developer platforms, APIs, SDKs, docs products, DevRel portals, or technical setup tools with public activation/proficiency feedback mechanics.
- `infra_data`: cloud infrastructure, data, observability, security, payments, or admin platforms with public setup/readiness/proficiency feedback mechanics.
- `learning_certification`: product-learning academies, certification programs, interactive training, or enablement paths with public progress, credential, or reward mechanics.
- `ai_agent_support_automation`: AI-agent builders, chatbot builders, customer-support automation, workflow agents, or AI assistant setup products with public builder/proficiency feedback mechanics.

Evidence facets:
- `first_run_ui_or_progress`: first-run, onboarding, setup, activation, or proficiency UI that visibly tracks checklist state, guided-tour progress, completion, readiness/health, warnings, draft-to-live state, or comparable user-visible progress.
- `reward_score_or_badge`: points, optimization/readiness score, rank, badge, certificate, credential, level, streak, achievement, leaderboard, trophy, XP, loot, or comparable reward/status marker tied to onboarding or product proficiency.
- `interactive_milestone_or_gate`: interactive mission, quest, quiz, tutorial, sandbox, agent/admin builder, publish/go-live gate, unlock/completion state, or milestone sequence with visible user feedback.
- `public_capture_or_teardown`: public screenshot, video, teardown, flow library, official launch/demo, or other public capture that visibly or textually documents a gamified onboarding/proficiency mechanic and preserves source directness/provenance.

An evidence item can be a visible checklist/progress path, score/readiness meter, milestone gate, guided tour with completion state, points/badges/levels/streaks/leaderboard, credential or certificate reward, quiz or training result, agent-builder launch/publish milestone with visible feedback, public screenshot/flow/video capture, or reputable teardown that shows the mechanic. Preserve what the public evidence actually shows rather than forcing every product into the same pattern set.

Do not submit a generic setup route, help-center setup article, academy catalog page, product docs page, or marketing page unless it visibly supports the submitted gamified feedback mechanic/state and the relevant onboarding/proficiency context. Rows that only claim no visible gamification, no public onboarding, no AI-agent configuration, gated/pro-library access, stale/screenshot-only provenance, or other source-local absence/provenance states are out of scope as positive evidence.

For each row, make the observed mechanic and provenance explicit: the onboarding, activation, product-learning, proficiency, or configuration context; the declared evidence facet; the user-visible feedback mechanic; source type and directness; visible UI/screenshot/video availability; source date or staleness when relevant; and whether access is gated, third-party-only, screenshot-based, or historical.

Eligible rows must use public sources with concrete product-specific evidence of the observable mechanic. Official docs/help centers/blogs, public demos or marketing pages with visible UI, public videos/transcripts, public screenshot or flow libraries, and reputable teardowns can all work when they contain concrete product evidence of the submitted mechanic. Generic onboarding advice, private or login-only scraped flows, unrelated listings, unavailable gated stubs, and pages whose usable content is only broad pattern taxonomy are out of scope.

Keep rows factual: no UX strategy advice, implementation guidance, dark-pattern recommendation, product recommendation, competitive ranking, or unsourced conversion/uplift claim.

Requirements:
- The page must tie the evidence item to the named product rather than only to a generic onboarding pattern.
- The page must fit the declared `evidence_facet`; a URL that only supports a different facet, a generic setup route, or a source-local missing/provenance state does not satisfy the declared facet.
- The page must connect the evidence item to onboarding, activation, setup, first-run use, product learning, certification, agent/admin configuration, support automation configuration, or a comparable user-start/proficiency milestone.
- The page must support an observed user-visible gamified feedback mechanic: progress/checklist/completion state, score, reward, badge, certificate, rank, level, streak, leaderboard, quest, quiz result, guided-tour state, milestone gate, publish/go-live gate, unlock, readiness/health feedback, public screenshot/video/teardown of such a state, or a comparable feedback loop. A page that merely documents setup steps, education content, or configuration without such a visible mechanic fails.
- The source evidence must support the claimed source type, directness, and availability/provenance state, such as official vs. third-party, visible UI/screenshot/video/docs/blog/teardown, dated or stale when relevant, gated or screenshot-only when relevant, and the limits of third-party or historical evidence.

Write one JSON object per line to `results_onboarding_gamification.jsonl`:
{"item": { "category": "<category>", "product": "<product>", "evidence_facet": "<evidence_facet>", "evidence_item": "<evidence_item>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
