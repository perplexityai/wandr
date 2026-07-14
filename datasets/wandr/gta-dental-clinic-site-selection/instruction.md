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

## `gta_dental_clinic_site_selection`

For all the 13 submarkets listed below, build a feasibility evidence pack for a Greater Toronto Area cosmetic-and-implant dentistry clinic opening targeted for 2026-2027 by covering each of the 4 site-selection domains with at least 2 meaningfully distinct submarket-specific signals per domain, each backed by a source (i.e. 1+ URL per signal), then synthesize the evidence into a ranked site-selection recommendation.

The aim is a market-research comparison base that can separate demand quality, competitive saturation, lease economics, and practical street-level site fit for a new specialty dental clinic.

Target submarkets (canonical name — accepted aliases):
- **Downtown Toronto** — Toronto downtown core, Downtown core, Old Toronto, Financial District, Entertainment District, King West, Queen West, St. Lawrence, Toronto Waterfront
- **Midtown Toronto** — Yonge-Eglinton, Yonge and Eglinton, Davisville, Leaside, Forest Hill, Summerhill, Rosedale
- **North York** — North York Centre, Yonge-Sheppard, Yonge and Sheppard, Willowdale, Bayview Village, Don Mills
- **Scarborough** — Scarborough Town Centre, STC, Agincourt, Cliffside, Birch Cliff, Golden Mile
- **Etobicoke** — The Kingsway, Kingsway, Mimico, Humber Bay Shores, Islington, Bloor West Etobicoke
- **Mississauga** — City Centre Mississauga, Mississauga City Centre, Square One, Port Credit, Erin Mills, Cooksville
- **Brampton** — Downtown Brampton, Bramalea, Mount Pleasant Brampton, Brampton Gateway
- **Vaughan** — Vaughan Metropolitan Centre, VMC, Woodbridge, Maple, Thornhill Vaughan, Kleinburg
- **Markham** — Unionville, Downtown Markham, Markham Centre, Cornell, Buttonville
- **Richmond Hill** — Richmond Hill Centre, Oak Ridges, Bayview Hill, Yonge Street Richmond Hill
- **Oakville** — Downtown Oakville, Bronte, Kerr Village, Uptown Core, Joshua Creek
- **Burlington** — Downtown Burlington, Burlington Centre, Aldershot, Appleby, Millcroft
- **Pickering-Ajax-Whitby** — Pickering, Ajax, Whitby, Pickering Ajax Whitby, Pickering-Ajax, Ajax-Whitby, Durham west corridor, West Durham

Site-selection domains:
- `demographic_demand`: census or official statistical evidence on household income, population density, age profile, and population growth over the 2016-2021 census period for the relevant geography
- `competitive_supply`: nearby dental, implant dentistry, cosmetic dentistry, oral-surgery, orthodontic, or med-aesthetic provider evidence that helps characterize saturation and service gaps
- `lease_supply`: current commercial unit evidence for clinic-suitable space, including address, unit size, asking rent / rate when shown, and listing-source context
- `access_visibility`: location evidence on transit, highway / arterial access, parking, frontage / signage, medical-retail co-tenancy, pedestrian activity, or other visibility and accessibility factors

Use the evidence pack to produce a scored ranking table across demographics, competition, visibility, accessibility, growth, and lease cost; name the top 3 submarkets; shortlist 5 specific lease properties; and give one final property recommendation. The synthesis draws each numerical figure from a cited source, with unconfirmed figures shown as `unknown`.

Requirements:
- The page must clearly tie the signal to the named submarket, either through the named municipality / neighbourhood or through a specific address, provider, listing, transit node, or statistical geography located there.
- The page must make its site-selection-domain source role visible. For `demographic_demand`, use an official census / statistical profile, municipal profile, planning profile, or another quantitative geography source; a page that reproduces a census / statistical figure for a stated geography and reporting period carries this role regardless of who hosts it, while a page that only characterizes the area in qualitative terms does not. For `competitive_supply`, use a map or business-profile surface, clinic-owned page, provider directory, or similar provider-identification page. For `lease_supply`, use an active commercial listing, brokerage flyer, landlord listing, or comparable lease-marketing page. For `access_visibility`, use a property/location page, transit or transportation page, map/location profile, planning document, or any source that directly speaks to access or visibility.
- The page must expose a focused signal scoped to the site-selection domain. For `demographic_demand`, the signal must be a single quantified data point tied to a stated geography and reporting period, not a qualitative characterization of the area. For `competitive_supply`, it must identify named relevant providers, provider counts / clusters, specialty service lines, review-volume / rating signals, or an observable market gap. For `lease_supply`, it must identify a specific currently marketed unit or property with address and size, plus asking rate / rent when available. For `access_visibility`, it must show a concrete accessibility or visibility factor such as station proximity, highway / arterial frontage, parking, signage, retail anchor, medical co-tenancy, or pedestrian corridor.
- The page must support any numerical value or status claimed for the signal, including the relevant geography, measurement period, listing status, provider name, address, square footage, or asking rate when those are part of the claim.
- Current-market signals must have current relevance on the page: an active listing state, present-tense provider / location profile, current transit or access description, current map / directory context, or a publication / update date appropriate to the claim. Closed clinics, stale unavailable listings, and obsolete access claims do NOT count.

Write one JSON object per line to `results_gta_dental_clinic_site_selection.jsonl`:
{"item": { "submarket": "<submarket>", "site_selection_domain": "<site_selection_domain>", "site_selection_signal": "<site_selection_signal>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
