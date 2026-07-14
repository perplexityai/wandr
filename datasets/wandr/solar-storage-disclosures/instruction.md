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

## `solar_storage_disclosures`

For 120+ U.S. solar-plus-storage project/company contexts, cover each of the 3 disclosure facets below by supplying a public source (i.e. 1+ URL per facet) that states a project-scoped disclosure and visibly connects the named project, locality, state, and primary company.

The useful work is separating source-stated project disclosures from conclusions about whether a project is approved, operating, interconnected, feasible, safe, investable, worth procuring from, or recommended.

Disclosure facets:
- `project_profile`: a public project-scoped profile or record that identifies the project/context and states concrete source-stated project attributes.
- `company_commitment`: a company, parent, customer, offtaker, financier, investor, operator, or comparable source-role-visible page that states a project-scoped commitment, milestone, investment, financing, ownership, PPA/offtake, portfolio, or service-role disclosure.
- `entity_bridge`: a public page that explicitly connects the project/context to a distinct legal vehicle, developer, parent, counterparty, customer, offtaker, financier, public applicant, agreement party, owner/operator, asset manager, or comparable entity and makes the relationship role visible.

Each project/company context should be a named U.S. project or public project context involving both solar generation and battery or energy storage. Project aliases, project LLCs, solar/storage sibling entities, parent brands, customers, and counterparties count as connected only when the page itself makes the connection visible. Generic portfolio pages, trackers, search results, top-company listicles, lead-generation pages, contact-only pages, private databases, price/RFQ pages, and pages centered on emails, phone numbers, or private addresses do not provide useful task evidence.

Requirements:
- The page must identify the named project/context, U.S. locality or state, and relevant primary company role well enough to match the submitted project/company context.
- The page must frame the project/context as solar-plus-storage: solar generation paired with battery or energy storage under the same named project, facility, portfolio entry, agreement, filing, or source-stated project context.
- The page should make its public disclosure source role visible at the bar appropriate to `disclosure_facet`. For `project_profile`, the page should read as a project-specific profile, project page, official record, filing, fact sheet, or comparable project-context surface. For `company_commitment`, it should read as a controlled channel, filing, investor/ESG/press page, customer/offtaker announcement, financing statement, or comparable page for the party making the commitment. For `entity_bridge`, it should read as an official channel of a connected party or an official public record, filing, agreement, docket, or project-context surface that identifies the parties; generic news, trackers, listicles, and discovery databases usually will not show enough source-role anchoring.
- The page should state a focused disclosure for `disclosure_facet`. For `project_profile`, it should give concrete project attributes such as capacity, location, stage, schedule/COD target, capex/investment, acreage, ownership/service role, or comparable project fields. For `company_commitment`, it should state a project-specific commitment, milestone, investment, financing, PPA/offtake, customer/partner context, ownership, construction, operating, or service-role claim. For `entity_bridge`, it should explicitly name the connected entity and make its project relationship role visible rather than merely mentioning a company, locality, or broad portfolio.

Write one JSON object per line to `results_solar_storage_disclosures.jsonl`:
{"item": { "project": "<project>", "locality": "<locality>", "state": "<state>", "primary_company": "<primary_company>", "disclosure_facet": "<disclosure_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
