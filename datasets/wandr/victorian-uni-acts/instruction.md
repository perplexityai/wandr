You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `victorian_uni_acts`
  - `victorian_uni_acts.current_register`

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

## `victorian_uni_acts`

For each of the 8 Victorian public universities below, cover each of the 9 substantive statutory governance facets. For every (`university`, `governance_facet`) pair, supply one source under each of the 3 evidence-source roles listed below (i.e. 1+ URL per role): one current authorised enabling-Act text source, one university-controlled Council/governance-framework corroboration source, and one distinct university-controlled legal/accountability corroboration source. State the current source metadata, exact section or official reference, short statutory proposition, relevant excerpt, checked date, source-role rationale, and any dependency or missing-state signal.

Output every root record with an `item` object that includes exactly the root key fields `university`, `governance_facet`, and `evidence_source`, plus the row URL. For `item.evidence_source`, copy one of the three literal tokens listed below; do not paraphrase them. Do not emit URL-only rows, do not use aliases such as `facet`, `source_role`, or `evidence_source_role`, and do not move these key fields into `answer`. For the `current_register` subtask, use `item.university` plus the register URL.

The university universe is closed:

- `Deakin University`
- `Federation University Australia`
- `La Trobe University`
- `Monash University`
- `RMIT University`
- `Swinburne University of Technology`
- `The University of Melbourne`
- `Victoria University`

The governance facets are:

- `chancellor_or_council_officers`: statutory Chancellor, Deputy Chancellor, Vice-Chancellor, Visitor, or other Council/officer provisions
- `commercial_activity_or_reporting`: commercial-activity powers, significant commercial activity approvals, guidelines, audit, reporting, corporations, joint ventures, or related oversight provisions
- `council_member_duties_or_responsibilities`: member duties, responsibilities, conduct, conflict, or care-type provisions
- `council_membership_rule`: statutory membership architecture, classes, appointment sources, fixed-number rules, and any Order-in-Council dependency
- `council_role`: Council as governing body plus its general direction, superintendence, primary responsibilities, or comparable role provisions
- `ministerial_or_government_oversight`: Minister, Governor in Council, administration, accountability, approval, guideline, audit, or government oversight provisions/facts
- `objects_or_purpose`: objects, purposes, or statutory purpose language
- `statutes_regulations_or_subordinate_law`: Act provisions empowering, approving, commencing, making, publishing, or constraining university statutes, regulations, or subordinate law
- `university_functions_or_powers`: university-level powers, functions, body-corporate status, awards, property, or comparable enabling powers

The companion `current_register` subtask separately asks for the current Victorian legislation register page for each university's enabling Act. In this root provision panel, register pages can supply currentness context but do not replace section-level Act text or the two university-controlled corroboration source families.

The evidence-source roles of interest, which we refer to as `evidence_source`, are:
- `authorised_act_text`: a current authorised enabling-Act text source, such as a fetchable current authorised Act PDF/text on an official Victorian legislation surface or an official university-hosted copy that visibly matches the current authorised version. It must expose the operative section, schedule, Order dependency, or official administration entry relied on for the governance facet.
- `university_council_governance_surface`: a current official university-controlled Council charter, governance framework, Council page, committee terms, governance code, or comparable Council/governing-body source that quotes, cites, applies, or operationalizes the same enabling-Act provision or governance-facet rule. This role should show how the university's governing body uses the Act-based rule.
- `university_legal_accountability_surface`: a current official university-controlled legal, policy-library, statute/regulation, FOI, annual-report, compliance, delegations, commercial-activity, or accountability source that quotes, cites, applies, or operationalizes the same enabling-Act provision or governance-facet rule. This role should come from a different university source family than the Council/governance-framework source, not the same URL or substantially the same document under a second label.

Only the three exact `evidence_source` values above are valid. Do not output old, informal, or descriptive labels such as `university_governance_corroboration`, `governance_corroboration`, `university_council_or_governance_framework`, `university_legal_or_accountability_surface`, `source_role`, or `evidence_source_role`.

Sources must be official, current, and fetch-compatible. Direct `content.legislation.vic.gov.au` DOCX or PDF file URLs count for `authorised_act_text` only when the fetched page content visible to the evaluator exposes the operative section body relied on by the answer. Current legislation landing pages belong in the companion current-register evidence and do not support these substantive provision facets without section text. PDF cover pages, front matter, and table-of-provisions or table-of-contents headings are not enough. Official Administration of Acts reports can support ministerial administration facts where relevant, but they do not substitute for Act-section text when the answer claims a specific statutory provision.

University Council pages, university governance frameworks, charters, policies, university statutes or regulations, annual reports, FOI statements, delegations, and accountability materials are valid for the two university-controlled roles only when the fetched page gives a concrete governance-facet hook: an exact Act section citation, quoted or reproduced provision text, official university legal reference, or implementation/accountability statement tied to the enabling Act. Generic summaries, current officeholder lists without statutory connection, law-firm notes, private legal databases, sector explainers, media, inquiries, submissions, advocacy pages, historical/as-made legislation, repealed legislation, and superseded versions do not establish current source evidence.

The `council_membership_rule` facet is about statutory membership architecture. If the Act makes a number or class depend on an Order in Council, record that dependency rather than substituting current Council profiles or named officeholders. A university-controlled corroboration source may describe current Council composition, but it still needs a visible statutory or governance-framework tie to the Act rule.

High-yield source strategy:
- For `authorised_act_text`, prefer fetchable authorised Act PDF/DOCX files that expose the actual sections you cite. Known useful families include university-hosted Act copies such as Deakin's Act PDF, La Trobe's current Act PDF, Swinburne's authorised Act PDF, and official Victorian legislation `sites/default/files/... authorised.pdf` or `.docx` files when the fetched content shows the operative section text. Do not use an in-force landing page for a root provision row unless it also exposes the section text being claimed.
- For `university_council_governance_surface`, prefer Council Charters, Governance Frameworks, Council Statutes, and Council-facing policy documents that contain the Act hook in the visible text. Known useful families include Deakin Policy Library Council Charter pages, Federation Council Charter or Federation University Australia Statute PDFs, La Trobe Council duties/statute documents, RMIT Council Governance Charter or governance-framework PDFs, Victoria University Council Charter or Governance Framework PDFs, and University of Melbourne policy pages that identify their Act authority.
- For `university_legal_accountability_surface`, prefer legal/accountability surfaces that cite the Act and apply the relevant facet, such as Monash FOI Statement One for objects, Monash commercial-activity guidelines for commercial and ministerial-approval facets, RMIT statutes/regulations policy pages, Federation legal/university-legislation or statute pages, Victoria University policy-library regulation documents, Deakin Council Regulations or commercial-activities policies, La Trobe legal-services statutes, and Swinburne statute/policy pages that cite section 28 or Part 5. Generic "university legislation", "registrations", "quality compliance", or Council member profile pages usually fail unless they include the specific section-level hook and operative substance.

Requirements:
- The page must tie the evidence item to the claimed university's current enabling Act or to a current official university/Victorian public-sector administration or accountability source for that Act, including Act title plus version, effective-date, incorporating-amendments, current source-date, approval date, or report-date context that the answer relies on.
- The page must fit the selected `evidence_source`: current authorised Act text for `authorised_act_text`, current university-controlled Council/governance-framework corroboration for `university_council_governance_surface`, or current university-controlled legal/accountability corroboration for `university_legal_accountability_surface`.
- The page must support the claimed `governance_facet` with an exact Act section, schedule, Order, Gazette, official administration/report reference, or official university legal/governance reference appropriate to that facet.
- The fetched page content and excerpts must expose the operative provision text, section-level citation with enough quoted or applied substance, or official administration/report entry relied on by the evidence item; metadata-only landing pages, blocked or empty government file content, PDF cover/front matter, broad summaries, and table-of-provisions headings are not sufficient.
- The page must support the short statutory, governance-implementation, or government-administration proposition stated for the evidence item as factual source extraction rather than legal advice, policy recommendation, governance opinion, or university ranking.
- The answer must capture any visible dependency, missing, superseded/conflict, or non-statutory-context state that matters for the evidence item, especially Order-in-Council dependencies for Council membership.

Write one JSON object per line to `results_victorian_uni_acts.jsonl`:
{"item": { "university": "<university>", "governance_facet": "<governance_facet>", "evidence_source": "<evidence_source>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `victorian_uni_acts.current_register`

Cross-tasknode identifier discipline: this task is for the same {= university =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For each of the {= university =} Victorian public universities below, supply 1+ current official Victorian legislation register source identifying the university's current enabling Act, Act number, in-force status, current version or authorised file, and effective or incorporating-amendments context.

The university universe is closed:

- `Deakin University`
- `Federation University Australia`
- `La Trobe University`
- `Monash University`
- `RMIT University`
- `Swinburne University of Technology`
- `The University of Melbourne`
- `Victoria University`

Use a current `legislation.vic.gov.au` in-force Act landing page or version-specific register page for the university's enabling Act. The source should establish the Act identity and current register state; it is not expected to expose every substantive governance provision.

Requirements:
- The page must be an official Victorian legislation in-force register page for the claimed university's enabling Act, not a university mirror, as-made Act page, repealed/historical page, third-party database, or general search result.
- The page must identify the Act title and Act number, and tie them to the claimed university, including any visible former-title context that matters for the university name.
- The page must show current register/version context such as Act in force status, current version number, authorised file/version link, effective date, incorporating-amendments date, or version-history status.
- The answer must state the checked date and capture any visible former-title, superseded-version, amendment-history, or other currentness boundary that matters for using the Act as current evidence.

Write one JSON object per line to `results_victorian_uni_acts.current_register.jsonl`:
{"item": { "university": "<university>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
