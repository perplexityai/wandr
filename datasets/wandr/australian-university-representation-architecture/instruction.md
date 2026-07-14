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

## `australian_university_representation_architecture`

For each of the 36 Australian public or statutory universities listed below, supply governing-body seat-allocation evidence for 6+ normalized seat classes per university. For each (`university`, `seat_type`) pair, include 1+ source URLs for each of the 2 evidence sides.

The goal is to compare each governing body's representation design as proportions and mechanisms, not just named-member counts. Local seat labels matter alongside the normalized class. Each record reports the class count or quota, governing-body denominator or denominator range, and class mechanics as supported by the cited page.

Target universities:
- **Adelaide University**
- **Australian Catholic University**
- **Australian National University**
- **Central Queensland University**
- **Charles Darwin University**
- **Charles Sturt University**
- **Curtin University**
- **Deakin University**
- **Edith Cowan University**
- **Federation University Australia**
- **Flinders University**
- **Griffith University**
- **James Cook University**
- **La Trobe University**
- **Macquarie University**
- **Monash University**
- **Murdoch University**
- **Queensland University of Technology**
- **RMIT University**
- **Southern Cross University**
- **Swinburne University of Technology**
- **University of Canberra**
- **University of Melbourne**
- **University of Newcastle**
- **University of New England**
- **University of New South Wales**
- **University of Queensland**
- **University of Southern Queensland**
- **University of the Sunshine Coast**
- **University of Sydney**
- **University of Tasmania**
- **University of Technology Sydney**
- **University of Western Australia**
- **University of Wollongong**
- **Victoria University**
- **Western Sydney University**

The Adelaide University entry means the current merged institution. Predecessor-only governance pages for The University of Adelaide or the University of South Australia / UniSA do not qualify unless the page itself is current Adelaide University governance evidence.

Normalized seat classes:
- **official_executive**: ex officio executive offices such as Chancellor, Vice-Chancellor, President, or equivalent senior office-holder seats
- **official_academic_governance**: official academic-governance offices such as Academic Board chair, Academic Senate president, or equivalent academic-body office seats
- **government_appointed**: ministerial, Governor, Governor-in-Council, parliamentary, or other government-appointed seats
- **council_appointed**: council/senate/board-appointed, co-opted, or externally appointed expertise seats chosen by the governing body or a selection committee
- **elected_academic_staff**: academic staff seats filled by election or equivalent academic-staff constituency process
- **elected_professional_staff**: professional, general, non-academic, or administrative staff seats filled by election or equivalent staff-constituency process
- **elected_student**: student seats filled by election or equivalent student-constituency process, including undergraduate, postgraduate, coursework, research, or combined student seats
- **alumni_graduate_elected**: alumni, graduate, convocation, or similar graduate-body representative seats
- **other_reserved**: reserved or representative seats not captured above, such as Indigenous, vocational-education, donor, union, community, or special-purpose categories

Evidence sides:
- `current_roster`: official current evidence identifying occupants, office-holders, vacancies, or active reserved slots for the local seat class, with enough category context to count the class and current governing-body denominator.
- `formal_rule`: formal legal or governance-instrument evidence for the local seat class's allocation, selection path, denominator basis, and term or eligibility limits.

Primary governance sources fit this task: official university governance/member pages, official sector-governance member-university pages that publish a current governing-body roster for the named university, annual-report governance sections, current legislation, statutes, regulations, charters, governance handbooks, terms of reference, or comparable governance instruments. Legal or governance-instrument pages can support `current_roster` only when they identify an active current seat, vacancy, or reserved slot for the governing body. Sector-governance member-university pages support `current_roster` only; they do not support `formal_rule` merely by summarizing or linking to a legal or governance instrument. Third-party profiles, media articles, Wikipedia, LinkedIn, and standalone person biographies do not work as primary evidence here.

Requirements:
- The page ties the cited evidence to the named university's principal governing body: Council, Senate, Board of Governors, Board of Trustees, or its local equivalent.
- The page supports the local seat-category label or role grouping and its mapping to the submitted normalized seat class.
- The page supports the reported scale: for `current_roster`, occupied, vacant, or reserved seats in the submitted class and the current governing-body denominator; for `formal_rule`, a class count, quota, office count, composition formula, or equivalent allocation rule plus the governing-body denominator or denominator range.
- The page supports the reported mechanics: for `current_roster`, at least one current occupant or office-holder, a current vacancy, or an active reserved slot for that class; for `formal_rule`, the selection, appointment, election, or office-holding mechanism plus a term, eligibility, constituency, term-limit, or comparable rule for that class.

Write one JSON object per line to `results_australian_university_representation_architecture.jsonl`:
{"item": { "university": "<university>", "seat_type": "<seat_type>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
