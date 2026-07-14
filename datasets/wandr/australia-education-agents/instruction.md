You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `australia_education_agents`
  - `australia_education_agents.education_agencies_eligibility`

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

## `australia_education_agents`

For each of the 8 countries below, identify 6+ country-agency entities as educational service providers publicly recruiting or advising students from the named country for Australian education, with 2 kinds of corroborating sources provided (1+ URL per kind) — to cover each side of the relation.

Countries:
- **China**
- **India**
- **Nepal**
- **Indonesia**
- **Malaysia**
- **Philippines**
- **Sri Lanka**
- **Brazil**

Source kinds:
- `origin`: tied to the origin country and the agency itself
- `destination`: tied to Australia and the recipient institution(s)

Target pages differ by source kind: for `origin`, the page should be anchored in the named country and tied to the agency — the agency's own origin-country site, an origin-country sector news / forum / accreditation profile, or an origin-country regulator / association listing — recognizable, for instance, through origin-country TLDs, origin-language content, origin-country addresses, or local accreditation marks; for `destination`, the page should be an agency-recognizing source signaling the Australian-counterpart / -overseer / -(equivalent) nature of it — an Australian university / provider find-an-agent page, a public-sector registered-agent listing such as Austrade or PIER, a state-government education directorate, an Australian embassy education page, relevant Australian-side sector-news article, etc. — similarly, could be recognizable among other things through TLDs, CRICOS codes, letterheads, and so on.

Requirements:
- The page must clearly identify the named agency and a concrete counterparty.
- The page must clearly support the intended country-and-role binding for both parties: the counterparty as an Australia-based institution, the agency as an educational recruitment / advisory entity conducting to-institution student transfers.
- The page should provide enough substantive content per the source kind: for `origin`, concretely named Australia-bound activity attached to the agency in the origin country (for instance, counselling, application processing, scholarship advisory, visa support, pre-departure programs, named partnerships with Australian institutions, ...); for `destination`, recipient-side recognition specifics for the named agency (for instance, classification or qualifying notes on a registered-agent listing); both in contrast to in-passing mentions, bulk-aggregator rosters, boilerplates naming the agency without exhibiting any involvement, and so on.

Write one JSON object per line to `results_australia_education_agents.jsonl`:
{"item": { "country": "<country>", "agency": "<agency>", "source_side": "<source_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `australia_education_agents.education_agencies_eligibility`

Cross-tasknode identifier discipline: this task is for the same {= country_agency =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= country_agency =}+ country-agency entities, supply endorsement-evidence across each of the 2 flavors below, providing 2+ corroborating URLs per flavor.

Endorsement flavors:
- `scale_signal`: size / footprint / network / market recognition
- `community_feedback`: client-side / third-party assessments; accounts of what working with the agency is like from people not commercially aligned with the agency

Target pages differ by endorsement flavor: for `scale_signal`, agency-owned surfaces are acceptable, while `community_feedback` should come from independent ones such as consumer-review or independent expert-community / profile platforms, forum threads, sector-news outlets and so on.

Requirements:
- The page must clearly identify the named agency and its operation in the named country.
- The page should provide substantive evidence: for `scale_signal`, an agency-anchored factoid with concrete texture (not vague "leading agency" boilerplate); for `community_feedback`, a developed account with real texture about the agency (not a thin blurb or one-line rating); both in contrast to in-passing mentions, listing memberships, renders in barebones compilations, or pages that name the agency without exposing concrete content.

Write one JSON object per line to `results_australia_education_agents.education_agencies_eligibility.jsonl`:
{"item": { "country": "<country>", "agency": "<agency>", "endorsement_flavor": "<endorsement_flavor>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
