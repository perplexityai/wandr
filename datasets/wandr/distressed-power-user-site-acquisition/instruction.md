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

## `distressed_power_user_site_acquisition`

For 40+ distressed or available non-crypto heavy-industrial site opportunities in the United States and Canada, cover each of the 3 evidence axes below. For every (site, evidence axis) cell, submit 1+ concrete site finding, supplying a source (1+ URL per finding).

Treat May 12, 2026 as the status snapshot date. Distress and availability evidence is anchored to January 1, 2020 through May 12, 2026; do not use relative timing such as "recently" unless the page itself provides an absolute date or a current status at the snapshot.

This is an acquisition-screen and site-sourcing task, not a recommendation to build cryptocurrency mining. The site must not already be presented as a purpose-built cryptocurrency-mining, blockchain, hyperscale, or data-center campus. A completed sale only remains relevant when the cited page still presents tenant, parcel, lease, redevelopment, or reuse opportunity.

Use the site, locality, region/state/province, and country fields to identify a specific physical mill, smelter, plant, complex, parcel, or redevelopment property. Use the finding string to name one concrete fact that the page substantively supports for the submitted evidence axis. Submit one fact per row. Multiple atomic facts that sit on the same page - say, an acreage fact, a cogeneration fact, a rail-access fact, and a heavy-zoning fact for a single infrastructure site - belong on separate rows, not stuffed into one enumeration string. The finding may carry a small amount of natural supporting context (a date attached to a status event, a process anchor attached to a steel-mill identification), but it should not stack five or six independent specifics that the page only loosely supports.

Use only these evidence axes:

- **distress_availability** - distress, closure, sale, lease, auction, remediation, or redevelopment availability: a site-specific public signal dated or current within January 1, 2020 through May 12, 2026: closure, idling, bankruptcy, sale, lease, sealed-bid process, auction, tenant search, brownfield remediation, cleanup-driven reuse, redevelopment solicitation, or remaining land/space availability. A completed sale only qualifies when the page still presents remaining tenant, parcel, lease, redevelopment, or reuse opportunity.
- **power_intensive_industrial_use** - heavy-power industrial use proxy: site-specific evidence that the physical site was built for or operated as a power-intensive industrial facility, such as an aluminum/copper/lead smelter, steel mill, pulp or paper mill, glass plant, cement/lime/mineral plant, chemical or petrochemical plant, refinery, foundry, furnace-heavy manufacturing site, or similarly energy-intensive process facility. Warehouses, light assembly, offices, generic distribution buildings, and ordinary textile/light-industrial buildings do not qualify unless the page gives a concrete heavy-process power proxy.
- **site_infrastructure_reuse** - reuse infrastructure relevant to industrial power-site screening: site-specific infrastructure evidence useful for an acquisition screen: acreage, large manufacturing buildings, cranes, switchgear, transformers, substations, power capacity, cogeneration plant, utility provider/electric service, natural-gas service, water/wastewater/cooling-water assets, rail/port access, heavy zoning, remediation status, asking price, lease rate, tenant-ready space, or similar brownfield/property facts.

Expected source standing by evidence axis:

- **distress_availability** - broker/listing pages, owner or buyer announcements, bankruptcy or restructuring notices, local economic-development pages, redevelopment-authority pages, public cleanup/remediation updates, credible local business press, or official company filings
- **power_intensive_industrial_use** - operator or former-operator pages, broker/listing pages, equipment-auction pages, regulatory records, redevelopment pages, local economic-development pages, or credible business/trade coverage that names the industrial process at the site
- **site_infrastructure_reuse** - broker/listing pages, redevelopment-authority pages, buyer/owner reuse announcements, public brownfield or remediation updates, equipment-auction pages, utility/economic development pages, or credible local business press

The following are outside the site-opportunity universe:

- **already crypto or data-center conversions** - sites already presented as cryptocurrency mining facilities, blockchain campuses, hyperscale/data-center campuses, or completed conversions to those uses
- **active plants without an availability path** - active plants do not qualify as complete site opportunities unless separate distress_availability evidence supports a qualifying distress, sale, lease, remediation, redevelopment, or tenant-availability path inside the anchored window
- **light industrial or warehouse-only properties** - warehouses, offices, logistics buildings, light assembly, or ordinary textile/light industrial properties without a concrete heavy-power industrial process or infrastructure proxy
- **generic closures without a site opportunity** - plant-closure stories that do not identify a reusable physical site, owner, buyer, auction, sale, lease, remediation, or redevelopment path
- **broker pages without site identity** - anonymous broker teasers that do not identify the physical site well enough to screen the asset

Requirements:
- The page must identify the same physical site at the submitted granularity.
- The page source class must fit the selected evidence axis.
- The page must substantively support the submitted finding for the selected evidence axis, and the excerpts must faithfully carry the load-bearing facts in the finding.
- The finding should be one concrete page-supported fact for the selected evidence axis, not an enumeration of several. Use separate rows for separate atomic facts on the same page.

Write one JSON object per line to `results_distressed_power_user_site_acquisition.jsonl`:
{"item": { "site": "<site>", "locality": "<locality>", "region": "<region>", "country": "<country>", "evidence_axis": "<evidence_axis>", "finding": "<finding>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
