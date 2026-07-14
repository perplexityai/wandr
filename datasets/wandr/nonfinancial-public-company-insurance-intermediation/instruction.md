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

## `nonfinancial_public_company_insurance_intermediation`

For 50+ publicly listed operating companies whose parent business is outside traditional financial services as of 2026-06-29, cover both of the 2 source families below for each company and supply 1+ public authoritative URL under each family that states the company's customer-facing third-party insurance intermediation.

Source families:
- `company_or_filing_source`: a company-controlled, controlled-unit, investor-relations, annual-report, securities-filing, exchange-disclosure, or comparable authoritative company/disclosure source.
- `regulator_or_license_source`: a public regulator, license, producer/agency/broker register, insurance-department record, statutory register, or comparable public official register/source for the insurance intermediary activity.

For the same public company, the two source-family URLs must be distinct. A company marketing page cannot satisfy `regulator_or_license_source`, and a regulator/register page cannot satisfy `company_or_filing_source`.

The cited page should make its authority visible: it is controlled by or authoritative for the listed company, the relevant unit or intermediary, a filing or disclosure channel, a public register, or a comparable source with company-specific authority. Generic insurance-shopping pages, ads, unaffiliated snippets, and thin affinity/referral pages with no authoritative company-specific disclosure do not work.

The listed parent companies ought to be nonfinancial operating businesses such as retail, payroll/HCM, homebuilding, auto retail, e-commerce, telecom, travel, manufacturing, software, or similar sectors. Insurers, reinsurers, banks, broker-dealers, asset managers, and financial holding companies do not count as the parent company.

Useful source-stated context can include intermediary or unit name, ecosystem served, commission/fee/referral language, filing form or report type, fiscal year, filing date, accession/document ID, regulator or exchange, passage locator, or a compact note about missing/conflicting details. Preserve these only when the source states them.

Requirements:
- The page must satisfy the selected source family and be authoritative for that source role.
- The page must connect the submitted public company, or a controlled/named subsidiary, unit, or brand clearly connected to it, to the insurance activity.
- The page must state a genuine customer-facing third-party insurance intermediation role: brokerage, agency, producer, distribution, facilitating sale or access, commission/fee/referral compensation, or equivalent jurisdictional wording.

Write one JSON object per line to `results_nonfinancial_public_company_insurance_intermediation.jsonl`:
{"item": { "name": "<name>", "ticker": "<ticker>", "exchange": "<exchange>", "jurisdiction": "<jurisdiction>", "source_family": "<source_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
