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

## `photo_retail_event_workshops`

For 60+ photo/camera retail ecosystem organizations, supply dated public-event evidence for 2+ distinct customer-facing events, classes, workshops, demos, talks, photowalks, or education sessions per organization within July 1, 2026 through December 31, 2026; each event should be backed by a source (i.e. 1+ URL) that identifies the host's in-scope public event-program role, the event, the date or date range, and event-specific public access context.

The research work is a public-evidence atlas for fragmented camera stores, photo labs, galleries, pro-photo suppliers, brand stores, photo centers, and store/lab/gallery/brand-affiliated education programs, not an event guide, travel plan, outreach list, or registration recommendation.

Hosts ought to be real organizations whose public event identity is tied to a camera/photo retailer, photo lab or print lab, pro-photo supplier or rental house, brand store or showroom, photo gallery or center, or an affiliated customer-education program. Standalone photographer brands, destination photo-tour or travel-workshop operators, generic arts organizers, broad event platforms, ordinary venues, and event promoters are out of scope unless the cited page visibly ties the event to an in-scope retail, lab, gallery, supplier, brand-store, or photo-center program surface. Official host pages and official event-specific registration or social/event pages are the cleanest sources; secondary listings can work only when the page is event-specific, source-labeled, and states the facts it is used for. Generic event directories, organizer-profile pages, recommendation listicles, travel pages, product pages, contact/outreach pages, stale calendars with no target-period occurrence, and inferred recurrence are out of scope.

Requirements:
- The page must identify the named host as the event host, organizer, venue, official registration owner, or otherwise visibly authorized source for the event, and it must show the host's in-scope public photo/camera retail, lab, gallery/center, brand/supplier, or affiliated education-program role.
- The page must identify the named event, class, workshop, demo, talk, photowalk, or session as a distinct offering with event-specific detail, rather than just a generic calendar, organizer profile, category page, or one-line hub listing.
- The page must state a date, date range, session date, or recurring/session framing that places the event within July 1, 2026 through December 31, 2026.
- The page must show photo/camera/imaging customer-facing substance, such as camera technique, photography education, printing or lab work, gear demo, photowalk, critique, artist talk, gallery program, or comparable imaging content.
- The page must show at least two event-specific access, format, status, or program-detail cues such as venue, online/in-person format, time of day, registration or ticketing path, price/free status, sold-out/cancelled/waitlist status, capacity, recurring/session framing, course sequence, named instructor, or brand partner.

Write one JSON object per line to `results_photo_retail_event_workshops.jsonl`:
{"item": { "host_org": "<host_org>", "event_name": "<event_name>", "event_date_or_period": "<event_date_or_period>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
