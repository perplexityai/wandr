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

## `ai_mlops_vendor_claims`

For 50+ organizations that publicly offer AI/MLOps platforms, agentic-orchestration products, AI governance or MLOps tooling, or AI implementation/delivery services, name discrete vendor claims (at least 1+ per claim family) in each of the 3 claim families below and cover each of the 2 evidence sides for every claim with 1+ URL per side.

Most AI vendors can supply their own product pages, trust pages, and customer stories. The useful work is finding where the same specific claim is or is not corroborated by a non-vendor owner.

Claim families:
- `ai_mlops_or_agentic_capability`: a named AI/MLOps, LLMOps, model/data platform, eval/monitoring, agent orchestration, AI governance tooling, or AI implementation delivery capability
- `security_compliance_or_ai_governance`: a named security certification, compliance framework or status, trust-control posture, AI governance framework, model-risk control, or comparable governance claim
- `regulated_finance_customer_or_case`: a concrete regulated financial-services customer, case, deployment, pilot, implementation, or customer-context claim involving AI/MLOps, agentic AI, data/ML operations, or AI governance work

Evidence sides:
- `self_asserted`: vendor-controlled evidence: official product or docs pages, trust or compliance pages, vendor-owned customer stories, vendor blogs, vendor press releases, or vendor-controlled marketplace text
- `independent`: non-vendor-controlled corroboration: customer or counterparty pages, certification-body or registry pages, regulator or institution pages, hyperscaler-owned marketplace or docs pages, company registries for legal-entity facts, or reputable secondary reporting that independently reports the specific claim

The work is factual public-evidence research, not an RFI, shortlist, vendor ranking, procurement recommendation, implementation advice, regulatory/legal advice, pricing analysis, lead scoring, outreach, or contact enrichment.

A valid `claim` is a discrete, checkable factual assertion tied to the vendor and the claim family. It must name the fact being corroborated; it cannot be a broad family umbrella that leaves the reader or judge to choose a narrower fact from the page. Invalid umbrella claims include:
- "`<vendor>` publicly offers an AI, MLOps, model, data, automation, or agentic platform/service capability."
- "`<vendor>` publicly presents security, compliance, responsible-AI, AI-governance, or model-risk controls for its AI-related offerings."
- "`<vendor>` is tied in public evidence to a regulated financial-services customer, banking/insurance deployment, or financial-services AI/ML/automation use case."

Family-specific claim requirements:
- `ai_mlops_or_agentic_capability`: name a concrete product, service, platform, feature, or delivery capability plus a checkable function, such as deployment, monitoring, orchestration, evaluation, governance workflow, implementation service, or integration.
- `security_compliance_or_ai_governance`: name a concrete certification, framework, control, trust posture, AI-governance mechanism, model-risk control, registry/listing/status, or similar specific posture.
- `regulated_finance_customer_or_case`: name a concrete customer, counterparty, case, pilot, deployment, or sufficiently specific anonymized regulated-finance case.

Vague adjectives such as "enterprise-grade", "trusted", "AI-ready", "built for banks", or "compliant by design" do not count unless the claim itself states a checkable fact.

Requirements:
- The page must clearly identify the vendor named.
- The page must fit the claim family in scope: concrete AI/MLOps or agentic capability; named security/compliance or AI-governance posture; or concrete regulated-finance customer/case context.
- The page must state or independently corroborate the same specific claim, not merely mention the vendor and the broad topic.

Write one JSON object per line to `results_ai_mlops_vendor_claims.jsonl`:
{"item": { "vendor": "<vendor>", "claim_family": "<claim_family>", "claim": "<claim>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
