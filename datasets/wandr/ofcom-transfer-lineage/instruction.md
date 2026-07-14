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

## `ofcom_transfer_lineage`

For 100+ current/as-of Ofcom Wireless Telegraphy Register licence records, cover both of the 2 source families below for each record and supply 1+ official public URL under each family.

Treat one licence record as the combination of an exact Ofcom licence number, the public licensee or source-stated holder name, and the licence product, class, or sector. The task is a public source table for Wireless Telegraphy Register provenance, not spectrum trading advice, RF engineering, compliance/legal advice, contact enrichment, licensee ranking, alerts, or deployment inference.

Source families:
- `current_wtr_row`: an official current Ofcom Wireless Telegraphy Register or Spectrum Information System source that row-localizes the exact keyed licence number and states the current/as-of WTR provenance.
- `record_specific_official_context`: a separate official Ofcom licence PDF, licence document, award/variation/transfer notice, shared-access notice, licence-terms publication, or comparable Ofcom source that is specific to the individual licence record. It should identify the exact licence number; if the document omits the licence number, it must be a licence-record-specific publication or notice that uniquely identifies the same licensee or holder together with the same product, sector, service, spectrum band, or licence context.

For each licence record, the `record_specific_official_context` URL must be distinct from the `current_wtr_row` URL. The record-specific context cannot be satisfied by repeating the WTR CSV/register URL, the TNR CSV/register URL, a generic Ofcom spectrum landing page, a broad frequency/band assignment table, a broad spectrum-assignment CSV/data table, or any other source whose only tie to the record is a table row in a broad band/service dataset. Use a licence-specific document, notice, or publication instead.

Use official Ofcom sources only. WTR/SIS rows, Ofcom licence PDFs, Ofcom spectrum-trading or transfer notices, shared-access data or notices, award/variation publications, and product-specific licence context can count when they carry record-specific evidence. Do not use third-party WTR lookups, stale mirrors, data.gov.uk archives, geocoders, enriched contact/licence directories, broker pages, dashboards, or social pages as authoritative evidence.

The target record content is official licence provenance only. Contact-person names, phone numbers, email addresses, postal/contact addresses, inferred site coordinates, inferred postcodes/cities, RF calculations, coverage predictions, interference conclusions, and trading/legal recommendations are not target facts. Public licensee and holder organization names are allowed.

Requirements:
- The page must satisfy the submitted source-family role: current-WTR row evidence for `current_wtr_row`, or a record-specific official context source for `record_specific_official_context`.
- The page must identify the exact keyed licence number and tie it to the submitted licensee or holder for `current_wtr_row`; for `record_specific_official_context`, it must either identify the exact keyed licence number or be a licence-record-specific document/notice/publication that uniquely ties the same licensee or holder to the same product, sector, service, spectrum band, or licence context.
- The page must state or clearly anchor the product, class, sector, licence type, spectrum band, service, or comparable licence scope for the record.
- Current-WTR rows must state current status, licensee/holder, publishability/tradability, frequency, location/geographic state, or another source-stated current WTR field. Record-specific context rows must state licence issue, award, variation, transfer, shared-access, licence terms, licence-specific publication detail, or another source-stated official context fact for the same licence record.
- The page must preserve source currency using source-stated issue date, publication date, update date, file vintage, or document/version date when visible.

Write one JSON object per line to `results_ofcom_transfer_lineage.jsonl`:
{"item": { "licence_number": "<licence_number>", "licensee": "<licensee>", "product_or_sector": "<product_or_sector>", "source_family": "<source_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
