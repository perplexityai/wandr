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

## `industrial_air_controls`

As of April 28, 2026, for 200+ U.S. industrial manufacturer or processor operations, name the company and public facility/location scope, then supply 1+ documented industrial air-control instance and 1+ public URL for that instance.

Each record should be public provenance only: a named U.S. company/facility or unambiguous official corporate source, a source-stated industrial process that produces dust, fumes, mist, smoke, particulate, combustible dust, or a comparable air burden, and a source-stated control/project/equipment/permit signal. Useful records can come from official company pages or reports, sustainability reports, facility pages, public air permits or technical support documents, named-customer vendor case studies, reputable trade press, or project press releases. Anonymous customer cases, generic vendor application pages, market reports, manufacturer directories, SEO lead/contact databases, rankings, outreach/procurement pages, and pages that merely imply a possible need do not count.

The work is a public evidence dossier, not a target list, recommendation, compliance assessment, contact hunt, or procurement analysis. Prefer breadth across industrial segments and source families, and avoid letting one end-user company or one publisher dominate the table. Across the dossier, use at least 50 distinct source domains when enough public evidence is available; do not satisfy the volume mostly from a single vendor, permit repository, trade publication, or end-user company. If a source is company-wide rather than facility-specific, use the public U.S. operating scope the source actually supports.

Concise row notes on industrial segment, source class, visible source date, process evidence, control/project evidence, and scope caveats are useful. Company size, revenue, contacts, rankings, prospecting priority, and inferred operational needs are not needed.

Requirements:
- The page must clearly identify the named company/facility, or an unambiguous official corporate source, and tie it to a U.S. industrial operation.
- The page must state or directly describe the relevant manufacturing or processing activity and its dust, fume, mist, smoke, particulate, combustible-dust, or comparable industrial air burden.
- The page must state a documented control, project, equipment, permit device, or ventilation/filtration signal, such as a baghouse, dust collector, cartridge collector, fume extractor, scrubber, cyclone, mist collector, filtered exhaust system, or comparable air-control device.
- The process burden and air-control signal must belong to the same named company/facility or official corporate operation.

Write one JSON object per line to `results_industrial_air_controls.jsonl`:
{"item": { "company": "<company>", "facility_location": "<facility_location>", "control_instance": "<control_instance>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
