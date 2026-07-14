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

## `benefits_policy_sources`

For each of the 56 U.S. jurisdictions listed below and each of the 5 assistance-program categories, supply 1+ source URLs per jurisdiction-program pair. A qualifying URL points to an official public page that communicates the current operative policy source, official program-status source, or official program-scope source for that category in that jurisdiction.

Useful context for each source includes the source type, source status, and any visible version, revision, effective, update, or plan-year date. A source need not literally be called a manual: a delegated official policy system, live administrative-code surface, agency state plan, or official federal host carrying jurisdiction-specific official material can count when it is the public operative provision source. When no current public manual/source is publicly documented for a pair, or when the program is not operated, an official status page or program-specific exhaustive official jurisdiction list, statute, or rule can count only if it states that status, identifies the operative substitute, or makes the jurisdiction's omission from the operated-program scope clear.

Target jurisdictions:
- **Alabama**
- **Alaska**
- **Arizona**
- **Arkansas**
- **California**
- **Colorado**
- **Connecticut**
- **Delaware**
- **District of Columbia**
- **Florida**
- **Georgia**
- **Hawaii**
- **Idaho**
- **Illinois**
- **Indiana**
- **Iowa**
- **Kansas**
- **Kentucky**
- **Louisiana**
- **Maine**
- **Maryland**
- **Massachusetts**
- **Michigan**
- **Minnesota**
- **Mississippi**
- **Missouri**
- **Montana**
- **Nebraska**
- **Nevada**
- **New Hampshire**
- **New Jersey**
- **New Mexico**
- **New York**
- **North Carolina**
- **North Dakota**
- **Ohio**
- **Oklahoma**
- **Oregon**
- **Pennsylvania**
- **Rhode Island**
- **South Carolina**
- **South Dakota**
- **Tennessee**
- **Texas**
- **Utah**
- **Vermont**
- **Virginia**
- **Washington**
- **West Virginia**
- **Wisconsin**
- **Wyoming**
- **American Samoa**
- **Guam**
- **Northern Mariana Islands**
- **Puerto Rico**
- **U.S. Virgin Islands**

Assistance-program categories:
- **nutrition assistance**: SNAP or the jurisdiction's official nutrition-assistance counterpart, including territorial Nutrition Assistance Program equivalents where SNAP is not operated under that name.
- **cash assistance**: TANF, Temporary Assistance, or the jurisdiction's official family cash assistance program.
- **medical assistance**: Medicaid eligibility policy, including integrated Medicaid / CHIP policy sources when that is how the jurisdiction publishes the rules.
- **child care assistance**: CCDF child care subsidy / child care assistance eligibility and administration policy.
- **energy assistance**: LIHEAP / low-income home energy assistance policy, state plan, or equivalent official program source.

Requirements:
- The page must tie the source to the named jurisdiction and to the named assistance-program category. For official exhaustive program-scope sources, omission of the named jurisdiction can carry the jurisdiction tie when the page clearly defines the complete operated-program scope.
- The page must communicate official authority for the source: a state, territory, or District agency; delegated official policy/manual system; official administrative-rule or code publisher; or a federal USDA/FNS, ACF, CMS, or comparable host carrying jurisdiction-specific official material.
- The page must identify or contain operative eligibility, benefits, casework, administrative, state-plan, or rule provisions for the program; an official current-status statement for that program category; or a program-specific exhaustive official scope source establishing that the jurisdiction is outside the operated-program scope. Consumer application pages, outreach summaries, news releases, legal-aid mirrors, advocacy explainers, and commercial tool pages do not count by themselves.
- The page must expose a current-source status signal: visible revision/effective/update date, current plan or manual year, current-through rule status, current policy-system framing, or explicit official framing that no current public manual/source exists, the program is not operated, the operative substitute is a rule, plan, or other public provision source, or the jurisdiction is outside the program's current official scope.

Write one JSON object per line to `results_benefits_policy_sources.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "assistance_program": "<assistance_program>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
