You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `australia_philanthropic_giving_event_provenance`
  - `australia_philanthropic_giving_event_provenance.giving_vehicle_identity`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `australia_philanthropic_giving_event_provenance`

For 34+ giving vehicles, identify 1+ dated public giving events per vehicle within January 1, 2020 through April 23, 2026; for each event and each of the 2 evidence sides below, supply a public provenance source (i.e. 1+ URL per side).

This is a public giving-provenance task, not a ranked donor list, grant-seeking guide, outreach/contact collection task, private-wealth profile, religious-targeting task, or fundraising recommendation.

The evidence sides of interest, which we refer to as `evidence_side`, are:
- `funder_record`: a funder-controlled record from `giving_vehicle` naming the giving event.
- `non_funder_record`: a public record not controlled by `giving_vehicle` that independently names or reports the same support.

Giving events should be source-stated public-benefit philanthropy in arts, culture, music, media, heritage, education, theological education, faith/community activity, or adjacent public-benefit activity. Government grant programs do not count as giving vehicles; amounts can help when public but are not required.

Requirements:
- The page should communicate the source role appropriate to `evidence_side`: for `funder_record`, a funder-controlled giving surface such as an annual report, grants database, official grant/program page, or foundation/trust announcement; for `non_funder_record`, a non-funder public surface such as a recipient/grantee page, recipient annual report, charity report, reputable philanthropy article, public award page, or comparable source.
- The page must identify the claimed giving vehicle and the claimed recipient, program, initiative, or gift surface enough to bind the page to the submitted giving event.
- The page must describe actual philanthropic support by the vehicle, such as a grant, gift, fellowship, award, donation, funded program, commissioned support, named funding stream, or comparable public-benefit giving.
- The page must date or report the giving event within January 1, 2020 through April 23, 2026 through a grant year, award year, annual-report period, announcement date, reporting period, or equivalent event timing.
- The page must tie the giving event to a source-stated public-benefit area or funded activity, not merely infer relevance from the donor's identity or presumed interests.

Write one JSON object per line to `results_australia_philanthropic_giving_event_provenance.jsonl`:
{"item": { "giving_vehicle": "<giving_vehicle>", "recipient_or_program": "<recipient_or_program>", "gift_or_program": "<gift_or_program>", "year": "<year>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `australia_philanthropic_giving_event_provenance.giving_vehicle_identity`

Cross-tasknode identifier discipline: this task is for the same {= giving_vehicle =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= giving_vehicle =}+ giving vehicles, supply a public identity source (i.e. 1+ URL) establishing each as an Australian philanthropic giving vehicle or source-presented public donor.

This identity evidence is about public philanthropic standing, not private wealth, outreach potential, contact collection, donor ranking, grant-application strategy, or fundraising recommendations.

Giving vehicles can include foundations, charitable trusts, PAFs/PuAFs, community or corporate foundations, donor funds, bequests/funds, and named individual donors where public sources frame the person as the giving actor. Government grant programs, recipient charities acting only as recipients, generic donation platforms, ranked prospect entries, and private-wealth profiles are outside scope.

Requirements:
- The page must identify the claimed giving vehicle by name or clear alias.
- The page must tie the vehicle to Australia through registration, governance, location, operating focus, Australian recipients/programs, ACNC status, or comparable Australian public context.
- The page must communicate a philanthropic giving or charitable grantmaking role.
- The page should communicate why it is a credible identity source, such as official vehicle control, charity-register standing, governance or annual-report context, or reputable public philanthropy-profile framing.

Write one JSON object per line to `results_australia_philanthropic_giving_event_provenance.giving_vehicle_identity.jsonl`:
{"item": { "giving_vehicle": "<giving_vehicle>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
