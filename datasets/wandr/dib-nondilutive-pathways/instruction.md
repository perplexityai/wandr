You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `dib_nondilutive_pathways`
  - `dib_nondilutive_pathways.posting_status`

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

## `dib_nondilutive_pathways`

For each source family listed below, supply at least 3+ distinct `source_channel` values. For each `source_channel`, supply at least 2+ U.S. defense-industrial-base non-dilutive financing or procurement pathways, with an official or source-controlled authority / issuer source (1+ URL per pathway) that supports public provenance for the pathway as of 2026-06-30.

Use these `source_family` labels for the cited authority / issuer source surface:
- `agency_program_page`
- `opportunity_assistance_system`
- `statute_regulation_authority`
- `ota_consortium_channel`
- `sbir_sttr_component_surface`
- `credit_finance_program`

A pathway can be a program, opportunity class, solicitation or open announcement, assistance listing, OTA or procurement vehicle, loan or loan-guarantee channel, purchase commitment, challenge / prize, or comparable funding / procurement route when the cited source frames it as a public defense-industrial-base pathway. The source must be controlled by an authorizing body, implementing agency, official opportunity or assistance system, statute / regulation publisher, or source-controlled consortium / OTA channel whose official role is source-stated. Third-party explainers, CRS reports, law-firm or client alerts, trade press, LinkedIn posts, commercial aggregators, and generic market guides do not count as the authority / issuer source.

Treat `source_family` as the surface class of the cited source, not just the sponsor's organization. Treat `source_channel` as the specific official/source-controlled channel for the row: the issuer or source host plus the parent program, solicitation package, vehicle, assistance listing, SBIR/STTR cycle, opportunity surface, statute/regulation surface, or consortium channel. Examples: `xtech.army.mil / xTechSearch 9`, `DIBC / RPP-BES-26-01`, `DARPA / Open BAA HR0011-26-S-0001`, `SAM.gov / solicitation shell`, `Navy SBIR / 25.2 topic PDF`, or `U.S. Code / 10 U.S.C. 4022`.

A source map should be balanced across the listed families and across distinct `source_channel` values inside each family. Many rows from one host, one parent solicitation package, one PDF, one SBIR/STTR cycle, one broad opportunity system, or one statute/regulation surface do not substitute for other source channels. Topic-level SBIR/STTR rows can be valid pathways when source-stated, but multiple topics inside one parent topic package or PDF still share one `source_channel`.

Keep the claim to public, source-stated provenance. Do not turn it into bid advice, legal advice, eligibility determination, procurement recommendation, opportunity ranking, vendor matching, lead scoring, contact enrichment, export-control conclusion, or investment advice. Foreign-supplier posture is optional: include citizenship, ownership / control, domicile, domestic-source, country eligibility, foreign ownership, or foreign-government-control posture only when the cited page explicitly states it; page silence is only a bounded observation about that cited page.

Requirements:
- The `source_family` label must match the cited authority / issuer source surface.
- The `source_channel` must identify a distinct official/source-controlled channel for the row: source host or issuer plus the parent program, package, vehicle, cycle, or opportunity surface. Do not fill a family with repeated rows from the same host, package, PDF, cycle, statutory surface, or broad system shell.
- The page must identify the claimed pathway itself.
- The page must identify the issuer or implementer for the pathway.
- The page must state the instrument type or funded / procured activity.
- The page must state an authorizing authority, authorizing section, statute, regulation, authority basis, or comparable official authorization language.

Write one JSON object per line to `results_dib_nondilutive_pathways.jsonl`:
{"item": { "source_family": "<source_family>", "source_channel": "<source_channel>", "pathway": "<pathway>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `dib_nondilutive_pathways.posting_status`

Cross-tasknode identifier discipline: this task is for the same {= pathway =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For at least {= pathway =}+ U.S. defense-industrial-base non-dilutive financing or procurement pathways, supply an official or source-controlled posting / status source (1+ URL per pathway) that states the pathway's posting or program status as checked against 2026-06-30.

The status source must be an official opportunity page, program page, NOFO, assistance listing, official solicitation or amendment, source-controlled consortium / OTA channel, source-controlled SBIR/STTR component topic page, or comparable official channel. A component-controlled SBIR/STTR topic page can count even when it labels its topic text as an unofficial copy, but a third-party mirror cannot. "Current" does not mean open only: source-stated open, closed, archived, amended, posted, due, archive-date, future offering, on-hold, or comparable status / date context counts when the cited page states it.

Keep the claim to public, source-stated status facts. Do not turn it into bid advice, legal advice, eligibility determination, procurement recommendation, opportunity ranking, vendor matching, lead scoring, contact enrichment, export-control conclusion, or investment advice. Foreign-supplier posture is optional: include citizenship, ownership / control, domicile, domestic-source, country eligibility, foreign ownership, or foreign-government-control posture only when the cited page explicitly states it; page silence is only a bounded observation about that cited page.

Requirements:
- The page must tie the posting or status record to the claimed pathway.
- The page must self-state the pathway's posting or status state.
- The page must provide date context for that status, such as posted date, due date, close date, archive date, amendment date, update date, future-offering timing, or comparable source-stated timing.

Write one JSON object per line to `results_dib_nondilutive_pathways.posting_status.jsonl`:
{"item": { "pathway": "<pathway>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
