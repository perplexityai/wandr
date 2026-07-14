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

## `job_board_api_access`

For each of the 7 capability families listed below, cover 24+ hiring-ecosystem platforms per family and supply an official source for the platform/capability claim (1+ URL per platform/capability pair).

The useful work is public provenance: a broad table of platform-owned or platform-authorized sources showing what job-board, ATS/recruiting-platform, staffing CRM, employment-marketplace, job-distribution, or relevant cloud/job API capability is publicly documented. Record source-stated access posture, credential or partner requirement, current/deprecated/conflict status, market or geography limit, source date/version, checked date, and pricing or fee presence when the source states those facts. Do not infer absence from silence.

Capability families:
- `job_posting_create_or_publish`: creating, publishing, posting, or submitting a job advertisement or job posting.
- `job_posting_update_or_upsert`: updating, editing, replacing, or upserting an existing job posting.
- `job_posting_close_delete_or_expire`: closing, deleting, expiring, cancelling, or otherwise removing an active job posting.
- `job_or_posting_status_retrieve_or_list`: retrieving posting status, reading a job/posting record, or listing job postings.
- `applicant_or_candidate_feed_or_apply`: receiving applications, candidate feeds, apply payloads, candidate ingestion, or apply flows.
- `webhook_or_event_delivery`: webhooks, event subscriptions, callbacks, or event-delivery APIs for recruiting/job workflow events.
- `account_tenant_hirer_or_company_management`: API-visible account, tenant, company, hirer, employer, brand, or organization management.

Acceptable evidence includes official developer documentation, API references, partner-program pages, official help-center pages, platform-owned GitHub or documentation repositories, official marketplace pages only when they directly state the capability, official pricing pages only when they directly state source-relevant pricing or fee facts, and reputable platform announcements for currentness, deprecation, withdrawal, or access-status evidence.

Third-party aggregators, unified-API matrices, scraper API marketplaces, generic "top APIs" lists, pricing blogs, platform-ranking or procurement pages, and implementation how-to articles do not establish the platform's own capability. A generic docs homepage should not stand in for many capability records unless the page itself directly documents each claimed capability. A read/listing API page does not establish create, update, close, webhook, apply, or account-management capability unless the relevant operation is directly stated.

Keep the submission to public source facts. Do not include app build advice, implementation code, credential acquisition or use instructions, account setup steps, scraping or bypass guidance, posting automation instructions, rankings, procurement recommendations, applicant-management advice, recruiter contact discovery, outreach, or contact enrichment.

Requirements:
- The page must communicate that it is a platform-owned, platform-controlled, or platform-authorized official surface for the claimed platform.
- The page must directly document the claimed capability family for the claimed platform, with enough operation-level specificity to distinguish posting create/publish, update/upsert, close/delete/expire, status/read/list, applicant/apply/candidate ingestion, webhook/event delivery, and account/tenant/company management.
- Access posture, credential or partner requirements, currentness/deprecation/conflict status, pricing or fee facts, source date/version, and market/geography limits must be reported only when they are stated or clearly signaled by the official source; otherwise mark the fact as unstated or no-source rather than guessing. The checked date is the date the source was inspected, not a fact the source needs to state.

Write one JSON object per line to `results_job_board_api_access.jsonl`:
{"item": { "capability_family": "<capability_family>", "platform": "<platform>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
