You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `furniture_maker_object_attributions`
  - `furniture_maker_object_attributions.maker_documentation`

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

## `furniture_maker_object_attributions`

For 90+ historical furniture makers or firms, cover each of the 2 object-source roles below by identifying 2+ distinct attributed furniture objects per maker/source role and supplying an object/catalogue source (i.e. 1+ URL per object) that ties the specific object to the maker by page-stated attribution.

Object/catalogue pages ought to be public, text-usable records for specific pieces: museum or public-collection records, historic-house collection records, institutional catalogues, auction-lot pages, or substantive dealer-catalogue pages can qualify when they carry object-specific evidence. Broad biography pages, search results, category pages, appraisal-only summaries, and style-inspiration pages do not qualify by themselves.

The object-source roles of interest, which we refer to as `object_source_type`, are:
- `collection_record`: a museum, historic-house, public-collection, or institutional collection record for the specific object. A V&A Explore the Collections page can qualify here when it carries object-specific evidence.
- `external_object_record`: a public object-specific catalogue or reference source outside V&A's collections domain, such as another museum/public-collection record, historic-house page, auction-lot page, substantive dealer-catalogue page, exhibition catalogue, or comparable object-specific reference passage. V&A collection pages, V&A image pages, and mirrors or direct copies of a V&A record do not qualify here.

Requirements:
- The page should visibly fit the object-source role in scope: for `collection_record`, a public collection, historic-house, or institutional collection-record surface; for `external_object_record`, a non-V&A object-specific catalogue/reference surface whose page context is independent of V&A's collections domain.
- The page must clearly identify the specific object, such as by title, object type, accession or inventory number, lot identifier, house or collection label, date, materials, description, or comparable object-defining details.
- The page must state the attribution relationship between the object and the named maker or firm through maker, designer, manufacturer, cabinetmaker, workshop, "by", "made by", "attributed to", "stamped", "labelled", or comparable page wording. A page that only says "style of", "manner of", "after", "school of", or generic inspiration without attributing the specific object to the maker does not satisfy this requirement.
- The page must tie the object to a public object context, such as a museum or collection record, historic house, accession/inventory entry, exhibition catalogue, sale or lot page, or substantive dealer catalogue record.

Write one JSON object per line to `results_furniture_maker_object_attributions.jsonl`:
{"item": { "maker": "<maker>", "object_source_type": "<object_source_type>", "object": "<object>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `furniture_maker_object_attributions.maker_documentation`

Cross-tasknode identifier discipline: this task is for the same {= maker =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= maker =}+ historical furniture makers or firms, supply a documentation source per maker (i.e. 1+ URL) that identifies the maker or firm as part of the British or Irish furniture trade and gives a concrete working anchor.

Documentation pages ought to be public and text-usable with maker-specific historical content. Biographical/reference pages, institutional maker pages, museum maker biographies, dictionary entries, society or local-history pages, trade-directory entries, guild/company records, and comparable source-derived career passages can qualify. Broad search/list pages, bibliographies without a maker passage, preview-only records with no maker-specific passage, and object pages that only name the maker without a working anchor do not qualify.

Requirements:
- The page must clearly identify the named maker or firm as a furniture-trade entity, such as a cabinetmaker, furniture maker, chairmaker, upholsterer, upholder, inlayer, carver/gilder, workshop, partnership, manufacturer, or comparable trade role.
- The page must tie the maker or firm to Britain or Ireland through place, address, firm history, training, work, trade-directory context, institutional framing, or comparable historical context.
- The page must give a concrete working anchor, such as dates, place of work, trade role, apprenticeship, partnership, firm history, directory entry, commission, labelled/stamped work, or source-derived career context.

Write one JSON object per line to `results_furniture_maker_object_attributions.maker_documentation.jsonl`:
{"item": { "maker": "<maker>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
