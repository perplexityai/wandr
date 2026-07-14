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

## `upc_offering_mechanics`

For 50+ post-IPO registered offering or prospectus events by companies that used an Up-C IPO structure, cover each of the 5 evidence facets listed below for each event with 1+ official filing URL per facet.

Each offering event is identified by `company`, `event_date`, and `filing_accession_or_file_id`. Use `event_date` for the SEC/EDGAR filing date of the later registered-event document or event chain, not the IPO date, prospectus cover date, effectiveness date, pricing date, delivery date, or closing date. A final prospectus, prospectus supplement, or 424B page can show a prospectus cover date, pricing date, delivery date, closing date, or effectiveness date that differs from the SEC filing date; that difference is not by itself a mismatch when the filing identifier or SEC filing detail supports the submitted EDGAR filing date.

Evidence facets:
- `ipo_up_c_structure`: IPO registration-statement or prospectus evidence that the issuer used an Up-C-style structure, with PubCo/OpCo or LLC ownership, exchangeable units, Class B voting stock, a tax receivable agreement, registration rights, or an organizational chart carrying the structure.
- `filing_sequence_and_timing`: official filing-history or filing-document evidence that distinguishes the IPO document date from the later registered-event SEC/EDGAR filing date and ties the later filing to the submitted event.
- `registered_offering_document`: the later S-1, S-1/A, 424B4, 424B5, 424B7, prospectus, or prospectus supplement surface showing the document's role for the registered event.
- `offering_character_and_proceeds`: filing evidence for the event's primary, secondary, selling-stockholder, resale, synthetic-secondary, use-of-proceeds, or no-proceeds mechanics.
- `underwriting_or_distribution_terms`: filing evidence for underwriters, underwriting discounts or options, firm-commitment terms, selling-stockholder plan of distribution, or other distribution mechanics.

Sources must be SEC EDGAR filing documents, SEC filing-detail pages, SEC submissions JSON, or company investor-relations mirrors only when they reproduce exact SEC filing content or exact SEC filing PDFs. Legal primers, law-firm summaries, academic papers, press articles, snippets, and generic filing summaries do not count as evidence for this task.

Registered events can be primary offerings, secondary or selling-stockholder offerings, resale registrations, synthetic-secondary transactions, or other registered prospectus events. A bare shelf registration with no concrete sale, resale, pricing, or distribution terms is not enough.

Keep the claim descriptive and factual. Do not provide legal, tax, investment, or capital-markets advice.

Requirements:
- The page must clearly identify or bind to the submitted company or issuer.
- The page must have the document role required for `evidence_facet`: for `ipo_up_c_structure`, an IPO registration statement or IPO prospectus for the company; for `filing_sequence_and_timing`, an official filing-history source or filing document that distinguishes the IPO document date from the later registered-event SEC/EDGAR filing date; for the other facets, the later registered-event filing or final prospectus/prospectus supplement tied to `event_date` and `filing_accession_or_file_id` through accession, file number, SEC filing detail, or filing metadata.
- The page must support the evidence required for `evidence_facet`: Up-C IPO structure; filing sequence and timing; registered offering document role; offering character and proceeds mechanics; or underwriting/distribution terms.

Write one JSON object per line to `results_upc_offering_mechanics.jsonl`:
{"item": { "company": "<company>", "event_date": "<event_date>", "filing_accession_or_file_id": "<filing_accession_or_file_id>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
