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

## `pharma_former_rd_heads`

For each of the 52 European pharmaceutical and biotech companies listed below, supply 1+ (company, person) pairs (i.e. 2+ URLs per pair) identifying the person who held the top research-and-development leadership role — Head of R&D, EVP / SVP of R&D, Chief Scientific Officer, President of Research, Global Head of Research / Drug Discovery, or the equivalent group- or division-wide research-leadership post — immediately before the person who currently holds it at that company, with each URL on a page whose content shows that the named person held that research-leadership role at the named company and that they have since left it.

Companies in scope (canonical name — accepted aliases):
- **Roche** — Roche, F. Hoffmann-La Roche, Hoffmann-La Roche, Roche Holding, Genentech, Roche pRED, Roche Pharma Research and Early Development
- **Novartis** — Novartis, Novartis AG, Novartis Pharma, Novartis Institutes for BioMedical Research, NIBR, Biomedical Research
- **AstraZeneca** — AstraZeneca, AstraZeneca plc, AZ, MedImmune, AstraZeneca R&D
- **GSK** — GSK, GlaxoSmithKline, Glaxo, GSK plc, GlaxoSmithKline plc
- **Sanofi** — Sanofi, Sanofi-Aventis, Sanofi S.A., Sanofi Aventis, Genzyme
- **Novo Nordisk** — Novo Nordisk, Novo Nordisk A/S, Novo
- **Bayer** — Bayer, Bayer AG, Bayer Pharmaceuticals, Bayer HealthCare
- **Boehringer Ingelheim** — Boehringer Ingelheim, Boehringer, BI
- **Merck KGaA** — Merck KGaA, Merck Group, EMD Serono, Merck Healthcare, Merck Darmstadt
- **UCB** — UCB, UCB S.A., UCB Pharma
- **Lundbeck** — Lundbeck, H. Lundbeck, H. Lundbeck A/S
- **Ipsen** — Ipsen, Ipsen S.A.
- **Servier** — Servier, Les Laboratoires Servier
- **Grünenthal** — Grünenthal, Gruenenthal, Grunenthal, Grünenthal GmbH
- **Galapagos** — Galapagos, Galapagos NV
- **Genmab** — Genmab, Genmab A/S
- **Almirall** — Almirall, Almirall S.A.
- **Recordati** — Recordati, Recordati S.p.A.
- **Chiesi** — Chiesi, Chiesi Farmaceutici, Chiesi Group
- **Orion** — Orion, Orion Corporation, Orion Pharma
- **BioNTech** — BioNTech, BioNTech SE
- **Idorsia** — Idorsia, Idorsia Pharmaceuticals
- **argenx** — argenx, argenx SE, Argenx
- **Bavarian Nordic** — Bavarian Nordic, Bavarian Nordic A/S
- **Evotec** — Evotec, Evotec SE, Evotec AG
- **MorphoSys** — MorphoSys, MorphoSys AG
- **BioArctic** — BioArctic, BioArctic AB
- **Zealand Pharma** — Zealand Pharma, Zealand Pharma A/S, Zealand
- **Ascendis Pharma** — Ascendis Pharma, Ascendis Pharma A/S, Ascendis
- **Hikma** — Hikma, Hikma Pharmaceuticals, Hikma Pharmaceuticals plc
- **Indivior** — Indivior, Indivior PLC, Indivior plc
- **Vifor Pharma** — Vifor Pharma, Vifor, Vifor Pharma Group
- **CureVac** — CureVac, CureVac N.V., CureVac SE
- **Galderma** — Galderma, Galderma Group, Galderma S.A.
- **Sobi** — Sobi, Swedish Orphan Biovitrum, Swedish Orphan Biovitrum AB
- **Lonza** — Lonza, Lonza Group, Lonza Group AG
- **Stada** — Stada, STADA, Stada Arzneimittel, STADA Arzneimittel AG
- **Krka** — Krka, Krka d.d., Krka, d.d., Novo mesto
- **Gedeon Richter** — Gedeon Richter, Richter Gedeon, Richter Gedeon Nyrt.
- **Oxford BioMedica** — Oxford BioMedica, Oxford Biomedica, Oxford BioMedica plc, OXB
- **BenevolentAI** — BenevolentAI, Benevolent AI, BenevolentAI Limited
- **Immunocore** — Immunocore, Immunocore Holdings, Immunocore Holdings plc
- **Autolus** — Autolus, Autolus Therapeutics, Autolus Therapeutics plc
- **Adaptimmune** — Adaptimmune, Adaptimmune Therapeutics, Adaptimmune Therapeutics plc
- **Nicox** — Nicox, Nicox S.A., Nicox SA
- **Valneva** — Valneva, Valneva SE
- **DBV Technologies** — DBV Technologies, DBV, DBV Technologies S.A.
- **Innate Pharma** — Innate Pharma, Innate Pharma S.A., Innate
- **Genfit** — Genfit, GENFIT, Genfit S.A.
- **Bachem** — Bachem, Bachem Holding, Bachem Holding AG
- **Faron Pharmaceuticals** — Faron Pharmaceuticals, Faron, Faron Pharmaceuticals Oy
- **Oxford Nanopore** — Oxford Nanopore, Oxford Nanopore Technologies, Oxford Nanopore Technologies plc, ONT

Favor the person who was the immediate predecessor of the current holder; a holder two or more transitions back, with a different person between them and the current incumbent, is a weaker fit. This predecessor-of-the-current-holder framing — and any naming of the successor or description of the handover — is a property of the pair taken as a whole, not a requirement each cited page must satisfy: an individual page need only show that the named person held the research-leadership role at the company and has since left it. Back each pair with two URLs on genuinely different sources — the company's own site (governance, newsroom, leadership-history, or appointment / departure announcement) and an independent source (news coverage, the person's later employer or board bio, a professional profile); two pages from the same domain do not corroborate each other.

Requirements:
- The page must name the person and tie them to a top research-and-development leadership role at the named company — a unit-level, divisional, or group-wide R&D / research / science head such as Head of R&D, EVP / SVP R&D, Chief Scientific Officer, President of Research, or Global Head of Research / Drug Discovery — a non-leadership research scientist, a therapeutic-area or single-project lead, or a purely commercial / manufacturing / medical-affairs / regulatory role does NOT count.
- The page must establish that the person no longer holds that role at the named company — through departure / retirement / succession framing, a stated end date, a "formerly" / "previously" designation, or a subsequent role elsewhere that post-dates the company tenure — a page presenting them as the current incumbent does NOT count.

Write one JSON object per line to `results_pharma_former_rd_heads.jsonl`:
{"item": { "company": "<company>", "person": "<person>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
