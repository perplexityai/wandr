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

## `helmet_procurement_records`

For 8+ jurisdictions from the allowed set below, name 16+ distinct public procurement records per jurisdiction and supply 1+ URL for each record. A record counts when the cited source states a publication, closing, award, contract, update, status, creation, or other procurement-lifecycle date from 2023-01-01 through 2026-06-30, and helmets are actual procured goods or line items.

Allowed jurisdictions:
- **Australia** (also written as: Commonwealth of Australia, AU)
- **Brunei** (also written as: Brunei Darussalam)
- **Cambodia** (also written as: Kingdom of Cambodia)
- **China** (also written as: People's Republic of China, PRC, mainland China)
- **India** (also written as: Republic of India, Bharat)
- **Indonesia** (also written as: Republic of Indonesia)
- **Laos** (also written as: Lao PDR, Lao People's Democratic Republic, Lao)
- **Malaysia**
- **Myanmar** (also written as: Burma)
- **Philippines** (also written as: Republic of the Philippines, the Philippines)
- **Singapore** (also written as: Republic of Singapore)
- **Thailand** (also written as: Kingdom of Thailand)
- **United States** (also written as: United States of America, USA, U.S., US)
- **Vietnam** (also written as: Viet Nam, Socialist Republic of Vietnam)

Valid evidence comes from official procurement portals, tender/RFQ/bid notices, award or contract notices, buyer procurement pages, gazettes, official tender or bid PDFs, and multilateral procurement notices when the beneficiary or delivery jurisdiction is source-stated and in the allowed set. Subnational buyers count under the source-stated country jurisdiction.

Commercial tender aggregators, paywalled teaser listings, market reports, shopping or retail pages, supplier or manufacturer marketing pages, lead-generation pages, contact databases, generic standards pages not tied to a procurement record, and login-only attachments do not count as final evidence. Pages where "helmet" appears only as bidder PPE, site-visit gear, worker safety instructions, or attendance requirements do not count. Service-only maintenance or repair records do not count unless the source also states purchase or delivery of helmet goods.

Source-stated status, quantity, value, budget, category, certification, specification, supplier, or awardee details can be reported when visible. If the cited page does not state one of those details, the row may only mark that the cited source does not state it; do not infer missing values or assert global absence. Standards and specifications should be recorded only as tender requirements stated by the source, without judging whether a helmet, supplier, standard, or tender requirement is safe, adequate, compliant, advisable, or strategically attractive.

This is neutral public-record provenance. Police, tactical, ballistic, rescue, or other public-safety records can count only as procurement records; do not provide supplier ranking, purchase recommendations, bid strategy, outreach leads, contact enrichment, tactical assessment, threat modeling, export-control advice, or defense/security implications.

Requirements:
- The page must communicate official public procurement, buyer, gazette, award/contract, tender-document, or multilateral procurement authority.
- The page must identify the buyer or issuing authority and the tender, notice, solicitation, RFQ, bid, award, contract title, or record reference.
- The page must show helmets, hard hats, protective helmets, tactical/police/rescue/fire/motorcycle/bicycle/industrial helmets, or another source-stated helmet type as an actual procured good or line item.
- The page must source-state at least one relevant publication, closing, award, contract, update, status, creation, or procurement-lifecycle date within 2023-01-01 through 2026-06-30.
- Every reported status, quantity, value, budget, helmet category, certification, specification text, awardee, supplier, or source-scoped missing annotation must be directly grounded in the cited page rather than inferred.

Write one JSON object per line to `results_helmet_procurement_records.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "buyer": "<buyer>", "notice_id_or_title": "<notice_id_or_title>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
