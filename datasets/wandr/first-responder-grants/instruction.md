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

## `first_responder_grants`

For 4+ of the source families below, name 20+ private/corporate or privately administered funders per source family, name 1+ current or recent (2024-2026) first-responder or public-safety funding program cycle per funder, and supply 1+ official or administering-source URL for each program cycle.

The source-family values are:
- `telecom_wireless_tower`: telecom, wireless, broadband, tower, communications-network, or emergency-connectivity operators, foundations, sponsors, or named funds
- `energy_grid_pipeline`: electric, gas, grid, power, fuel, pipeline, wildfire-grid, or comparable energy-infrastructure operators, foundations, sponsors, or named funds
- `transportation_logistics`: rail, trucking, port, aviation, shipping, fleet, or comparable transportation/logistics infrastructure operators, foundations, sponsors, or named funds
- `public_safety_technology`: public-safety technology, emergency communications, dispatch, rescue equipment, safety engineering, security/risk, or comparable technology and equipment companies, foundations, sponsors, or named funds
- `administered_corporate_sponsor`: direct corporate/private foundations, company-sponsored funds, named private funds, or administering partner pages with a clear corporate/private sponsor

The useful record is a dated source-backed program cycle, not a grant directory entry or application-advice page. Alongside each source, include brief notes for the source-family rationale, type of support, target or eligibility scope, cycle/window and open/closed/rolling/history status, deadline/application period when stated, amount/cap/total pool when stated, source date when visible, and the date you checked the page. If an official source establishes the cycle but does not state an amount or deadline, say that rather than inventing one.

Eligible funders include private-sector companies, corporate foundations, company-sponsored charitable funds, and private funds administered by community foundations, trade associations, or similar partners when the named corporate/private sponsor or named fund is clear. Use the controlling corporate sponsor, corporate foundation, or named fund as the funder identity; local operating-company labels from the same parent and same branded template should not be used as separate funders unless the source establishes a genuinely separate sponsor, fund, or non-template cycle.

Official company, corporate-foundation, program, application, official news, grant-history, community-foundation, trade-association, or administering-partner pages can count when they carry the program-cycle facts and make the private/corporate funder or named fund clear. Grant aggregators, scraped opportunity listings, social-media-only claims, government-only grant programs, recipient-only award announcements, generic corporate giving pages, broad community grants without public-safety targeting, water/sewer-only utility grants, disaster/network-response marketing, first-responder discounts, advisory councils, public-safety sales pages, and legal/permitting uses of "grant" do not establish a qualifying cycle.

Requirements:
- The page must communicate that the submitted funder or program belongs to the submitted source family rather than a generic utility, water, community-giving, discount, sales, or directory shortcut.
- The page must tie the submitted funder, sponsor, foundation, or named fund to the submitted program cycle through an official or administering-source context.
- The page must describe a concrete grant, award, scholarship, equipment/training support, emergency hardship/family support, or comparable funding/support program.
- The page must target first responders, public-safety agencies, fire/EMS/police departments, emergency-response organizations, first responders' families/dependents, or a closely equivalent public-safety population.
- The page must anchor the submitted cycle/window as current or recent in 2024-2026, rolling/evergreen with current page evidence, recently closed with explicit cycle status, or award-history evidence from that period, and must expose enough program terms to distinguish the cycle from generic giving.

Write one JSON object per line to `results_first_responder_grants.jsonl`:
{"item": { "source_family": "<source_family>", "funder": "<funder>", "program_name": "<program_name>", "cycle_window": "<cycle_window>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
