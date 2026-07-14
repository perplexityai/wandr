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

## `atlantic_canada_tech_company_ecosystem_evidence`

Identify 120+ companies as real technology or R&D-heavy companies with public Atlantic Canada evidence, and cover the 4 ecosystem facets listed below for each company by supplying 2+ distinct sources under each facet, each visibly supporting the company/facet finding.

The aim is an evidence panel for technology-company activity across the Atlantic Canada ecosystem: operations, products, support relationships, and commercialization signals, including acquired or renamed companies when the page still supports the historical or continuing submitted-company identity.

Ecosystem facets:
- `provincial_operation`: company-specific operation, headquarters, founding, office, facility, origin, contact, profile, or comparable operating tie to a named Atlantic province
- `technology_offering`: the company's product, platform, method, technical service, R&D direction, or technology capability
- `ecosystem_participation`: a named program, public funder, cluster, accelerator, incubator, association, university-commercialization path, trade delegation, or comparable ecosystem relationship involving the company
- `commercialization_signal`: a non-grant market or scale signal, such as a customer or deployment, sale/order/contract, revenue/adoption metric, product launch or market availability, private financing, acquisition or exit, listing, expansion, production scale-up, major commercial partnership, or comparable traction event

Companies ought to be named technology/product/R&D-heavy companies, including biotech, bioscience, ocean-tech, cleantech, software, hardware, AI, cyber, and healthtech companies. Generic programs, accelerators, government agencies, investor entities, directories, universities as institutions, pure support organizations, ordinary non-tech service shops, and classification-code-only entries are outside the company set.

Requirements:
- The page must clearly identify the named company.
- The page should make its selected `ecosystem_facet` role visible. For `provincial_operation`, it should read as a company-specific operation, contact, about, profile, history, office, facility, headquarters, founding, origin, or comparable source; a broad funding, mission, event, or delegation list grouped by province is not enough by itself. For `technology_offering`, it should read as a company/product/R&D/technical source with real offering detail; a one-line funded-project blurb, conference-attendee listing, sector tag, or bare domain label is not enough. For `ecosystem_participation`, it should show the named ecosystem actor or relationship involving the company, including public funding and program relationships. For `commercialization_signal`, it should show a market or scale milestone involving the company; public grants/funding, public-program support, or trade-delegation attendance alone belong to `ecosystem_participation`, not this facet.
- The page should expose a focused finding for the selected `ecosystem_facet`: an operation, headquarters, founding, office, facility, origin, contact/profile, or comparable company tie to Nova Scotia, New Brunswick, Prince Edward Island, or Newfoundland and Labrador for `provincial_operation` ("Atlantic Canada" or "Maritimes" alone is not enough for this facet); a named product/platform/technology/method/technical service or technical capability with detail beyond a sector label for `technology_offering`; a named program / public funder / cluster / accelerator / incubator / association / university-commercialization / trade-delegation or comparable relationship for `ecosystem_participation`; or a customer/deployment, sale/order/contract, revenue/adoption metric, product launch/market availability, private financing, acquisition/exit, listing, expansion, production scale-up, major commercial partnership, or comparable non-grant traction signal for `commercialization_signal`.

Write one JSON object per line to `results_atlantic_canada_tech_company_ecosystem_evidence.jsonl`:
{"item": { "company": "<company>", "ecosystem_facet": "<ecosystem_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
