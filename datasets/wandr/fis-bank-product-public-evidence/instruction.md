You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `fis_bank_product_public_evidence`
  - `fis_bank_product_public_evidence.regulated_institution_identity`

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

## `fis_bank_product_public_evidence`

For 5+ canonical FIS banking product families, cover 18+ named U.S. banks or credit unions per product family with 1+ public evidence URL for each institution-product relationship.

The purpose is to map public, source-stated relationships between regulated U.S. depository institutions and selected FIS banking product families. Selection, implementation, conversion, modernization, support, customer-story, and active-use statements can qualify when the relationship status is represented no more strongly than the page supports.

Canonical `fis_product` values:
- `horizon_core`: FIS HORIZON / HORIZON Core Banking System
- `digital_one`: FIS Digital One consumer, retail, online, mobile, or omnichannel banking
- `digital_one_business`: FIS Digital One Business / business eBanking
- `digital_one_commercial`: FIS Digital One Commercial, D1C, or Dragonfly Universal Online Banker
- `code_connect`: FIS Code Connect / CodeConnect
- `affinityedge`: FIS AffinityEdge

Sources should be public, source-stated product evidence. FIS client stories, FIS press or investor releases, institution-owned press releases or filings, institution technology pages, partner case studies, reputable banking media articles, and equivalent primary or near-primary sources can qualify. Secondary customer databases, technographic or lead-generation tables, job postings, LinkedIn or resume text, contractor profiles, app-store metadata, login domains, online-banking redirects, URL guessing, regulator profiles, and generic FIS product pages without customer-specific relationship text are outside scope. Product-name collisions are outside scope: "Horizon Bank" or "First Horizon" does not establish `horizon_core`. Unrelated FIS products or services such as Zelle, NYCE, IBS, card processing, wealth, Glia, nCino, and generic FIS APIs do not establish one of the six canonical product families.

Requirements:
- The page must clearly identify the named bank or credit union.
- The page must name the selected canonical FIS product family or a clear alias for that family.
- The page must directly tie the named institution to the selected FIS product family through customer, selection, conversion, implementation, modernization, use, support, case-story, or equivalent relationship language.

Write one JSON object per line to `results_fis_bank_product_public_evidence.jsonl`:
{"item": { "fis_product": "<fis_product>", "institution_display_name": "<institution_display_name>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `fis_bank_product_public_evidence.regulated_institution_identity`

Cross-tasknode identifier discipline: this task is for the same {= institution =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= institution =}+ named U.S. banks or credit unions, provide 1+ official FDIC-or-NCUA regulator identity anchor per institution, backed by 1+ official regulator URL.

The regulator authority symbols are:
- `fdic`: banks and savings banks insured by the Federal Deposit Insurance Corporation, with FDIC BankFind profile or data surfaces as typical evidence
- `ncua`: credit unions insured or supervised through the National Credit Union Administration, with NCUA credit-union profile, locator, or official data surfaces as typical evidence

Regulator identity evidence substantiates institution identity only, not any FIS product relationship. The page must be an official FDIC or NCUA source: official public FDIC BankFind and NCUA regulator data endpoints can qualify when the response exposes the required identity fields. FIS product pages, institution homepages, press releases, Wikipedia/Wikidata, customer databases, search-result snippets, app stores, LinkedIn or resume text, state regulator pages, wrong-authority profiles, and similarly named but different institutions are outside this identity evidence shape.

Requirements:
- The page must identify the named institution or an official/common alias of it.
- The page must establish the selected regulator authority and that it fits the institution type: `fdic` for banks and savings banks; `ncua` for credit unions.
- The page must expose a stable regulator anchor such as FDIC certificate number, NCUA charter number, active status, official institution name, or official profile/data path.

Write one JSON object per line to `results_fis_bank_product_public_evidence.regulated_institution_identity.jsonl`:
{"item": { "institution_display_name": "<institution_display_name>", "regulator_authority": "<regulator_authority>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
