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

## `food_transport_ops`

For 150+ North American food, grocery, foodservice, convenience, natural/specialty, redistribution, or cold-chain distribution operators, cover 4+ transportation operating-model axes per operator by supplying at least 1+ public URL under each selected axis. KeHE is the seed anchor and should appear somewhere, but the table should move well beyond KeHE and the obvious national head group.

The operating-model axes are:
- `network_footprint`: distribution-center, warehouse, regional coverage, service-area, facility-event, or facility-function evidence.
- `fleet_posture`: private-fleet, dedicated-carriage, vehicle / tractor / trailer scale, driver base, or owned-versus-outsourced transportation posture evidence.
- `registry_signal`: public motor-carrier registry, operating authority, safety, inspection, mileage, cargo, or ranking evidence with its definition visible.
- `cold_chain_control`: temperature-controlled transportation, refrigerated trailer, food-safety, cold-chain certification, monitoring, or product-protection evidence.
- `technology_visibility`: route visibility, telematics, TMS, WMS, warehouse automation, asset tracking, environmental monitoring, or related operations-technology evidence.
- `routing_control`: inbound / outbound routing rules, appointment scheduling, carrier reservation, supplier compliance, route notifications, or document-control evidence.
- `decarbonization`: SmartWay, CNG, EV, electric TRU, charging, alternative-fuel, emissions-target, or transport-energy deployment evidence.
- `logistics_partner`: named dedicated-carriage, 3PL, freight-management, carrier, vendor, or other logistics partner relationship evidence.

The obvious national head group is useful as a starting point, not the whole universe:
- Sysco
- US Foods
- Performance Food Group
- McLane
- UNFI
- KeHE
- C&S Wholesale Grocers
- Gordon Food Service

For each source, report the operator / parent or legal-entity relationship where relevant, distributor archetype, North American geography, operating fact or value, source class, source date or as-of date when visible, checked date, count definition or caveat, and confidence. Use 2026-06-29 as the checked date unless the source was checked later.

Useful public source classes include:
- official company page or press release
- regulator / public registry
- SEC filing or investor disclosure
- private-fleet ranking or trade dataset
- vendor case study or customer story
- trade press or business press
- local government or economic-development announcement
- supplier routing guide, portal page, or public compliance summary
- careers or workforce page
- association, directory, or partner page with entity-specific facts

These source classes are leads, not a closed menu. Direct official, regulatory, filing, or clearly attributed source pages are preferred for identity, network, fleet, and authority claims; vendor, trade, local-government, careers, association, routing, and partner pages are valid when they concretely name the operator and operating-model fact. Lead-generation, procurement advice, generic logistics explainers, rankings without operator-specific support, login-only portals, and gated documents do not count by themselves.

Requirements:
- The page must identify the named operator or a clearly connected parent, segment, legal carrier entity, facility, or logistics arm and tie it to North American food, grocery, foodservice, convenience, natural/specialty, redistribution, or cold-chain distribution.
- The page must fit the submitted `operating_axis`; a source useful for one axis should not be stretched to another axis unless the page actually carries that operating evidence.
- The page must state a concrete public operating-model fact, not merely generic "logistics", "supply chain", service-marketing, or company-about copy.
- The record must preserve the source context: fleet and facility counts should keep their stated definition and date; vendor and trade claims should remain attributed; gated-guide pages should not be used for hidden details; missing public definition or date context should be labeled rather than invented.

Write one JSON object per line to `results_food_transport_ops.jsonl`:
{"item": { "operator": "<operator>", "operating_axis": "<operating_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
