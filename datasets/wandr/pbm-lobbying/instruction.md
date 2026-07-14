You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `pbm_lobbying`
  - `pbm_lobbying.seed_actor_probes`

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

## `pbm_lobbying`

For each of the 7 positive-record jurisdictions listed below, provide 6+ filed actors per jurisdiction with official state lobbying registrations, disclosure reports, search-result rows, PDFs, or open-data records that directly tie the actor to PBM, pharmacy-benefit, prescription-drug-pricing, or closely related healthcare issue text during 2021-2026. Each actor should be backed by at least 1 official URL.

For each filed actor, report the best-fitting actor class from the labels below. Aim for a mix of actor classes within each jurisdiction where official records support it; the root task does not require every jurisdiction to produce every class.

The tracker is about what the lobbying record itself says. Legislation trackers, advocacy pages, organizational pages, news, testimony, OpenSecrets, FollowTheMoney, ProPublica Represent, F Minus, OpenLobby, Lobbylinx, Cause IQ, InfluenceWatch, and similar secondary sources can suggest search terms, but they do not count as evidence for this task.

Use only page-local official evidence that visibly appears in the cited page text, PDF text, search-result row, or open-data row. Do not infer a PBM issue from the actor identity, from a search summary, or from a different page. Every excerpt must faithfully support the filed actor, filing context, issue text, and URL submitted.

Positive-record jurisdictions:
- **Colorado**
- **Massachusetts**
- **Montana**
- **New Jersey**
- **New York**
- **South Carolina**
- **Wisconsin**

Actor classes:
- `pbm_or_payer`: PBM, PBM trade association, insurer/PBM affiliate, health plan, payer, plan sponsor, or comparable payer-side actor
- `provider_pharmacy_or_pharma`: pharmacy, pharmacy association, hospital/provider association, drugmaker, pharma/biotech company, or comparable healthcare supply-side actor
- `consumer_labor_or_other`: consumer, patient, labor, employer, public-interest, reform, or other healthcare actor with official PBM/drug-pricing issue text

Only filed names, public registrant/client/principal/lobbyist/firm names, filing periods, filing IDs, bill/subject/activity text, and named firms or lobbyists as filed are in scope. Contact details, addresses, emails, phone numbers, outreach targets, biographies, campaign-finance/PAC/contribution records, lobbying strategy, lobbying-effectiveness analysis, opposition research, healthcare policy advice, and legal or compliance advice are outside the task.

Requirements:
- The page must communicate that it is an official state lobbying/disclosure source for the jurisdiction, such as a state ethics, secretary of state, campaign-finance board, lobbying commission, direct filing PDF, official search-result page, or official bulk/open-data record.
- The page must identify the submitted actor as filed in a lobbying registrant, client, principal, beneficial client, lobbyist, lobbying firm, or comparable public-record role for that jurisdiction and target period.
- The official record text must directly state a PBM, pharmacy-benefit, prescription-drug-pricing, or closely related healthcare issue connection through a subject field, bill field, activity description, bill/position table, lobbying-interest field, or similar official text. The issue connection cannot be inferred from actor identity, a PBM bill tracker, advocacy content, or the existence of PBM legislation in the jurisdiction.
- The page must expose record-specific context such as filing/report period, session, filing ID, bill or position, subject or issue field, activity description, client/principal/lobbyist relationship, or comparable official-record detail.

Write one JSON object per line to `results_pbm_lobbying.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "actor": "<actor>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `pbm_lobbying.seed_actor_probes`

Cross-tasknode identifier discipline: this task is for the same {= jurisdiction =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For each target jurisdiction listed below and each anchor family, provide 2+ searched or as-filed name variants across official state lobbying/disclosure portals for PBM Accountability Project and America's Agenda. Each probe variant should have one of the listed page-local statuses and at least 1 official URL supporting what that official page shows.

The slice preserves positive, stale, negative, and limited official evidence. A status is page-local: the cited official URL must support the reported status without needing a secondary source or a second official comparison page. Secondary sources can motivate a probe but do not satisfy the source bar.

Do not submit generic portal homepages for `no_visible_official_result` unless the visible page text, URL, title, or preserved query state shows the searched name and the no-result/empty-result outcome. A solver-only note that a search was performed, or an excerpt that is not visible on the cited official page, is invalid. For all statuses, every excerpt must be faithful page-local evidence for the submitted name, status, and jurisdiction.

Target jurisdictions:
- **Colorado**
- **Massachusetts**
- **Montana**
- **New Jersey**
- **New York**
- **South Carolina**
- **Wisconsin**

Anchor families:
- `pbm_accountability_project`: PBM Accountability Project, PBM Accountability Project of a state, PBM Accountability, or closely filed state-branded variants
- `americas_agenda`: America's Agenda, America's Agenda: Health Care for All, America's Agenda Healthcare Education Fund, and closely filed variants

Probe statuses:
- `official_record`: cited official page identifies a matching state lobbying/disclosure record in the target period
- `stale_official_record`: cited official page identifies a matching official record outside the target period
- `no_visible_official_result`: cited official search/result page visibly reports no matching result or an empty result set for the submitted name variant
- `portal_limited`: cited official source visibly cannot establish the requested name or issue linkage from available portal content
- `withheld_or_blocked`: cited official source visibly indicates unavailable, withheld, blocked, or inaccessible official records

Optional audit notes may include a checked date and sibling variants tried, but those notes are not a substitute for visible official page evidence. Keep the row to public record inventory only: filed names, public lobbyist or firm names as filed, search terms, periods, record identifiers, source type, and official limitations. Do not add emails, phone numbers, addresses, outreach targets, biographies, campaign-finance/PAC/contribution records, strategy, policy advice, or legal/compliance advice.

Requirements:
- The page must communicate that it is an official state lobbying/disclosure portal, official search-result page, direct official filing/PDF, or official open-data/bulk source for the jurisdiction.
- For `official_record` and `stale_official_record`, the page must show the submitted `probe_name` as an official filed name or variant. For `no_visible_official_result`, the page, title, or URL must preserve the submitted searched name/query. For `portal_limited` and `withheld_or_blocked`, the page must support the official limitation or block; it need not preserve a query when the official source itself cannot expose one.
- The page must support the claimed `probe_status`: a target-period official record, an older stale official record, a visible no-result or empty official result set, a portal limitation, or a withheld/blocked official-record condition.
- For `no_visible_official_result`, `portal_limited`, and `withheld_or_blocked`, the official page, URL, title, or excerpts must provide judgeable audit evidence of the searched query/result state or the official limitation/block. A solver-only note that a search was performed is not enough.
- For `official_record` and `stale_official_record` rows that claim PBM issue linkage, the issue or bill connection must come from official record text. For negative or limited statuses, the page must support the limitation or absence outcome rather than a positive lobbying claim.

Write one JSON object per line to `results_pbm_lobbying.seed_actor_probes.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "anchor_family": "<anchor_family>", "probe_name": "<probe_name>", "probe_status": "<probe_status>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
