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

## `hkex_ipo_pipeline_market_map`

For 200+ HKEX IPO applicants whose application round remained pre-listing in the task snapshot as of June 17, 2026, name the applicant and application-round submission date. For each application, cover 3+ pipeline axes with 1+ concrete facts and 1+ substantiating URLs per axis.

Treat an applicant application as the applicant company plus the application-round submission date. Later AP, OC, PHIP, status, or listed-parent notices for the same applicant belong to that same application round unless they show a genuine renewed or resubmitted round. Rounds submitted before December 17, 2025 need renewal or current-status evidence showing that they remained non-listed as of June 17, 2026; an application-round submission date on or after December 17, 2025 can carry the non-listed pipeline boundary unless the page itself shows a terminal outcome.

The finding itself should carry the concrete fact. Auxiliary notes such as board / route or event date are helpful when visible, but they are not substitutes for applicant-specific evidence. Historical application-stage facts such as filing dates, OC appointments, Application Proof sector sections, or scale metrics can support a qualifying application fact, but pages that show the round already listed, lapsed, withdrawn, rejected, or returned do not qualify that application.

Pipeline axes:
- **application_status** -- A1 / Application Proof / OC / PHIP draft-not-approved wording, under-processing / approved-pending status, board or route, or other dated application-stage status facts for an application round that remains non-listed in the task snapshot
- **sponsor_adviser** -- joint sponsors, sponsor-overall coordinators, overall coordinators, underwriters, issuer counsel, sponsor counsel, or other named advisers tied to the HKEX application
- **business_sector** -- industry, subsector, business model, core products or services, or route-relevant sector description for the applicant
- **deal_size_or_scale** -- proposed fundraising, offer size, issue size, price range, valuation, use-of-proceeds amount, or operating scale proxy where Application Proof proceeds are redacted
- **timeline_milestone** -- filing / submission date, OC appointment date, Application Proof date, PHIP date, Listing Committee hearing or approval date, offer period, pricing date, expected listing date, or other dated milestone for the non-listed pipeline application round

Target pages differ by pipeline axis:
- `application_status`: applicant-specific Application Proofs, OC announcements, PHIPs, applicant or listed-parent spin-off announcements, or per-applicant HKEX status entries that explicitly report the round's current status.
- `sponsor_adviser`: the applicant's OC announcement, the Application Proof page that names the sponsors and overall coordinators, a joint-sponsor / underwriter / counsel deal-team note, or applicant-focused capital-markets coverage that names the advisers.
- `business_sector`: the Application Proof business / industry section or applicant-focused capital-markets coverage that characterizes the business model.
- `deal_size_or_scale`: the Application Proof operating-scale / financial section, applicant-focused capital-markets coverage reporting valuation or proceeds, or a listed-parent disclosure giving the spin-off proceeds.
- `timeline_milestone`: the applicant-specific announcement that carries the milestone itself, such as an OC announcement for an OC-appointment milestone, an AP / PHIP cover page for a filing milestone, a spin-off announcement for a board-resolution milestone, or applicant-focused coverage of the same event.

Strong evidence usually names the applicant and proposed listing directly, such as HKEX Application Proofs, OC announcements, PHIPs, HKEX status records, applicant or listed-parent spin-off announcements, sponsor or law-firm deal notes, or reputable capital-markets and trade coverage focused on that applicant.

Requirements:
- The page must identify the same listing applicant you are naming. A listed parent, controlling shareholder, sponsor, or trade outlet counts only when it explicitly ties the text to that applicant's HKEX listing application, proposed spin-off, Application Proof, OC announcement, PHIP, or a similar application-stage event.
- The page must be about the same HKEX application round and keep it eligible as a non-listed pipeline application: either an application-round submission date on or after December 17, 2025, or renewal / current-status evidence showing the round remained non-listed as of June 17, 2026. Nothing on the page can place that round into a later listed, lapsed, withdrawn, rejected, or returned outcome.
- The page must actually speak to the kind of pipeline fact being claimed: status, sponsor / adviser, business sector, size / scale, or timeline.
- The page must support the specific sponsor / adviser, status phrase, sector, size / scale, date, or milestone being claimed, without stronger claims than the page makes.
- The source must be applicant-specific or transaction-specific.
- The page must anchor the relevant date or status. Current non-listed status claims need a current status source or explicit as-of marker; dated AP / OC / PHIP / submission facts can support other angles only when the application-round date is inside the active window or the application also has renewal / current-status support.

Write one JSON object per line to `results_hkex_ipo_pipeline_market_map.jsonl`:
{"item": { "applicant": "<applicant>", "filing_date": "<filing_date>", "pipeline_axis": "<pipeline_axis>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
