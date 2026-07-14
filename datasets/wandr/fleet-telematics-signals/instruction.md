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

## `fleet_telematics_signals`

For at least 100+ public fleet-telematics, ELD/compliance, vehicle-tracking, fleet-safety, or adjacent fleet-management platforms, cover 2+ of the operational-signal families listed below per platform. Within each platform-family pair, name 3+ distinct source-backed UI signals and supply 1+ public URL for each signal.

The useful object is the operational meaning of a public UI cue: a status label, icon, badge, dot, banner, status column, dial, map/list marker, card, or similar signal that tells fleet users about an exception or important state change. Describe cues in words only; do not reproduce icons, screenshots, or other UI assets.

Operational-signal families:
- `diagnostics_maintenance`: engine faults, diagnostic trouble codes, malfunction indicators, severity/status fields, maintenance alerts, or similar vehicle-health signals
- `hos_eld_compliance`: HOS/ELD malfunctions, diagnostics, violations, remaining-time dials, duty-status signals, or similar compliance-state cues
- `device_camera_data_health`: gateway, tracker, dashcam, camera, GPS-quality, data-freshness, non-reporting, disconnected, powered-off, or other device-health cues
- `safety_video_emergency`: safety/video events, coaching or review status, crash/collision/distracted-driving categories, panic alerts, emergency banners, or similar risk signals
- `map_list_trip_status`: map/list/trip/history status cues that carry operational state or exception meaning, such as stale, not communicating, out of coverage, EV charging, GPS quality, or source/status markers

For each signal, state the platform/vendor, product or surface, family label, signal name, trigger or condition, UI cue description, lifecycle/status or recoverability detail, source name/type/date, checked date, official-vs-third-party stance, caveat state, and a short confidence rationale.

Strong sources are official help/support/product pages, release notes, public manuals, and other public vendor-controlled documentation that names the signal or its meaning. Each URL should be appropriate as standalone evidence for the submitted signal. App-store listings, public product pages, public videos, and third-party screenshots can support surface visibility when their limits are explicit, but screenshot-only evidence without a public semantic definition should be low confidence. Public registries, directories, app catalogs, certification lists, and other source hubs can help discover or corroborate platforms, but they should not be used as the only evidence for a signal when they mainly repeat platform metadata, regulatory code lists, self-certification text, or generic feature semantics. A source-hub page can carry a signal row only when the cited page has distinct, platform-specific UI-signal semantics for that row, not a templated body of generic codes or capabilities reused across many platforms. Public pages that reference an in-product legend, expose only image labels, or are visibly stale can still be useful when the caveat is stated.

Do not use private dashboards, logged-in customer screenshots, scraped asset files, vendor-review rating icons, procurement comparisons, price/contract commentary, maintenance advice, compliance advice, driver-management recommendations, or subjective design critique.

Requirements:
- The page must tie the submitted signal to the claimed platform or product surface and to an operational state, exception, or important status-change family.
- The page must support the trigger, condition, threshold, or event that causes the signal or status to appear.
- The page must describe, label, or visibly anchor how the operational state is surfaced in the UI through a cue such as an icon, badge, dot, banner, status label, status column, dial/clock, marker, card, or sub-icon.
- The page must expose at least one lifecycle, status, source-quality, or recoverability detail for the signal, such as active/pending state, severity, review state, remaining time, stale/disconnected/current status, displayed duration, source date/staleness, screenshot-only cue, gated legend reference, or similar.

Write one JSON object per line to `results_fleet_telematics_signals.jsonl`:
{"item": { "platform": "<platform>", "signal_family": "<signal_family>", "product_surface": "<product_surface>", "signal_name": "<signal_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
