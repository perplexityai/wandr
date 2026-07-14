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

## `aquilon_comic_universe_volumes`

For each of the 126 numbered tomes of the Aquilon shared-fictional-universe imprint listed below — published during 2013-2026 by Soleil Productions across the seven concept-series of the imprint — supply a per-volume archival page. Each page must give the album's calendar release year and scénariste(s) and dessinateur(s) credits. One row per (series, tome) pair.

Per-volume archival surfaces include community comic-database catalog entries, per-volume publisher-authoritative pages, and per-volume reviewer-of-record pages that surface the album's per-volume metadata as discrete fields.

Tomes in scope:

- **Elfes T1**
- **Elfes T2**
- **Elfes T3**
- **Elfes T4**
- **Elfes T5**
- **Elfes T6**
- **Elfes T7**
- **Elfes T8**
- **Elfes T9**
- **Elfes T10**
- **Elfes T11**
- **Elfes T12**
- **Elfes T13**
- **Elfes T14**
- **Elfes T15**
- **Elfes T16**
- **Elfes T17**
- **Elfes T18**
- **Elfes T19**
- **Elfes T20**
- **Elfes T21**
- **Elfes T22**
- **Elfes T23**
- **Elfes T24**
- **Elfes T25**
- **Elfes T26**
- **Elfes T27**
- **Elfes T28**
- **Elfes T29**
- **Elfes T30**
- **Elfes T31**
- **Elfes T32**
- **Elfes T33**
- **Elfes T34**
- **Elfes T35**
- **Nains T1**
- **Nains T2**
- **Nains T3**
- **Nains T4**
- **Nains T5**
- **Nains T6**
- **Nains T7**
- **Nains T8**
- **Nains T9**
- **Nains T10**
- **Nains T11**
- **Nains T12**
- **Nains T13**
- **Nains T14**
- **Nains T15**
- **Nains T16**
- **Nains T17**
- **Nains T18**
- **Nains T19**
- **Nains T20**
- **Nains T21**
- **Nains T22**
- **Nains T23**
- **Nains T24**
- **Nains T25**
- **Nains T26**
- **Orcs et Gobelins T1**
- **Orcs et Gobelins T2**
- **Orcs et Gobelins T3**
- **Orcs et Gobelins T4**
- **Orcs et Gobelins T5**
- **Orcs et Gobelins T6**
- **Orcs et Gobelins T7**
- **Orcs et Gobelins T8**
- **Orcs et Gobelins T9**
- **Orcs et Gobelins T10**
- **Orcs et Gobelins T11**
- **Orcs et Gobelins T12**
- **Orcs et Gobelins T13**
- **Orcs et Gobelins T14**
- **Orcs et Gobelins T15**
- **Orcs et Gobelins T16**
- **Orcs et Gobelins T17**
- **Orcs et Gobelins T18**
- **Orcs et Gobelins T19**
- **Orcs et Gobelins T20**
- **Orcs et Gobelins T21**
- **Orcs et Gobelins T22**
- **Orcs et Gobelins T23**
- **Orcs et Gobelins T24**
- **Orcs et Gobelins T25**
- **Orcs et Gobelins T26**
- **Orcs et Gobelins T27**
- **Orcs et Gobelins T28**
- **Orcs et Gobelins T29**
- **Orcs et Gobelins T30**
- **Orcs et Gobelins T31**
- **Orcs et Gobelins T32**
- **Orcs et Gobelins T33**
- **Mages T1**
- **Mages T2**
- **Mages T3**
- **Mages T4**
- **Mages T5**
- **Mages T6**
- **Mages T7**
- **Mages T8**
- **Mages T9**
- **Mages T10**
- **Mages T11**
- **Mages T12**
- **Mages T13**
- **Mages T14**
- **Terres d'Ogon T1**
- **Terres d'Ogon T2**
- **Terres d'Ogon T3**
- **Terres d'Ogon T4**
- **Terres d'Ogon T5**
- **Terres d'Ogon T6**
- **Terres d'Ogon T7**
- **Terres d'Ogon T8**
- **Terres d'Ynuma T1**
- **Terres d'Ynuma T2**
- **Terres d'Ynuma T3**
- **Terres d'Ynuma T4**
- **Guerres d'Arran T1**
- **Guerres d'Arran T2**
- **Guerres d'Arran T3**
- **Guerres d'Arran T4**
- **Guerres d'Arran T5**
- **Guerres d'Arran T6**

Series-name surface variants — any of these forms refers to the same canonical concept-series, and a per-volume archival page that surfaces the album under any of them is admissible evidence:

- **Elfes** (also known as: Elves, Les Elfes, Terres d'Arran - Elfes, Terres d'Arran : Elfes)
- **Nains** (also known as: Dwarves, Les Nains, Terres d'Arran - Nains)
- **Orcs et Gobelins** (also known as: Orcs & Gobelins, Orcs & Goblins, Orcs and Goblins, Orcs et Goblins, Orks et Gobelins)
- **Mages** (also known as: Les Mages, Terres d'Arran - Mages)
- **Terres d'Ogon** (also known as: Lands of Ogon, Terre d'Ogon, Terres d Ogon)
- **Terres d'Ynuma** (also known as: Lands of Ynuma, Terre d'Ynuma, Terres d Ynuma)
- **Guerres d'Arran** (also known as: Wars of Arran, Guerres d'Arran-Extinction, Guerres d Arran, Guerre d'Arran)

Requirements:

- The page must state the album's calendar release year; a 4-digit year (or year + month) shown as an album-level publication / dépôt-légal value is enough.
- The page must identify both the album's scénariste(s) and dessinateur(s), consistent with the claim.
- The page must focus per-volume on the submitted (series, tome) album as a canonical numbered tome of its concept-series — not a multi-volume retrospective, universe-overview, or supplementary / bundled / special-edition entry.
- The page must communicate (possibly via URL among other things) that it is on a community comic-database catalog surface, a publisher-authoritative surface, or a reviewer-of-record surface.

Write one JSON object per line to `results_aquilon_comic_universe_volumes.jsonl`:
{"item": { "series": "<series>", "tome": "<tome>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
