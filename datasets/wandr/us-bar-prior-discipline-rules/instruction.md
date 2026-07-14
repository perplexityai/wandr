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

## `us_bar_prior_discipline_rules`

For each of the 51 in-scope US bar-admitting jurisdictions and each of the 2 listed `rule_class` values, supply 1+ URL for the (`jurisdiction`, `rule_class`) cell. Each URL must point to the jurisdiction's own court or bar-admission rules publication channel, or to a faithful mirror of those rules, and must carry the operative provision for the submitted `rule_class`.

A jurisdiction's attorney-discipline and bar-admission rules span two distinct rule classes. The submitted `rule_class` selects which rule book to use:

- `reciprocal_discipline`: how an attorney already admitted in the jurisdiction is handled in that jurisdiction's own disciplinary process when discipline has been imposed on the attorney by an outside jurisdiction. The provision typically sits in the jurisdiction's disciplinary-enforcement, disciplinary-procedure, bar-commission, or court rules governing attorney discipline.
- `admission_disclosure`: how an applicant for bar admission must disclose, document, or be screened for disciplinary history, current disciplinary standing, certificates of good standing, or analogous professional-disciplinary status in outside jurisdictions. The provision typically sits in the jurisdiction's rules governing admission to the bar, character-and-fitness rules, admission-on-motion or admission-without-examination rules, temporary or special admission rules, or rules of the supreme court relating to admissions. A provision that only requires prior admission elsewhere or years of practice, without tying that outside jurisdiction to disciplinary status, good standing, or discipline history, does not satisfy this rule class.

The 51 US bar-admitting jurisdictions in scope:

- **Alabama** (also written as: AL, Ala.)
- **Alaska** (also written as: AK)
- **Arizona** (also written as: AZ, Ariz.)
- **Arkansas** (also written as: AR, Ark.)
- **California** (also written as: CA, Cal., Calif.)
- **Colorado** (also written as: CO, Colo.)
- **Connecticut** (also written as: CT, Conn.)
- **Delaware** (also written as: DE, Del.)
- **District of Columbia** (also written as: DC, D.C., Washington DC, Washington, DC, Washington D.C.)
- **Florida** (also written as: FL, Fla.)
- **Georgia** (also written as: GA, Ga.)
- **Hawaii** (also written as: HI, Haw.)
- **Idaho** (also written as: ID)
- **Illinois** (also written as: IL, Ill.)
- **Indiana** (also written as: IN, Ind.)
- **Iowa** (also written as: IA)
- **Kansas** (also written as: KS, Kan.)
- **Kentucky** (also written as: KY, Ky.)
- **Louisiana** (also written as: LA, La.)
- **Maine** (also written as: ME)
- **Maryland** (also written as: MD, Md.)
- **Massachusetts** (also written as: MA, Mass.)
- **Michigan** (also written as: MI, Mich.)
- **Minnesota** (also written as: MN, Minn.)
- **Mississippi** (also written as: MS, Miss.)
- **Missouri** (also written as: MO, Mo.)
- **Montana** (also written as: MT, Mont.)
- **Nebraska** (also written as: NE, Neb., Nebr.)
- **Nevada** (also written as: NV, Nev.)
- **New Hampshire** (also written as: NH, N.H.)
- **New Jersey** (also written as: NJ, N.J.)
- **New Mexico** (also written as: NM, N.M., N.Mex.)
- **New York** (also written as: NY, N.Y.)
- **North Carolina** (also written as: NC, N.C.)
- **North Dakota** (also written as: ND, N.D.)
- **Ohio** (also written as: OH)
- **Oklahoma** (also written as: OK, Okla.)
- **Oregon** (also written as: OR, Ore., Oreg.)
- **Pennsylvania** (also written as: PA, Pa., Penn.)
- **Rhode Island** (also written as: RI, R.I.)
- **South Carolina** (also written as: SC, S.C.)
- **South Dakota** (also written as: SD, S.D.)
- **Tennessee** (also written as: TN, Tenn.)
- **Texas** (also written as: TX, Tex.)
- **Utah** (also written as: UT)
- **Vermont** (also written as: VT, Vt.)
- **Virginia** (also written as: VA, Va.)
- **Washington** (also written as: WA, Wash.)
- **West Virginia** (also written as: WV, W.Va., W. Va.)
- **Wisconsin** (also written as: WI, Wis., Wisc.)
- **Wyoming** (also written as: WY, Wyo.)

The US territories below are outside this task's jurisdiction universe; their bar-admission and attorney-discipline regimes are not in scope:

- **Puerto Rico** (also written as: PR, P.R.)
- **Guam** (also written as: GU)
- **U.S. Virgin Islands** (also written as: USVI, Virgin Islands)
- **American Samoa** (also written as: AS)
- **Northern Mariana Islands** (also written as: CNMI, MP)

Federal-court attorney admission and state-bar attorney admission are distinct regimes. The claimed jurisdiction is always the state-bar (or DC-bar) regime, never any federal court.

Authoritative source channels by `rule_class`:

- `reciprocal_discipline`: the jurisdiction's own court of last resort, judiciary, or attorney-disciplinary authority publication channel for its rules of disciplinary enforcement and disciplinary procedure: state-supreme-court or state-judiciary domains, state attorney-disciplinary board, lawyer-regulation-system, or bar-counsel domains, the official state administrative or session-laws code carrying those court rules, or a recognized faithful mirror carrying both the section number and the operative text
- `admission_disclosure`: the jurisdiction's own court of last resort, judiciary, board of bar examiners, or bar-admission authority publication channel for its rules governing admission to the bar, character and fitness, admission on motion / without examination, or temporary and special admission: state-supreme-court or state-judiciary domains, state board of bar examiners or bar-admissions-office domains, the official state administrative or session-laws code carrying those bar-admission rules, or a recognized faithful mirror carrying both the section number and the operative text

Requirements:
- The page must identify the named rule provision by section number, rule number, or other rule-numbering anchor sufficient that a reader could uniquely locate the provision within the jurisdiction's rules.
- The operative provisions must substantively match the claimed rule class under the scope for the submitted `rule_class`.
- The provision must reach outside-jurisdiction attorney discipline, disciplinary history, current disciplinary standing, certificates of good standing, or analogous professional-disciplinary status, using outside-the-jurisdiction framing such as another or foreign jurisdiction, every jurisdiction of admission, or equivalent wording.
- The page must communicate, through its URL, title, publisher context, or page text, that it is on this jurisdiction's own court or bar-admission rule publication channel for the claimed rule class, or on a faithful mirror of those rules.
- The page must present the provision as currently in force as of May 7, 2026. A current official rule publication, or a faithful mirror of that publication, satisfies this unless the page itself marks the provision as former, superseded, repealed, proposed, or not yet adopted. Amendment-history-only text does not satisfy the in-force requirement.

Write one JSON object per line to `results_us_bar_prior_discipline_rules.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "rule_class": "<rule_class>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
