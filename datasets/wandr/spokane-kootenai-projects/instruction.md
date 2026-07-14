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

## `spokane_kootenai_projects`

For each of the 2 counties listed below, cover 7+ lead agencies or jurisdictions per county; for each lead agency, cover 6+ canonical transportation or street-integrated public works capital projects; for each canonical project, cover 3+ distinct official source-claim families; for each source-claim family, supply 1+ official public source-claim URL focused on the 2026-2032 planning/programming period.

Target counties:
- **Spokane County, Washington**
- **Kootenai County, Idaho**

A canonical project is the smallest official project, stage, package, or capital item with its own identifiable scope and at least one official budget, phase, schedule, project ID, PIN, key number, contract, award, or project page. Umbrella corridors, long-range initiatives, and broad programs can be parent context, but they should not be double-counted as standalone projects unless an official source treats the umbrella itself as the funded deliverable. Generic maintenance categories count only when the source gives project-level scope, location, schedule, budget, or identifier detail.

Each source-claim family is a materially distinct official source role or surface for the canonical project, and each URL is one source claim inside that family. Public agency pages, adopted or draft programming documents, public budgets, public project pages, transit capital materials, official meeting or board records, official contract records, and similar public-source surfaces can all count when they make a project-level claim. News, trade, campaign, advocacy, vendor, plan-room, and private bid-intelligence pages may help discovery but do not carry the primary evidence here.

Parent TIP, STIP/ITIP, call-for-projects, regional program, amendment, and master-program sources are useful, but they count as one parent-program source family for a canonical project. A strong source set for the same project should combine that family with meaningfully different official surfaces when available, such as a project-specific page, lead-agency budget or CIP page, board/council packet, contract or award record, construction update, transit capital page, state DOT project page, or comparable independent official source. Two rows, PDFs, amendments, or table views from the same parent program context are not two source-claim families for the same project.

For downstream ledger usefulness, preserve source-specific names and fields rather than smoothing them away: source family, source status, source period, source date when visible, checked date, project name as written, costs and budget basis, phase/status, dates, funding, sponsor, identifiers, location limits, and missing/conflict flags. Checked date and confidence are auxiliary ledger metadata; source-specific project facts still need page evidence.

This is factual public-source reconciliation only. Exclude investment prioritization, bid strategy, contractor targeting, procurement advice, policy advocacy, real-estate inference, or unsupported extrapolation from planning-only records.

Requirements:
- The page must communicate official public-source status for the cited project claim.
- The page must identify the claimed capital project, stage, package, or project item and tie it to the submitted county and lead agency, sponsor, corridor, jurisdiction, or geography.
- The page must represent the submitted source-claim family as a distinct official source role or surface for this project; parent program/list/table pages count only as that parent-program family, not as a separate project-specific, lead-agency, budget, board, contract, or construction source family.
- The page must provide source-specific project-claim detail: the source's project name plus useful fields such as cost, budget basis, phase, dates, funding, sponsor, project ID/PIN/key number, scope, location limits, or contract/award fields.
- The submitted source claim must distinguish lifecycle, source-period, source-status, and money/budget interpretation where the page makes those visible, including draft/adopted/amended status, plan-only/programmed/funded/construction/completed/unknown state, total cost versus phase/programmed-year/grant/local-match/source-period dollars, and explicit missing or unknown fields.
- Contractor or award claims must come from an official award, contract, bid-tabulation, board-action, or equivalent agency record. Bid notices, solicitations, plan-room pages, and contractor outreach pages support only advertised/no-official-award/unknown states.

Write one JSON object per line to `results_spokane_kootenai_projects.jsonl`:
{"item": { "county": "<county>", "lead_agency": "<lead_agency>", "project": "<project>", "source_family": "<source_family>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
