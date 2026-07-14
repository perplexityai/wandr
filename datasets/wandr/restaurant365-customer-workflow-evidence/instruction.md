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

## `restaurant365_customer_workflow_evidence`

For at least 55+ restaurant, hospitality, franchise, accounting, back-office, workforce, payroll, inventory, or operations customer operators publicly evidenced as Restaurant365/R365 customers, supply at least 2+ named workflow-evidence records per operator, with at least 1+ customer-specific source URL for each record.

The measured record is a public-provenance workflow/use-case record for a named Restaurant365/R365 customer/operator, not a loose source-table row. Use the named franchisee, operating group, hospitality group, parent operator, or customer organization as the customer/operator identity when the source supplies one; a brand name by itself works only when the source itself treats that brand entity as the customer.

For each workflow-evidence record, report the source-stated workflow/module/use-case wording, a normalized workflow bucket, source class, source role, source date or `no_date`, cutoff status, and checked date. The workflow wording/bucket plus source class/role/date/cutoff labels are part of the evidence bar. Brand/franchise context, service-partner context, segment/location, checked date, confidence, and missing/conflict flags are auxiliary provenance context; they do not replace the relationship, workflow, or source/date requirements.

Suggested normalized workflow buckets: accounting, inventory, workforce_labor_scheduling, payroll_hr_training, operations_task_management, reporting_analytics, ap_lease_accounting_stack, multi_location_franchise_rollout, purchasing_vendor_management, other_source_stated_workflow.

Sources may include Restaurant365 case studies or customer pages, Restaurant365 official news or press pages, newswire copies of official releases, customer-owned pages, partner or service-provider co-marketing stories, public webinar/video pages, public conference/session pages, trade editorial, sponsored trade content, or similar public sources. Broad customer lists, logo walls, category hubs, sitemaps, generic integration/support/partner pages, and aggregator/customer-database pages are discovery aids, not full evidence, unless the cited page section itself gives customer-specific Restaurant365 relationship and workflow proof.

Do not use sources dated after May 5, 2026 as in-scope evidence. An undated page can be used only with `no_date` and a cutoff status indicating undated current public provenance; it is a provenance caveat, not hidden proof that the page existed before May 5, 2026.

Keep this as public vendor-customer provenance. Do not include contacts, emails, phone numbers, outreach hooks, lead scoring, buyer intent, account priority, revenue inference, rankings, recommendations, procurement advice, or enrichment fields.

Requirements:
- The page must identify Restaurant365 or R365, a specific customer/operator organization, and a customer relationship such as selection, use, rollout, implementation, customer story, award, testimonial, public session, or co-marketed implementation.
- The page must state the submitted workflow-evidence record as a concrete Restaurant365 module, workflow, use case, implementation area, or operational/accounting stack role for that customer.
- The page must expose enough source-role and timing context to label the source class, source role, source date/no-date status, and cutoff status honestly.

Write one JSON object per line to `results_restaurant365_customer_workflow_evidence.jsonl`:
{"item": { "customer_operator": "<customer_operator>", "workflow_evidence_record": "<workflow_evidence_record>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
