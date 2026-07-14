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

## `medica_2026_western_europe_exhibitor_evidence`

Identify 110+ companies as Western-Europe-based organizations publicly tied to MEDICA 2026; for each company, cover each of the 4 evidence facets below with a source whose page-local content fits that facet (i.e. 1+ URL per facet).

The goal is a multi-surface exhibitor evidence panel: the useful work is separating event, home-identity, product, and external-activity evidence for the same company.

Eligible Western European home countries:
- **Austria**
- **Belgium**
- **France**
- **Germany**
- **Ireland**
- **Italy**
- **Luxembourg**
- **Netherlands**
- **Portugal**
- **Spain**
- **Switzerland**
- **United Kingdom**

Evidence facets:
- `event_presence`: public evidence that the company is tied to MEDICA 2026.
- `home_market_identity`: public evidence of the company's home-market identity in an eligible Western European country.
- `product_evidence`: company-controlled evidence of a concrete healthcare, medtech, diagnostics, digital health, device, supplier, distribution, or healthcare-service offering.
- `external_activity_profile`: non-company, non-MEDICA-event evidence of the company's healthcare or medtech activity, sector role, registry/activity posture, or public business footprint.

`company` ought to be a real operating organization in the healthcare / medtech ecosystem and based in one of the eligible countries. MEDICA, COMPAMED, event organizers, event pages, individual people, products, product categories, booth numbers, attendee-list publishers, and attendee databases are not company identities for this purpose. MEDICA or COMPAMED organizer pages are event surfaces only: an event-side country tag is not home-market identity evidence, and an event-side category tag is not product evidence or external-activity evidence.

Requirements:
- The page must clearly identify the named company or a visible legal / trading identity for that same company.
- The page should make its facet-appropriate source role visible through page-local anchors. For `event_presence`, the page should read as a MEDICA 2026 event-presence surface, such as an official MEDICA profile/API/meta page, a company-controlled event page, or a trade-press event announcement. For `home_market_identity`, the page should read as company identity evidence, such as an imprint, legal notice, registry record, registered-office page, official about page, or comparable identity surface carrying an eligible country. For `product_evidence`, the page should be controlled by the company and read as a product, service, catalogue, datasheet, case, or offering surface. For `external_activity_profile`, the page should be outside the company's own control and outside MEDICA/COMPAMED event-organizer surfaces, with enough profile, registry, sector, trade-press, standards, or public business context to be about the company's activity rather than merely repeating event-attendance metadata.
- The page should expose a focused finding for the selected facet. For `event_presence`, it should show MEDICA 2026 participation or event association for the company. For `home_market_identity`, it should tie the company to one eligible country through registered office, legal identity, official identity, registry, or comparable home-market evidence. For `product_evidence`, it should show a concrete healthcare / medtech offering, product family, service, technology, or distribution/supplier capability. For `external_activity_profile`, it should substantively describe the company's healthcare / medtech activity, sector role, registry/activity posture, or public business footprint beyond an attendee-list mention.

Write one JSON object per line to `results_medica_2026_western_europe_exhibitor_evidence.jsonl`:
{"item": { "company": "<company>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
