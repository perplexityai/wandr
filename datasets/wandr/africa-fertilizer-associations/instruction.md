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

## `africa_fertilizer_associations`

For 35+ African fertilizer or plant-nutrition trade, industry, membership, or professional associations, name public organizational evidence whose source-visible signal or fact is dated or clearly contextualized on or before May 12, 2026 under 3+ evidence roles per association, with 2+ distinct evidence signals per role and 1+ URL for each signal.

Country, region, and continent are evidence-bearing attributes here, not a checklist to fill. National, regional, continental, and sub-sectoral fertilizer / plant-nutrition bodies can all qualify when the source-stated association role is visible. Do not submit absence rows such as `no-association-anchor`, `no-membership-evidence`, or similar missing-state findings.

The May 12, 2026 cutoff applies to the submitted evidence signal or fact. This task does not ask for a separate current-operation finding on the cutoff date; it asks for public organizational evidence whose date or source context places the claimed signal or fact on or before the cutoff.

The evidence roles are:
- `identity_mandate`: public identity, mandate, objectives, or association purpose in fertilizer, plant nutrition, soil-health/fertilizer, or the fertilizer industry
- `geographic_tie`: public tie to Africa, an African region, or one or more African countries
- `constituency_membership`: public evidence of member classes, member organizations, constituency represented, committees, rosters, or member-side acknowledgment
- `governance_secretariat`: public organizational governance or secretariat evidence such as board, officers, committees, secretariat, management, or official organizational roles
- `dated_activity_affiliation`: dateable formation, launch, event, project, affiliation, standards/regulatory engagement, training, consultation, endorsement, or comparable public activity involving the association

Eligible source classes include official association or association-owned pages, association reports, regional or continental association pages, credible institutional or project pages, public news, government or agriculture-sector publications, and member-company pages when they explicitly evidence the association relationship or role. Eligible rows should stay within public organizational evidence. Exclude private contact details, emails, phone numbers, private addresses, people-finder/contact-broker surfaces, outreach utility, lead scoring, supplier rankings, procurement advice, lobbying strategy, and political or personal profiling.

Requirements:
- The page must clearly identify the named association by name or recognizable alias.
- The page must state or plainly substantiate a fertilizer, plant-nutrition, soil-health/fertilizer, or fertilizer-industry association role; crop-protection, pesticide, generic agribusiness, donor-implementation, regulator, data-platform, company, or farmer-federation similarity is not enough by itself.
- The page must tie the association to Africa, an African region, or one or more African countries.
- The page must support the declared evidence role with a concrete public organizational signal matching the submitted `association_evidence_signal`.
- The page must support a cutoff-bounded time basis for the claimed signal or fact: the signal or fact must be dated on or before May 12, 2026, appear in source context published or updated on or before May 12, 2026, or be clearly described by a later page as having occurred or existed on or before May 12, 2026.

Write one JSON object per line to `results_africa_fertilizer_associations.jsonl`:
{"item": { "association": "<association>", "evidence_role": "<evidence_role>", "association_evidence_signal": "<association_evidence_signal>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
