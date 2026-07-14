You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `perplexity_elite_schools`
  - `perplexity_elite_schools.school_authorized_affiliation`

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

## `perplexity_elite_schools`

For each of the 19 schools listed below, supply 2+ (school, person) pairs (i.e. 1+ URL per pair) with a personal page URL whose content shows the named person graduated from the school and currently works at Perplexity AI (profiles, personal academic pages, lab affiliation pages, self-hosted bio pages all count as long as both the graduation and the current Perplexity employment are explicit).

Schools in scope (canonical name — accepted aliases):
- **Harvard** — Harvard University, Harvard College, Harvard Business School, Harvard Medical School, Harvard Kennedy School, Harvard Law, Harvard SEAS
- **MIT** — Massachusetts Institute of Technology, MIT Sloan, MIT Media Lab, MIT CSAIL, MIT EECS
- **Stanford** — Stanford University, Stanford GSB, Stanford Law, Stanford School of Engineering, SAIL
- **Berkeley** — UC Berkeley, University of California Berkeley, Berkeley Haas, Berkeley Engineering, Berkeley EECS
- **Yale** — Yale University, Yale College, Yale SOM, Yale Law
- **Princeton** — Princeton University, Princeton SEAS
- **UPenn** — University of Pennsylvania, Penn, Wharton, Penn Engineering, Penn Law
- **Brown** — Brown University
- **Caltech** — California Institute of Technology
- **UChicago** — University of Chicago, Booth, UChicago Law
- **CMU** — Carnegie Mellon University, CMU SCS, Tepper, CMU Robotics Institute
- **UW** — University of Washington, Allen School, UW Foster
- **Cornell** — Cornell University, Cornell Tech, Cornell Engineering, Cornell Bowers CIS
- **GeorgiaTech** — Georgia Tech, Georgia Institute of Technology
- **Michigan** — University of Michigan, UMich, Ross, Michigan Engineering
- **Northwestern** — Northwestern University, Kellogg, McCormick, Medill
- **UTAustin** — University of Texas at Austin, UT Austin, McCombs
- **UCLA** — University of California Los Angeles, Anderson, UCLA Engineering
- **Purdue** — Purdue University, Purdue ECE, Purdue CS

Requirements:
- The page must show that the person graduated from the named school (degree designation, graduation year, or alumnus framing) — employment at the school without graduation does NOT count.
- The page must show Perplexity (or "Perplexity AI") as the person's active primary current employment — not a permanent honorary designation when the actual primary role is elsewhere, not a non-employment program (fellowship / ambassador / affiliate / etc.), not an ended tenure.

Write one JSON object per line to `results_perplexity_elite_schools.jsonl`:
{"item": { "school": "<school>", "person": "<person>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `perplexity_elite_schools.school_authorized_affiliation`

Cross-tasknode identifier discipline: this task is for the same {= school_person =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= school_person =}+ (school, person) pairs from the schools listed below (i.e. 1+ URL per pair), supply a URL pointing to a page that is officially affiliated with the named school AND substantively mentions the named person.

Schools in scope (canonical name — accepted aliases):
- **Harvard** — Harvard University, Harvard College, Harvard Business School, Harvard Medical School, Harvard Kennedy School, Harvard Law, Harvard SEAS
- **MIT** — Massachusetts Institute of Technology, MIT Sloan, MIT Media Lab, MIT CSAIL, MIT EECS
- **Stanford** — Stanford University, Stanford GSB, Stanford Law, Stanford School of Engineering, SAIL
- **Berkeley** — UC Berkeley, University of California Berkeley, Berkeley Haas, Berkeley Engineering, Berkeley EECS
- **Yale** — Yale University, Yale College, Yale SOM, Yale Law
- **Princeton** — Princeton University, Princeton SEAS
- **UPenn** — University of Pennsylvania, Penn, Wharton, Penn Engineering, Penn Law
- **Brown** — Brown University
- **Caltech** — California Institute of Technology
- **UChicago** — University of Chicago, Booth, UChicago Law
- **CMU** — Carnegie Mellon University, CMU SCS, Tepper, CMU Robotics Institute
- **UW** — University of Washington, Allen School, UW Foster
- **Cornell** — Cornell University, Cornell Tech, Cornell Engineering, Cornell Bowers CIS
- **GeorgiaTech** — Georgia Tech, Georgia Institute of Technology
- **Michigan** — University of Michigan, UMich, Ross, Michigan Engineering
- **Northwestern** — Northwestern University, Kellogg, McCormick, Medill
- **UTAustin** — University of Texas at Austin, UT Austin, McCombs
- **UCLA** — University of California Los Angeles, Anderson, UCLA Engineering
- **Purdue** — Purdue University, Purdue ECE, Purdue CS

Requirements:
- The page must speak with the authority of the named school (incl. via being hosted on a recognizably official-school domain or on a sub-organization the school officially controls). Sub-school / department names listed as aliases above are accepted under their parent institution.
- The named person must be substantively mentioned on the page — a profile, lab role, news subject, project credit, or similar — clearly signalling an eligible person-school relationship.

Write one JSON object per line to `results_perplexity_elite_schools.school_authorized_affiliation.jsonl`:
{"item": { "school": "<school>", "person": "<person>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
