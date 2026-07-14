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

## `virginia_k12_districts`

For each of the 68 divisions listed below, cover each of the 3 contact facets listed below by supplying a source (1 URL per facet) that exposes the facet's contact datum scoped to that division and carried on a page belonging to the division's own official web presence.

The goal is a downloadable contact sheet for the larger Virginia public K-12 school divisions — the central web address, mailing/physical address, and main phone number for each.

Divisions in scope:
- **Fairfax County Public Schools**
- **Prince William County Public Schools**
- **Loudoun County Public Schools**
- **Virginia Beach City Public Schools**
- **Chesterfield County Public Schools**
- **Henrico County Public Schools**
- **Chesapeake City Public Schools**
- **Stafford County Public Schools**
- **Arlington County Public Schools**
- **Norfolk City Public Schools**
- **Newport News City Public Schools**
- **Spotsylvania County Public Schools**
- **Richmond City Public Schools**
- **Hampton City Public Schools**
- **Hanover County Public Schools**
- **Alexandria City Public Schools**
- **Suffolk City Public Schools**
- **Frederick County Public Schools**
- **Albemarle County Public Schools**
- **Roanoke County Public Schools**
- **Roanoke City Public Schools**
- **Portsmouth City Public Schools**
- **York County Public Schools**
- **Rockingham County Public Schools**
- **Williamsburg-James City County Public Schools**
- **Fauquier County Public Schools**
- **Augusta County Public Schools**
- **Montgomery County Public Schools**
- **Bedford County Public Schools**
- **Culpeper County Public Schools**
- **Pittsylvania County Public Schools**
- **Campbell County Public Schools**
- **Lynchburg City Public Schools**
- **Manassas City Public Schools**
- **Henry County Public Schools**
- **Washington County Public Schools**
- **Harrisonburg City Public Schools**
- **Franklin County Public Schools**
- **Prince George County Public Schools**
- **Wise County Public Schools**
- **Danville City Public Schools**
- **Shenandoah County Public Schools**
- **Isle of Wight County Public Schools**
- **Tazewell County Public Schools**
- **Louisa County Public Schools**
- **Warren County Public Schools**
- **Gloucester County Public Schools**
- **Orange County Public Schools**
- **Accomack County Public Schools**
- **Halifax County Public Schools**
- **King George County Public Schools**
- **Botetourt County Public Schools**
- **Charlottesville City Public Schools**
- **Caroline County Public Schools**
- **Petersburg City Public Schools**
- **Winchester City Public Schools**
- **Dinwiddie County Public Schools**
- **Powhatan County Public Schools**
- **Scott County Public Schools**
- **Pulaski County Public Schools**
- **Amherst County Public Schools**
- **Hopewell City Public Schools**
- **Smyth County Public Schools**
- **Mecklenburg County Public Schools**
- **Wythe County Public Schools**
- **Fredericksburg City Public Schools**
- **Salem City Public Schools**
- **Radford City Public Schools**

Contact facets:
- `website`: the division's central/official website — its home page or a page on that domain that establishes the domain as the division's primary public web presence.
- `mailing_address`: the street or mailing address of the division's central office / school board office (street or PO box, city or town, and ZIP).
- `main_phone`: the general / main switchboard or central-office telephone number for the division (a published division-wide contact line, not a single school's or an individual staff member's direct line).

Requirements:
- The page must identify the named division as the entity the contact datum belongs to — division name, official logo, or domain identity tying the page to that division, not merely to one of its individual schools or to a county/city government department that is not the school division.
- The page must be on the division's own official web presence — its primary domain or an officially-controlled subdomain or channel; a third-party directory, aggregator listing, ratings site, or news article does NOT count even when it reprints the contact datum.
- The page should expose the facet's contact datum directly and unambiguously. For `website`, the page itself establishes the division's central web domain (the home page or a page whose chrome/navigation identifies the domain as the division's). For `mailing_address`, a complete street or mailing address (street or PO box, locality, and ZIP) for the central office / school board office is shown. For `main_phone`, a published division-level main / switchboard phone number is shown — a single school's number or one staff member's direct extension does NOT count.

Write one JSON object per line to `results_virginia_k12_districts.jsonl`:
{"item": { "district": "<district>", "contact_facet": "<contact_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
