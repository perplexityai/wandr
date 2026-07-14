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

## `ftse_private_roles`

For 48+ companies from the full FTSE Women Leaders private-company canon below, cover the 2 role-kind slots below with positive public role evidence where official sources support them. For each submitted company-role pair, supply 1+ role-evidence URLs naming the person and role.

This is a public executive-role evidence task, not a complete CEO/CFO absence table. Current official leadership/report pages are preferred. Official dated appointment or transition pages also count when the row is framed as dated role evidence rather than unqualified current-role proof.

FTSE private-company canon source: https://ftsewomenleaders.com/company-rankings/

Canonical companies in scope:
- **DLA Piper International LLP** (also written as: DLA Piper, DLA Piper International)
- **John Lewis Partnership Plc** (also written as: John Lewis Partnership, JLP, John Lewis)
- **Matalan Ltd** (also written as: Matalan, Matalan Limited)
- **CDS (Superstores International) Ltd** (also written as: The Range, Range, CDS, CDS Superstores, CDS Superstores International, CDS (Superstores International) Limited)
- **The Co-operative Group Ltd** (also written as: Co-operative Group, Co-operative Group Limited, Co-op, Co-op Group, The Co-op)
- **Freshfields LLP** (also written as: Freshfields, Freshfields Bruckhaus Deringer, Freshfields Bruckhaus Deringer LLP)
- **Mace Group Ltd** (also written as: Mace, Mace Group, Mace Construct)
- **Ernst & Young LLP** (also written as: EY, EY UK, Ernst and Young, Ernst & Young)
- **Deloitte LLP** (also written as: Deloitte, Deloitte UK)
- **Pentland Group Ltd** (also written as: Pentland, Pentland Group, Pentland Brands)
- **PricewaterhouseCoopers LLP** (also written as: PwC, PWC, PwC UK, PricewaterhouseCoopers)
- **Arup Group Ltd** (also written as: Arup, Arup Group, Ove Arup)
- **Wm Morrison Supermarkets Ltd** (also written as: Morrisons, Morrison, Morrison Supermarkets, Wm Morrison, Wm Morrison Supermarkets)
- **Linklaters LLP** (also written as: Linklaters)
- **Colt Group Holdings Ltd** (also written as: Colt, Colt Group, Colt Technology Services)
- **Nationwide Building Society** (also written as: Nationwide)
- **Accenture (UK) Ltd** (also written as: Accenture, Accenture UK, Accenture (UK) Limited)
- **Laing O'Rourke Corp Ltd** (also written as: Laing O'Rourke, Laing ORourke, Laing O Rourke, Laing O'Rourke Corp, Laing O'Rourke Corporation)
- **INEOS Group** (also written as: INEOS, Ineos)
- **Wolseley UK Ltd** (also written as: Wolseley, Wolseley UK, Wolseley UK Limited)
- **A&O Shearman LLP** (also written as: A&O Shearman, A and O Shearman, Allen & Overy Shearman, Allen Overy Shearman)
- **Samworth Brothers (Holdings) Ltd** (also written as: Samworth Brothers, Samworth Brothers Holdings)
- **A.F. Blakemore & Son Ltd** (also written as: A.F. Blakemore, A F Blakemore, AF Blakemore, Blakemore, A.F. Blakemore & Son)
- **Virgin Atlantic Ltd** (also written as: Virgin Atlantic, Virgin Atlantic Airways)
- **Anglian Water Group Ltd (AWG)** (also written as: Anglian Water, Anglian Water Group, Anglian Water Group Limited, AWG)
- **M Group Ltd** (also written as: M Group, M Group Services)
- **FGP Topco Ltd** (also written as: FGP Topco, Heathrow, Heathrow Airport, Heathrow Airport Holdings)
- **British United Provident Association Ltd (BUPA)** (also written as: BUPA, Bupa, Bupa Group, British United Provident Association)
- **KPMG LLP** (also written as: KPMG, KPMG UK)
- **Muller UK & Ireland Group LLP** (also written as: Muller, Muller UK & Ireland, Muller UK and Ireland, Muller UK & Ireland Group)
- **Thames Water Utilities Ltd** (also written as: Thames Water, Thames Water Utilities, Thames Water Utilities Limited)
- **EG Group Ltd** (also written as: EG, EG Group, Euro Garages)
- **City Facilities Management Holdings Ltd** (also written as: City Facilities Management, City Facilities Management Holdings, City FM)
- **VMED O2 UK Ltd (Virgin Media O2)** (also written as: VMED O2 UK, Virgin Media O2, VMO2, Virgin Media, O2 UK)
- **2 Sisters Food Group Ltd** (also written as: 2 Sisters, 2 Sisters Food Group, Two Sisters Food Group)
- **Specsavers Optical Group Ltd** (also written as: Specsavers, Specsavers Optical Group)
- **Merlin Entertainments Ltd** (also written as: Merlin, Merlin Entertainments)
- **ASDA Group Ltd** (also written as: ASDA, Asda, ASDA Group, Asda Group)
- **AWE Plc** (also written as: AWE, AWE plc, Atomic Weapons Establishment)
- **Wates Group Ltd** (also written as: Wates, Wates Group)
- **Avara Foods Ltd** (also written as: Avara, Avara Foods)
- **Bet365 Group Ltd** (also written as: bet365, Bet365, Bet365 Group)
- **Arnold Clark Automobiles Ltd** (also written as: Arnold Clark, Arnold Clark Automobiles)
- **Mott MacDonald Group Ltd** (also written as: Mott MacDonald, Mott MacDonald Group)
- **Hermes Parcelnet Ltd (Evri)** (also written as: Hermes Parcelnet, Hermes Parcelnet Limited, Evri, Hermes, Hermes UK)
- **Rubix Ltd** (also written as: Rubix, Rubix Limited, Rubix UK)
- **KCA DEUTAG Drilling Group Ltd** (also written as: KCA DEUTAG, KCA Deutag, KCA DEUTAG Drilling, KCA Deutag Drilling)
- **Marshall Group Properties Ltd** (also written as: Marshall Group, Marshall Group Properties, Marshall of Cambridge)

Role kinds:
- **chief_executive**: CEO, Chief Executive, Chief Executive Officer, Chief Executive Officer CEO, Group Chief Executive, Group Chief Executive Officer, Interim CEO, Managing Partner, Global Managing Partner, Managing Partner and Global Co-CEO, Global Co-CEO, Co-CEO, Co Chief Executive
- **finance_lead**: CFO, Chief Financial Officer, Chief Financial Officer CFO, Chief Finance Officer, Chief Finance Officer CFO, Group CFO, Group Chief Financial Officer, Finance Director, Group Finance Director, Executive Director Finance, Interim CFO, Interim Chief Financial Officer

Source modes to make clear in each row:
- **current_role_surface**: a current leadership, board, governance, team, executive, profile, or equivalent official page that names the person and role as currently held
- **latest_report_or_accounts**: a latest annual report, accounts, results, investor, or debt-reporting page/document that names the person and role in the current report context
- **dated_appointment_or_transition**: an official appointment, election, departure, transition, or effective-date announcement; this supports the dated role/event claim, not unqualified currentness

Role-evidence sources should be official company or firm pages, board / executive / governance / team pages, official media-centre announcements, official annual reports or accounts, results, investor or debt-reporting pages, or statutory filings whose text itself states the executive title. Companies House can support legal identity, company status, officer status, and appointment timing, but an ordinary officer list does not by itself prove a CEO, CFO, or finance-director title.

LinkedIn snippets, people aggregators, org-chart products, contact-enrichment tools, scraped bio databases, generic company databases, and the FTSE report's role-marker column do not count as primary roleholder evidence. Reputable business press is useful only as secondary conflict context, not as the primary source for a row. Do not infer gender, collect contact details, rank executives, score governance, or provide investment or outreach analysis.

Requirements:
- The page must connect the role evidence to the submitted FTSE company, an accepted legal or trading alias, or the same official group/firm identity.
- The page must name the person and state a role title that matches the submitted `role_kind`, with the role held for that FTSE company or official group/firm identity rather than merely for an unrelated entity, product line, local office, or business unit.
- The page must support the submitted source mode: current-role framing for current rows, latest-report framing for report/accounts rows, or dated appointment / transition / effective-date framing for event rows.

Write one JSON object per line to `results_ftse_private_roles.jsonl`:
{"item": { "company": "<company>", "role_kind": "<role_kind>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
