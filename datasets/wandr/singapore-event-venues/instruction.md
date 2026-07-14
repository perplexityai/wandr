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

## `singapore_event_venues`

For 5+ of the Singapore event-venue families below, name 300+ venues per family and supply at least 1+ official source URL per venue. Each source should be about a Singapore venue, property, or named bookable event space that publicly documents event-hosting capability and at least one concrete numbered venue capability.

Venue families:
- `hotel_resort_integrated_resort`: hotels, resorts, serviced residences, and integrated resorts whose own public material documents meetings, weddings, banquets, conferences, incentives, gala dinners, or comparable events.
- `convention_exhibition_large_hall`: convention centres, exhibition centres, conference centres, theatres, auditoria, and large halls with public event, conference, exhibition, or technical venue specifications.
- `cultural_heritage_gallery_museum`: museums, galleries, theatres, heritage buildings, civic arts spaces, and cultural institutions that rent named spaces for events.
- `attraction_garden_wildlife_leisure`: gardens, attractions, wildlife destinations, leisure destinations, and scenic venues with public corporate, wedding, reception, product-launch, or social-event capability.
- `club_institution_campus_community`: clubs, member associations, universities, campuses, training centres, community venues, and similar institutional spaces with public event-hire or meeting-room capability.

Official cited URLs can come from:
- venue-owned meeting, event, wedding, banquet, room, space, or venue-hire pages.
- venue or operator PDF brochures, capacity charts, fact sheets, floor plans, technical guides, or service manuals.
- venue-specific pages from official destination, attraction, tourism, or government-backed venue portals.
- official event or organiser manuals for a real event at the submitted venue, but only when the document is venue-branded or clearly venue/operator-issued or approved and exposes venue-specific specifications.

Official event or organiser manuals count only when they are for a real event at the submitted venue and the document itself is official venue material, venue-branded technical guidance, or clearly venue/operator-issued or approved venue specifications for the submitted venue. A congress, exhibition, or event upload is not enough by itself.

For each source, report the operator or brand when public, Singapore precinct or location, submitted venue family, principal event space or venue-level scope, event use case, capability measurement, setup or measurement basis, capability category, official source type, visible source date when public, and a short limitation note for gated, partial, stale, or promotional specs.

Useful capability measurements include:
- setup-specific capacity, standing capacity, theatre capacity, banquet capacity, classroom capacity, or similar pax counts.
- event-space area, floor area, function-room count, guest-room count, booth count, or package/menu price.
- named-space dimensions, ceiling height, floor loading, freight-door or loading-bay dimensions, rigging or hall connectivity.
- built-in AV, LED wall or screen dimensions, live-streaming, hybrid-event support, Wi-Fi, or other technical fit-out.
- on-site catering, halal/vegetarian/dietary package support, sustainable meeting practice, accessibility, or accommodation adjacency.

Cvent, Tagvenue, Venuerific, SingaporeBrides, planner blogs, travel agency pages, booking marketplaces, and directory result pages can be useful discovery or corroboration surfaces, but the cited URL should be an official or official-adjacent source for the submitted venue. Do not turn the task into rankings, recommendations, lead generation, procurement advice, or venue quality judgments.

Requirements:
- The page must identify the submitted Singapore venue / property / named event space and show public event-hosting capability.
- The page must support the submitted venue family rather than merely listing a broad precinct, hotel chain, operator, vendor, or marketplace category.
- The page must state at least one concrete number-bearing event capability for the venue or a named space within it.
- The page must give enough capability context to preserve what the number measures, especially setup basis, named-space scope, technical specification, service package, accessibility, sustainability, accommodation, catering, or operational context when stated.

Write one JSON object per line to `results_singapore_event_venues.jsonl`:
{"item": { "venue_family": "<venue_family>", "venue": "<venue>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
