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

## `olympic_medal_revocations`

For 80+ Olympic medal-stripping cases — `(athlete, event, games)` tuples where the IOC, CAS, or an International Federation formally stripped a medal — supply 2 evidence entries per case (1+ URL per entry): one establishing the disqualification facts (substance or reason and stripping date) and one establishing the reallocation outcome (who got upgraded, or that the medal was vacated).

Each case requires two complementary evidence directions, which we refer to as `evidence_type`; these are:

- `disqualification_facts`: the page must document both the substance (or non-doping reason) and the stripping date (year minimum, month preferred). Per-athlete biographical references, per-event-at-Olympics references, sports trade press, anti-doping decision documents, sports arbitration decisions, IOC primary documents, etc. all count.
- `reallocation_outcome`: the page must either name at least one upgraded medalist with their new medal color or explicitly state the medal was vacated (not reallocated). Per-athlete biographical references, per-event-at-Olympics references, sports trade press, anti-doping decision documents, sports arbitration decisions, IOC primary documents, etc. all qualify; trade press is often where the upgrade chain is documented in full.

Each `(athlete, event, games)` tuple must reference a real Olympic Games (Summer 1896-2024 or Winter 1924-2022), a recognizable athlete name, and a real event of those Games. For team-event medals where a single offending member was named, the athlete name may identify that individual or the team's country / team designation.

Requirements:
- The page must document a formal stripping decision by the IOC, CAS, or the relevant International Federation — not a voluntary return or an unfinalized case.
- The case ought to reflect the current state — if a CAS overturning subsequently restored the medal, that case isn't currently stripped and shouldn't be claimed. (Reversals too recent to be anticipated are fine.)
- The page must carry the substance for that entry's evidence type — for `disqualification_facts`, both the substance / reason AND the stripping date; for `reallocation_outcome`, at least one upgraded medalist (with new medal color) OR explicit vacancy.

Write one JSON object per line to `results_olympic_medal_revocations.jsonl`:
{"item": { "athlete": "<athlete>", "event": "<event>", "games": "<games>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
