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

## `voss_evanger_place_paths`

For 180+ historical farm/place scopes in the Voss and Evanger source ecology, name the current municipality for each scope and supply 4+ distinct evidence kinds per place, with 1+ public source URL or catalog page per evidence kind. The open place universe should draw from Evanger/Voss core farms, Brekkhus and Teigdalen, former-Evanger places now in Vaksdal, and useful Voss or Vossestrand comparators.

The work is a source-pathway crosswalk, not a family-history conclusion. Each source should leave a clear trail for the place term or variant being used, why the source family applies, and what access or uncertainty state remains. Favor place-specific entries, factsheets, map objects, catalog/search-result pages, index rows, or cited book/PDF sections over broad parish, catalog, wiki, or bibliography hubs. Catalog-only and sign-in-limited sources can be useful when that limitation is explicit; do not reproduce gated record contents.

Evidence kinds:
- `historical_name_authority`: historical name or farm-name authority evidence for old spellings, pronunciation, older written forms, or probable equivalence.
- `modern_place_authority`: official or institutional modern place/map authority evidence, such as Kartverket SSR factsheets, Norgeskart, cadastral, or comparable place data.
- `local_farm_history`: local/farm-history bibliography, bygdebok, farm list, historical society, or comparable source identity evidence.
- `archive_catalog_pathway`: archive, library, or catalog pathway for records or source series, including Digitalarkivet, Nasjonalbiblioteket, WorldCat, FamilySearch catalog, or comparable public catalog surfaces.
- `jurisdiction_time_slice`: jurisdiction, parish, prestegjeld, sokn, tinglag, municipality, or boundary-change evidence that explains where the place belongs for a source/date slice.

Useful sources include public archive/catalog pages, official place-name or map authorities, historical farm-name authorities, local farm-history bibliographies or indexes, historical society pages, library records, and source-search or factsheet URLs that document a no-match or duplicate-looking state. Private family trees, current resident pages, social profiles, living-person material, record images behind sign-in, and generic tourism or transport pages do not count unless they also expose a substantive public place/source-pathway fact.

Do not let one broad source hub carry most of the work for many places or several `evidence_kind` branches. A broad PDF, parish catalog, wiki page, farm list, source catalogue, or library record can count only when the cited URL, visible result, or quoted section does place-specific work for the submitted place and the selected evidence kind. For a given farm/place, reusing the same hub across different evidence kinds is acceptable only when the page has separate visible place-specific material that independently satisfies each kind; otherwise use a more specific page, search-result URL, entry, factsheet, or source family.

Requirements:
- The source must tie the submitted farm/place scope to the Voss/Evanger/Vaksdal/Vossestrand source ecology through a place name, old or modern variant, farm-number/book index, municipality, parish, prestegjeld, sokn, tinglag, map object, or explicit no-match/search-result state. A broad source scope is not enough by itself unless the visible page, result, or cited section names the submitted place or a source-backed variant.
- The source must expose a substantive pathway detail appropriate to the selected `evidence_kind`: old spelling or equivalence evidence, official modern place-name data, local farm-history source identity, archive/catalog source family and coverage, or jurisdiction/time-slice context. The detail must be place-specific when the source family supports place-level pages, rows, entries, map objects, or search results; generic Evanger/Voss coverage alone does not satisfy multiple places.
- The source must make an access, limitation, or uncertainty state clear for this pathway: public scan or searchable index, official spelling status, catalog-only record, sign-in/gated or region-limited access, missing image/index/date range, no direct place match, duplicate-looking distinct place, probable equivalence, or unresolved variant conflict.

Write one JSON object per line to `results_voss_evanger_place_paths.jsonl`:
{"item": { "farm_place": "<farm_place>", "current_municipality": "<current_municipality>", "evidence_kind": "<evidence_kind>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
