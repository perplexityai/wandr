You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `polish_energy_project_relationship_evidence`
  - `polish_energy_project_relationship_evidence.independent_project_relationship_evidence`

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

## `polish_energy_project_relationship_evidence`

For 100+ companies, name 1+ Polish energy or energy-infrastructure project per company where the company has a public project role, and supply a company-authored or company-attributed relationship source for each such (`company`, `project`) pair (i.e. 1+ URL).

The useful company-side signal is a project-specific public account from the named company itself, rather than a market-status table, generic footprint page, or lead list.

The project should be a named energy or energy-infrastructure project tied to Poland, including electricity generation, gas, heat, offshore wind, renewable power, grid/transmission, storage, industrial-energy, port/terminal, or comparable infrastructure. Broad market presence, generic technology categories, company footprints without a named project, and project aliases that merely rename the same asset are not separate project relationships.

Requirements:
- The page should communicate official control or clear attribution by `company`.
- The page must identify `company` as the company in scope.
- The page must identify the named project and tie it to Poland through location, project framing, owner/operator context, Polish grid/market context, or comparable project-specific wording.
- The page should substantiate `company`'s role or relationship in the project through a company-authored or company-attributed project-specific role description.

Write one JSON object per line to `results_polish_energy_project_relationship_evidence.jsonl`:
{"item": { "company": "<company>", "project": "<project>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `polish_energy_project_relationship_evidence.independent_project_relationship_evidence`

Cross-tasknode identifier discipline: this task is for the same {= company_project =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= company_project =}+ named company/project relationships involving Polish energy or energy-infrastructure projects, supply an independent project-side acknowledgment source for each (`company`, `project`) relationship (i.e. 1+ URL).

The independent side is a project-owner, governing, financing, public-authority, customer/offtaker, tender/procurement, or direct-contract side of the relationship, independent from `company`, such as an owner, SPV, joint-venture partner, grid/transmission operator, financier or DFI, tender/procurement issuer, public issuer, regulator or project authority, direct customer/offtaker, or comparable project-side body.

The project should be a named energy or energy-infrastructure project tied to Poland, including electricity generation, gas, heat, offshore wind, renewable power, grid/transmission, storage, industrial-energy, port/terminal, or comparable infrastructure. Broad market presence, generic technology categories, company footprints without a named project, and project aliases that merely rename the same asset are not separate project relationships.

Requirements:
- The page should communicate official, institutional, or project-party attribution from a project-owner, governing, financing, public-authority, customer/offtaker, tender/procurement, or direct-contract side independent from `company`. Generic trade articles, market summaries, peer supplier or contractor self-descriptions, logo walls, and passing list mentions typically do not carry independent project-side attribution unless the page itself exposes focused project-owner, project-governing, financing, public-authority, customer/offtaker, tender/procurement, or direct-contract acknowledgment of the relationship.
- The page must identify `company` as the company in scope.
- The page must identify the named project and tie it to Poland through location, project framing, owner/operator context, Polish grid/market context, or comparable project-specific wording.
- The page should substantiate `company`'s role or relationship in the project through a focused project-side decision, contract, work package, ownership or financing stake, authority/customer/offtake/tender action, or comparable relationship-specific item for `company`, not merely a reusable construction overview, participant roster, broad list, or progress page that happens to name `company`.

Write one JSON object per line to `results_polish_energy_project_relationship_evidence.independent_project_relationship_evidence.jsonl`:
{"item": { "company": "<company>", "project": "<project>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
