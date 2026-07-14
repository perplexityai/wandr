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

## `automotive_ai_sales_workflows`

For each of the 5 broad automotive/dealer workflow groups below, name 30+ public software or service vendors per workflow that offer that workflow for dealerships, dealer groups, automotive retail, OEM retail, service/fixed ops, or dealer marketing, and supply at least 1 source for each of the 2 evidence roles per vendor/workflow pair.

Workflow groups:
- `chat_messaging_or_voice_ai`: website chat, SMS/messaging, conversational AI, phone/voice AI, virtual assistants, or inbox automation for dealership customers
- `dealer_marketing_cdp_or_reputation`: dealer marketing automation, CDP/audience activation, reputation/reviews, social advertising, inventory merchandising, or customer data workflows
- `digital_retailing_finance_or_desking`: online retailing, vehicle purchase flows, trade/credit/finance, payment, F&I, desking, or showroom-to-online retail workflows
- `sales_bdc_or_lead_followup`: AI sales agents, BDC automation, lead response, lead nurturing, reactivation, equity mining, appointment setting, or CRM follow-up for vehicle sales
- `service_scheduling_or_fixed_ops`: service appointment scheduling, service drive messaging, fixed-ops outreach, repair-order/customer follow-up, or service-lane AI

Evidence roles:
- `official_workflow_feature`: a vendor-owned product, solution, launch, documentation, or official-channel page showing that the vendor offers the claimed workflow for automotive retail, dealerships, dealer groups, OEM retail, or fixed ops. A reputable automotive trade launch can work when it clearly reports the vendor's own launch and a vendor-owned page is unavailable.
- `adoption_or_outcome_evidence`: a public source showing concrete real-world automotive use for the same vendor/workflow pair, such as a named dealer, dealer group, OEM program, certified or approved program, workflow-specific integration page, case study, customer story, or source-stated customer outcome/result. Broad market-presence counts, acquisition articles, funding announcements, vendor directories, and generic trade mentions do not satisfy this role unless the same page ties a named dealer/OEM/program/integration/customer to the submitted workflow.

Requirements:
- The vendor must be a real public software or service provider. Dealers, OEM customers, article publishers, directories, review sites, generic source domains, and product features are not vendor identities.
- The page must clearly identify the submitted vendor or a reasonable alias, sub-brand, acquired brand, or parent-branded form of the same vendor offering.
- The page must tie that vendor to the submitted workflow in an automotive retail, dealership, dealer-group, OEM retail, dealer sales/service, dealer marketing, or fixed-ops context. Generic B2B chat, CRM, sales-engagement, messaging, reputation, or review tools count only when the cited page itself establishes the automotive/dealer workflow relevance.
- The page must visibly earn the selected evidence role. Directories, marketplaces, review pages, and communities are useful discovery or secondary context, but they should not be the backbone for official capability proof.
- The page must expose a concrete workflow-scoped finding: a specific capability, workflow product, named customer/program/integration, case-study detail, source-stated result, or comparable public evidence. Broad adoption counts, acquisition rollups, bare logo grids, vague "AI platform for dealers" boilerplate, public-pricing availability, missingness states, feature rankings, and subjective competitor comparisons do not satisfy the row.
- Outcome or result wording must stay source-stated. Do not turn a vendor page into business-impact validation, vendor ranking, weakness scoring, recommendation, sales strategy, private database enrichment, outreach, or contact enrichment.

Write one JSON object per line to `results_automotive_ai_sales_workflows.jsonl`:
{"item": { "workflow": "<workflow>", "vendor": "<vendor>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
