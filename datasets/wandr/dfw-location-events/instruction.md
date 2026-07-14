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

## `dfw_location_events`

For at least 40+ source-backed company-location events in the Dallas-Fort Worth area during January 1, 2025 through June 26, 2026, cover both of the 2 source families below for each event, supplying at least 1 public URL under each family. Each URL must sit on an event-specific page that establishes the named company's relocation, expansion, headquarters move, office or facility opening, consolidation, regional headquarters, manufacturing / logistics / R&D / operations site, data-center commitment, or comparable material DFW location commitment.

Treat one event as the combination of a company, a DFW city or site, a location-event kind, and an announcement/source date or source-labeled event timing. The same company can appear more than once for distinct DFW events, while repeated coverage of the same project belongs to one event. The relevant timing is the event's announcement/source date, approval/opening/commitment timing, or page-labeled future timing; an aggregate page updated during the period is not enough for an older event unless it reports a new in-window event stage.

Source families:
- `direct_or_civic`: a company-controlled announcement, durable press release or filing, government/state/city/county economic-development announcement, municipal agenda or council packet, incentive agreement, EDC or chamber narrative announcement, or comparable direct/civic source that is about the specific event.
- `independent_report`: a local, business, trade, site-selection, or comparable independently edited report about the specific event, or a later public lifecycle/status page from a different public institution that substantively reports the event rather than merely restating a list entry.

Construction or permit records only count when the cited page itself establishes the corporate location event and fits the submitted source family. Generic trend pieces, broker/property marketing, rankings, business advice, opinion, source-name-only list rows, social-only claims, and aggregate relocation/expansion tables that merely name companies do not count.

Requirements:
- The page must establish a named company's material DFW location event of the requested kind.
- The page must support the DFW city, site, address, campus, facility, DFW Airport location, or comparable source-stated Dallas-Fort Worth metro location for that event.
- The page must support the event's announcement/source date, approval/opening/commitment timing, or source-labeled future timing within January 1, 2025 through June 26, 2026.
- The page must support a concrete lifecycle or status anchor for the event, such as announcement, site selection, incentive approval, relocation underway/completed, opening, operational launch, construction phase, or source-labeled future opening/commissioning.
- Any jobs, investment, square footage, prior location, status, industry, incentive, or other event detail asserted for the event must be source-stated by the page.

Write one JSON object per line to `results_dfw_location_events.jsonl`:
{"item": { "company": "<company>", "dfw_site": "<dfw_site>", "event_kind": "<event_kind>", "event_timing": "<event_timing>", "source_family": "<source_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
