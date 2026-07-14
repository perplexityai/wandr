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

## `us_msp_mssp`

For each of the 7 customer sectors below, supply named customer-deployment evidence for 15+ companies operating in or selling into the US market as managed IT, managed security, MSSP, MDR, SOC, or adjacent outsourced IT/security operations providers. For each company-sector pair, include 1+ named customer deployment with 1+ URL per deployment. The target is a defensible MSP/MSSP prospect set grounded in real customer work, not a scraped contact list or ranking table.

Customer sectors are broad task-local buckets:
- `healthcare`: healthcare, life sciences, medical, or pharmaceutical organizations
- `financial_services`: banking, insurance, fintech, investment, credit, or private-equity organizations
- `government_education`: government, public-sector, K-12, higher-education, or SLED organizations
- `manufacturing_industrial`: manufacturing, industrial, construction, energy, utility, food-supply, automotive, or logistics organizations
- `legal_professional`: law, accounting, consulting, or other professional-services organizations
- `retail_hospitality`: retail, consumer, hospitality, restaurant, real-estate, sports, or entertainment organizations
- `technology_software`: software, SaaS, cloud, data, internet, or technology organizations

US-market scope applies to the provider company, not to the submitted customer's headquarters. A customer deployment can involve a US, North American, global, or non-US customer when the provider itself has a public US-market footprint and the cited page otherwise proves the provider-customer deployment and sector fit. Providers whose public footprint is only outside the US market do not work.

Sources must be public, readable, and specific to the submitted provider-customer relationship. Customer stories, case studies, deployment writeups, substantive testimonials, customer-owned pages, and independent articles can work when they carry a named-customer deployment passage. Generic provider service pages, logo-only walls, bare customer lists, rankings, award lists, partner directories, search results, anonymous reviews, and scraped contact pages do not work by themselves.

Requirements:
- The page must clearly identify the submitted provider and its service-provider role.
- The page must clearly identify the submitted customer and show that the customer fits the claimed sector.
- The page must show that the provider delivered ongoing managed IT, managed security, MDR, MSSP, SOC, or comparable outsourced IT/security operations to that customer.

Write one JSON object per line to `results_us_msp_mssp.jsonl`:
{"item": { "sector": "<sector>", "company": "<company>", "customer": "<customer>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
