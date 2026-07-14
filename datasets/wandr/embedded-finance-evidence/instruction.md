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

## `embedded_finance_evidence`

For 300+ public companies, startups, or scaleups whose public materials show embedded-finance or adjacent-fintech capabilities, supply at least 2 URLs per company, each on a page that identifies the company, establishes the relevant financial product or capability, and contributes source-stated evidence for a checked-date public evidence atlas.

The atlas is public provenance reconstruction, not a ranking or enrichment list. Companies can play roles such as provider, embedded product operator, vertical SaaS with financial feature, implementation / customer, infrastructure / API company, bank or regulated-delivery counterparty. Product surfaces can include accounts / wallets, cards / issuing, money movement, payments, treasury, lending / credit, payroll, insurance, brokerage / investing, open banking, vertical-SaaS finance, banking infrastructure, compliance / disclosure, and adjacent surfaces. Submit source class and source date when visible or claimed so source provenance can be judged. Checked date, submitted confidence, and cautious missing / conflict flags are auxiliary dataset metadata; include them when useful, but they are not independent substitutes for page-stated atlas facts. Do not fill company facts from memory or infer hidden providers, bank partners, customers, funding, geography, or regulatory status.

Do not collect people/contact data, LinkedIn or other social-graph relationships, lead scores, outreach targets, investment or acquisition recommendations, Top-25-style rankings, or SEO-list extractions.

Company names ought to be real operating companies or organizations, not products, people, investors, regulators, banks named only as counterparties, or generic product categories.

Requirements:
- The page must clearly identify the named company as the subject, publisher, official profile subject, or company being described.
- The page must establish that the company offers, enables, embeds, implements, or materially depends on a financial capability in another business workflow or platform experience.
- The page must contribute at least one concrete source-stated atlas fact claimed for the company, such as product category, product surface, implementation / provider role, customer, partner, bank / issuer / processor, regulator / disclosure, funding, investor, launch, traction, geography, founding date, acquisition, and source-stated absence / conflict state. Facts must be stated by the source or directly evidenced on the page; a missing / conflict flag can count as this atlas fact only when the cited page directly states the absence or conflict.
- The page must make its public source role and provenance visible enough to classify the citation, including authorship / publisher / company-control signals and source date when a source date is claimed.

Write one JSON object per line to `results_embedded_finance_evidence.jsonl`:
{"item": { "company": "<company>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
