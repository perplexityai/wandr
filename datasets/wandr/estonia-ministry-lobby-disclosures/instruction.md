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

## `estonia_ministry_lobby_disclosures`

For Estonia's ministry lobby-meeting disclosures, cover each of the 9 listed quarters individually for each of the 11 canonical ministries below, with 1+ official URL per ministry-quarter.

Use the ministry as the institution, not the minister's portfolio. Canonical ministries:
- **Ministry of Education and Research** (also written as: Education and Research Ministry, Haridus- ja Teadusministeerium, HTM)
- **Ministry of Justice and Digital Affairs** (also written as: Ministry of Justice, Justice Ministry, Justice and Digital Affairs Ministry, Justiits- ja Digiministeerium, JDM)
- **Ministry of Defence** (also written as: Defence Ministry, Kaitseministeerium)
- **Ministry of Climate** (also written as: Ministry of the Climate, Climate Ministry, Kliimaministeerium)
- **Ministry of Culture** (also written as: Ministry of Cultural Affairs, Culture Ministry, Kultuuriministeerium)
- **Ministry of Economic Affairs and Communications** (also written as: Economic Affairs and Communications Ministry, Majandus- ja Kommunikatsiooniministeerium, MKM)
- **Ministry of Finance** (also written as: Finance Ministry, Rahandusministeerium)
- **Ministry of Regional Affairs and Agriculture** (also written as: Regional Affairs and Agriculture Ministry, Ministry of Regional Affairs, Ministry of Agriculture, Regionaal- ja Põllumajandusministeerium)
- **Ministry of Social Affairs** (also written as: Social Affairs Ministry, Sotsiaalministeerium)
- **Ministry of the Interior** (also written as: Ministry of Interior, Interior Ministry, Siseministeerium)
- **Ministry of Foreign Affairs** (also written as: Foreign Affairs Ministry, Välisministeerium)

Canonical quarters:
- **2024-Q1**
- **2024-Q2**
- **2024-Q3**
- **2024-Q4**
- **2025-Q1**
- **2025-Q2**
- **2025-Q3**
- **2025-Q4**
- **2026-Q1**

For each ministry-quarter, include a concise disclosure/source-state classification supported by the cited source. Useful states include published meeting entries, an explicit no-disclosable-meetings or no-meetings statement, download/archive-only disclosure, visible update/checked coverage, no visible update date on an otherwise quarter-carrying official source, or an official-source conflict.

Each cited URL must be an official originating-ministry page, official originating-ministry download, or equivalent official ministry-owned archive carrying the claimed ministry's lobby or stakeholder meeting disclosure material in fetched/rendered text. Official originating-ministry downloads are usually the safest evidence. Official originating-ministry pages can also work, but only when the fetched page text itself exposes the claimed quarter's meeting entries, no-meeting statement, or source-state cue. If a ministry page mostly acts as an index, archive, link list, collapsed table, or current-quarter page, cite the direct official XLSX/PDF/download instead of quoting hidden or linked entries from the parent page. Government-wide rule pages, central statistics, and external context can explain the regime, but they should not replace the originating ministry's own runtime-visible disclosure page or download for a ministry-quarter record. Do not make unsupported no-public-portal claims; a negative state needs an official source that anchors it.

Requirements:
- The source must communicate that the disclosure surface or dataset belongs to the claimed ministry or its area of government for lobby/stakeholder meetings.
- The evidence must tie the record to the claimed quarter using a quarter heading, date range, last-updated or checked-through date, file title, meeting dates, or comparable source-level cue.
- The evidence must support the claimed disclosure/source state for that quarter. For published-meeting states, the source should show at least one meeting date in the quarter and enough entry detail to identify a meeting topic plus a lobbyist or represented organization or participating official. For no-meeting states, the official text must explicitly say there were no relevant or disclosable meetings for that quarter.

Write one JSON object per line to `results_estonia_ministry_lobby_disclosures.jsonl`:
{"item": { "ministry": "<ministry>", "quarter": "<quarter>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
