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

## `hdd_fiber_contractors`

For 450+ U.S. contractors that publicly perform HDD, directional boring, trenchless underground construction, or comparable underground utility construction for fiber, telecom, broadband, communications conduit, FTTH, middle-mile, or outside-plant work, supply evidence for each of the 2 evidence types, with 1+ source URL per type. This is public contractor capability provenance, not contractor ranking, buyer recommendation, outreach prioritization, contact enrichment, insurance strategy, lead scoring, or a prospecting list.

The evidence types are:
- `capability_source`: an official contractor/company-controlled source naming the contractor and stating both HDD, directional boring, trenchless, or underground utility construction capability and a fiber, telecom, broadband, communications conduit, FTTH, middle-mile, or outside-plant application.
- `public_corroboration`: a separate non-company public source naming the same contractor and giving provider-specific public accountability, project, registry, association, trade, or comparable corroboration.

For downstream reading, optional factual notes can include canonical contractor name, legal or DBA name when source-stated, parent/subsidiary or operating-brand context when source-stated, source-stated state or service geography, source class, HDD/fiber capability phrase, public corroboration context, bid/award/registry/project role when applicable, source date or observed date, checked date, confidence, and source notes. Use 2026-06-30 as the checked date unless the source was checked later. Do not include leadership names, phone numbers, emails, estimators, contact people, rankings, lead scores, outreach priority, buyer recommendations, or procurement advice.

Useful HDD or underground construction terms include:
- `horizontal directional drilling (HDD)`
- `directional drilling`
- `directional boring`
- `trenchless underground construction`
- `underground utility construction with boring or conduit placement`
- `microtrenching tied to underground communications construction`

Useful fiber/telecom application terms include:
- `fiber optic cable or conduit`
- `telecom or communications conduit`
- `broadband or internet infrastructure`
- `FTTH, FTTx, middle-mile, or long-haul fiber`
- `outside-plant or OSP communications construction`
- `wireline communications construction`

Useful public corroboration source types include:
- `official bid, award, bid-tab, or apparent-bid result`
- `municipal, traffic, utility, or construction notice`
- `permit, right-of-way, lane-closure, or public works notice`
- `state registry, license, vendor, prequalification, or work-code record`
- `trade association profile or member record`
- `trade publication, project article, or manufacturer case study`
- `provider-specific public directory profile with concrete accountability facts`
- `other non-company public corroboration source`

Source class should be factual, not promotional. Useful public source classes include:
- `contractor capability page`
- `contractor project or case-study page`
- `official contractor profile`
- `municipal or utility construction notice`
- `bid, award, or bid-tab record`
- `permit, right-of-way, or public works notice`
- `registry, license, vendor, prequalification, or work-code record`
- `trade association member profile`
- `trade/project article or manufacturer case study`
- `provider-specific public directory/profile`
- `other public source`

Boundary classes to keep out unless the page also proves contractor-specific evidence at the submitted role:
- `generic fiber contractor with no HDD, boring, trenchless, or underground utility capability`
- `generic driller, excavator, or trenchless contractor with no fiber, telecom, broadband, communications, or OSP application`
- `water, sewer, gas, pipeline, or environmental HDD evidence only`
- `aerial-only, splicing-only, in-building wiring, cabling, or low-voltage installer evidence`
- `ISP, network owner, BEAD subgrantee, or equipment vendor with no construction-contractor role`
- `lead funnel, quote-request site, contact database, private prospect list, insurance broker page, or outreach material`
- `generic listicle, industry explainer, SEO landing page, search result, or undifferentiated directory`

Public sources can include contractor capability pages, contractor project pages, official profiles, public bid/award/bid-tab records, municipal/traffic/utility/construction notices, permit or right-of-way notices, public utility procurement pages, registry/license/prequalification/vendor work-code records, trade association profiles, trade or project articles, manufacturer case studies, and provider-specific public directory profiles. Use a distinct source class for each evidence role; the same URL should not be reused as both `capability_source` and `public_corroboration`. Company-owned pages do not count as public corroboration for their own contractor, and non-company pages do not count as the contractor-controlled capability source unless the page is an official contractor-controlled profile.

Requirements:
- The page must identify the claimed contractor, or bridge the submitted trade name to a legal, DBA, subsidiary, parent, or operating-brand name, with enough public context to distinguish it from unrelated same-name contractors.
- The submitted page itself must fulfill the claimed `evidence_type`: `capability_source` evidence should be an official contractor/company-controlled source, while `public_corroboration` evidence should be a separate non-company public source for the same contractor.
- The page must support role-specific contractor substance. For `capability_source`, it must source-state both an HDD, directional-boring, trenchless, or underground utility construction capability and a fiber, telecom, broadband, communications conduit, FTTH, middle-mile, or OSP application. For `public_corroboration`, it must show a concrete provider-specific public accountability, project, registry, association, trade, or comparable corroboration fact for the same contractor.

Write one JSON object per line to `results_hdd_fiber_contractors.jsonl`:
{"item": { "contractor": "<contractor>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
