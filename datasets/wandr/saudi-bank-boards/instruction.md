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

## `saudi_bank_boards`

For each of the 10 Saudi Exchange Banks-sector issuers listed below, cover 10+ current board directors per bank; this is not a cap, so include all current directors the official evidence exposes. For each (`bank`, `board_member`) pair, cover each of the 3 official source modes by supplying 1+ URL for that mode.

The purpose is a public board-composition evidence table that checks the same director through different official source families. Gendered evidence is treated as a source-disclosure state, not as an inferred attribute. Names, photos, LinkedIn or social profiles, third-party parity tables, and private biography enrichment do not establish gendered disclosure.

Bank canon, pinned from the Saudi Exchange Banks sector on 2026-06-26:
- **Riyad Bank** (aliases/symbols: 1010, RIBL)
- **Bank Aljazira** (aliases/symbols: 1020, BJAZ, Bank AlJazira, Bank Al-Jazira)
- **Saudi Investment Bank** (aliases/symbols: 1030, SAIB, The Saudi Investment Bank)
- **Banque Saudi Fransi** (aliases/symbols: 1050, BSF, Saudi Fransi Bank)
- **Saudi Awwal Bank** (aliases/symbols: 1060, SAB, SABB, Saudi British Bank, Saudi Awwal)
- **Arab National Bank** (aliases/symbols: 1080, ANB, The Arab National Bank)
- **Al Rajhi Bank** (aliases/symbols: 1120, Alrajhi Bank, Al Rajhi Banking and Investment Corporation)
- **Bank Albilad** (aliases/symbols: 1140, Bank Al Bilad, Albilad)
- **Alinma Bank** (aliases/symbols: 1150, Al Inma Bank)
- **The Saudi National Bank** (aliases/symbols: 1180, SNB, Saudi National Bank, AlAhli, National Commercial Bank, NCB)

Source modes:
- `saudi_exchange_source`: a Saudi Exchange / Tadawul company profile, shareholding/board-information page, issuer announcement, or exchange-hosted issuer filing for the claimed bank. It must identify the director as a current board member using source cues such as designation/classification, board-session dates, appointment/election effective dates, announcement dates, trading dates, or a current company-profile context.
- `issuer_board_page`: a bank-controlled board, leadership, board-committee, investor-relations governance, or individual director page for the claimed bank. It must identify the director as a current board member and give a director-specific board role, committee role, chair/vice-chair office, qualification, or professional-background detail.
- `annual_governance_report`: a bank-controlled annual report, board report, governance report, audit-committee report, or official issuer-filed report PDF for the claimed bank. It must identify the director in board/governance reporting for a current or still-operative board term and give a director-specific board role, committee role, chair/vice-chair office, qualification, or professional-background detail.

For every source mode, the same URL must also support one task-local female-board-representation disclosure state for the named director: an explicit female/woman phrase tied to the director or board role; an official `Ms.` / `Mrs.` honorific tied to the director; or `no_explicit_gendered_signal_on_checked_source` when the checked official director evidence has no female/woman phrase and no `Ms.` / `Mrs.` signal tied to that director. `Mr.`, `H.E.`, `Dr.`, `Eng.`, `Engr.`, and similar male, professional, or generic honorific titles are not positive gendered-disclosure states. They may support only the source-scoped no-signal state by showing that the checked director evidence lacks the allowed female/woman or `Ms.` / `Mrs.` signal. `Ms.` / `Mrs.` honorific-only evidence stays in the honorific tier; do not restate it as an explicit female/woman claim.

Requirements:
- The page must fit the claimed `source_mode`: Saudi Exchange / Tadawul source for `saudi_exchange_source`; bank-controlled board/governance/leadership page for `issuer_board_page`; or bank-controlled or official issuer-filed annual, board, governance, or audit-committee report for `annual_governance_report`. Third-party governance pages, analyst pages, parity trackers, LinkedIn/social profiles, news profiles, generic awards/diversity pages, non-governance financial statements, and non-bank financial-services entities do not count.
- The page must clearly tie the named person to the claimed bank's board. Senior-executive-only entries, committee-only outsiders, generic management pages, and historical directors without current/as-of support do not satisfy the current board-member bar.
- The page must provide board evidence at the bar for the claimed `source_mode`. `saudi_exchange_source` must show current board membership with an exchange/profile/announcement currentness cue. `issuer_board_page` and `annual_governance_report` must show current or still-operative board membership plus a director-specific role/detail beyond a bare name in a roster.
- The page must support the source-scoped gendered-disclosure state for the named director: explicit female/woman phrasing, an official `Ms.` / `Mrs.` honorific, or source-scoped absence of those allowed signals in the checked director evidence. Male, professional, or generic honorific titles alone do not satisfy a positive disclosure state.

Write one JSON object per line to `results_saudi_bank_boards.jsonl`:
{"item": { "bank": "<bank>", "board_member": "<board_member>", "source_mode": "<source_mode>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
