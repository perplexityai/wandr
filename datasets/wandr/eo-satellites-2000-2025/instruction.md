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

## `eo_satellites_2000_2025`

For at least 150+ named Earth-observation satellites launched during 2000-01-01 through 2025-12-31, supply per-spacecraft technical-profile evidence with at least 1 URL per (operator/agency, satellite). In-scope mission classes are civilian, commercial, government, meteorological, scientific, and civil dual-use Earth-observation / remote-sensing spacecraft, including optical, multispectral, hyperspectral, thermal, atmospheric, ocean, weather, radar, and SAR satellites.

Requirements:
- The page must be a per-satellite profile or a narrow mission-family profile with a dedicated fact row/section for the submitted satellite. Suitable source surfaces include operator or owner mission pages; national, regional, or international space-agency mission pages; recognized EO mission directories such as NASA NSSDCA, ESA EO Portal, WMO OSCAR, USGS/NASA/JAXA/ISRO/CNES technical profiles; and per-satellite technical reports or fact sheets.
- The page must support the submitted launch date claim within 2000-01-01 through 2025-12-31 plus the submitted launch context claim, such as launch vehicle, launcher family, launch site, or named launch mission.
- The page must frame the spacecraft as Earth observation, remote sensing, environmental/meteorological observation, or Earth science, and support the submitted sensor/payload class claim.
- The page must support the submitted orbit claim with the orbit regime/type or at least one quantitative orbit attribute such as altitude, inclination, period, repeat cycle, or geostationary slot.
- The page must support the submitted payload-specific measurement or imaging performance claim, such as spatial resolution, swath, spectral bands, radar frequency/wavelength, revisit, acquisition rate, or data product resolution.
- The page must support the submitted lifecycle/status claim for the submitted satellite: active/current/operational/in-operation, commissioning/first-light, retired/lost/failed/deorbited, or design-life/mission-duration language tied to the satellite.

Write one JSON object per line to `results_eo_satellites_2000_2025.jsonl`:
{"item": { "operator": "<operator>", "satellite": "<satellite>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
