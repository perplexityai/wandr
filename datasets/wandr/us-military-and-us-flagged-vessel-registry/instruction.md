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

## `us_military_and_us_flagged_vessel_registry`

For each of the 14 public U.S. vessel-registry panels below, name 50+ individual vessels and supply at least 1 stable public fact with 1 URL per vessel.

This is a fleet-registry and maritime-market dataset, not a tracking task. Use stable public facts such as owner / service / operator, public homeport when a panel asks for it, class / type, and commissioning / delivery / built date or year. Do not use live AIS, current-position trackers, deployment tracking, readiness claims, exact present location, crew rosters, or private/security-sensitive details.

Public vessel-registry panels:
- **Commissioned U.S. Navy ships - public service or command facts** -- commissioned Navy ships with public vessel or fleet documentation stating the service branch, command, owning program, or similar fleet organization
- **Commissioned U.S. Navy ships - public homeport facts** -- commissioned Navy ships with a source-stated public homeport; do not infer homeport from a port call, exercise, or present location
- **Commissioned U.S. Navy ships - class or type facts** -- commissioned Navy ships with a source-stated class, type, designation, or ship category
- **Commissioned U.S. Navy ships - commissioning, delivery, or built facts** -- commissioned Navy ships with a source-stated commissioning, delivery, acceptance, launch, christening, built date, or built year
- **U.S. Coast Guard cutters - public service or command facts** -- named Coast Guard cutters with public vessel or fleet documentation stating service, district, command, operator, or fleet organization
- **U.S. Coast Guard cutters - public homeport facts** -- named Coast Guard cutters with a source-stated public homeport; exclude aircraft, shore units, and small boats not presented as named cutters
- **U.S. Coast Guard cutters - class or type facts** -- named Coast Guard cutters with a source-stated class, type, designation, or cutter category
- **U.S. Coast Guard cutters - commissioning, delivery, or built facts** -- named Coast Guard cutters with a source-stated commissioning, delivery, acceptance, launch, christening, built date, or built year
- **Military Sealift Command ships - public owner or service facts** -- USNS or MSC-controlled ships with public vessel or fleet documentation stating government ownership, service program, command, operator, or controlling fleet organization
- **Military Sealift Command ships - class or type facts** -- USNS or MSC-controlled ships with a source-stated class, type, designation, or ship category
- **Military Sealift Command ships - delivery or built facts** -- USNS or MSC-controlled ships with a source-stated delivery, acceptance, launch, christening, built date, or built year
- **U.S.-flag commercial vessels - public owner or operator facts** -- commercial U.S.-flagged vessels with a source-stated owner, operator, carrier, or controlling fleet organization and explicit U.S.-flag, Jones Act, or equivalent status
- **U.S.-flag commercial vessels - class or type facts** -- commercial U.S.-flagged vessels with a source-stated class, type, designation, or ship category and explicit U.S.-flag, Jones Act, or equivalent status
- **U.S.-flag commercial vessels - delivery or built facts** -- commercial U.S.-flagged vessels with a source-stated delivery, launch, christening, built date, or built year and explicit U.S.-flag, Jones Act, or equivalent status

Strong sources are stable public vessel, registry, inventory, owner / operator, carrier, or shipyard pages that identify the same named vessel and directly state the requested panel fact. Third-party vessel trackers, current-position pages, generic class pages, search-result pages, and pages that do not directly prove the claimed vessel-level U.S. registry status or fact do not count as source URLs for this task.

Requirements:
- The page must identify the same individual vessel, not only a class, program, aircraft, shore unit, fleet command, or different sister ship.
- The page must place the vessel in the claimed public registry panel.
- The page must speak to the kind of public registry fact requested by that panel.
- The page must support the specific fact without stronger claims than the source makes.
- The source must be a stable public registry, fleet, vessel, operator, shipyard, or official page, not live tracking or current-position content.

Write one JSON object per line to `results_us_military_and_us_flagged_vessel_registry.jsonl`:
{"item": { "registry_panel": "<registry_panel>", "vessel_name": "<vessel_name>", "fact": "<fact>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
