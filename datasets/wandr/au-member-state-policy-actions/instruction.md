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

## `au_member_state_policy_actions`

For each of the 54 in-scope African Union member states and each of the 6 policy areas listed below, supply 1+ distinct major *well-identified* policy actions (each a discrete artifact identifiable by citation, number, official title, or treaty-body document number) per (country, area) cell. Each action's first-adoption, promulgation, or — for UPR documents — official submission, distribution, review-session, or Council-session date must fall within January 1, 2013 through April 30, 2026; supply source URLs for each action (at least 1 per action).

The 54 African Union member states in scope are those listed below with UPR review records:

- **Algeria** (also written as: الجزائر, People's Democratic Republic of Algeria, Algérie)
- **Angola** (also written as: República de Angola)
- **Benin** (also written as: Bénin, République du Bénin)
- **Botswana** (also written as: Republic of Botswana)
- **Burkina Faso**
- **Burundi** (also written as: Republika y'Uburundi, République du Burundi)
- **Cabo Verde** (also written as: Cape Verde, República de Cabo Verde)
- **Cameroon** (also written as: Cameroun, République du Cameroun)
- **Central African Republic** (also written as: CAR, RCA, République centrafricaine)
- **Chad** (also written as: تشاد, Tchad, République du Tchad)
- **Comoros** (also written as: جزر القمر, Comores, Union des Comores)
- **Congo (Brazzaville)** (also written as: Republic of the Congo, Congo-Brazzaville, République du Congo)
- **Côte d'Ivoire** (also written as: Cote d'Ivoire, Ivory Coast, République de Côte d'Ivoire)
- **Democratic Republic of the Congo** (also written as: DRC, DR Congo, Congo-Kinshasa, RDC, République démocratique du Congo)
- **Djibouti** (also written as: جيبوتي, République de Djibouti)
- **Egypt** (also written as: مصر, Arab Republic of Egypt, Égypte)
- **Equatorial Guinea** (also written as: Guinea Ecuatorial, República de Guinea Ecuatorial, Guinée équatoriale)
- **Eritrea** (also written as: ኤርትራ, State of Eritrea)
- **Eswatini** (also written as: Swaziland, Kingdom of Eswatini)
- **Ethiopia** (also written as: ኢትዮጵያ, FDRE, Federal Democratic Republic of Ethiopia)
- **Gabon** (also written as: Gabonese Republic, République gabonaise)
- **Gambia** (also written as: The Gambia, Republic of The Gambia)
- **Ghana** (also written as: Republic of Ghana)
- **Guinea** (also written as: Guinée, République de Guinée)
- **Guinea-Bissau** (also written as: Guiné-Bissau, República da Guiné-Bissau)
- **Kenya** (also written as: Republic of Kenya, Jamhuri ya Kenya)
- **Lesotho** (also written as: Kingdom of Lesotho)
- **Liberia** (also written as: Republic of Liberia)
- **Libya** (also written as: ليبيا, State of Libya)
- **Madagascar** (also written as: Repoblikan'i Madagasikara, République de Madagascar)
- **Malawi** (also written as: Republic of Malawi)
- **Mali** (also written as: République du Mali)
- **Mauritania** (also written as: موريتانيا, Moritani, Islamic Republic of Mauritania, République islamique de Mauritanie)
- **Mauritius** (also written as: République de Maurice, Île Maurice)
- **Morocco** (also written as: المغرب, Maroc, Royaume du Maroc)
- **Mozambique** (also written as: Moçambique, República de Moçambique)
- **Namibia** (also written as: Republic of Namibia)
- **Niger** (also written as: République du Niger)
- **Nigeria** (also written as: Federal Republic of Nigeria)
- **Rwanda** (also written as: Repubulika y'u Rwanda, République du Rwanda)
- **São Tomé and Príncipe** (also written as: São Tomé e Príncipe, Sao Tome and Principe, STP)
- **Senegal** (also written as: Sénégal, République du Sénégal)
- **Seychelles** (also written as: Sesel, Republic of Seychelles)
- **Sierra Leone** (also written as: Republic of Sierra Leone)
- **Somalia** (also written as: الصومال, Soomaaliya, Federal Republic of Somalia)
- **South Africa** (also written as: Suid-Afrika, RSA, Republic of South Africa)
- **South Sudan** (also written as: Republic of South Sudan)
- **Sudan** (also written as: السودان, Republic of the Sudan)
- **Tanzania** (also written as: Jamhuri ya Muungano wa Tanzania, United Republic of Tanzania)
- **Togo** (also written as: Togolese Republic, République togolaise)
- **Tunisia** (also written as: تونس, Tunisian Republic, Tunisie)
- **Uganda** (also written as: Republic of Uganda)
- **Zambia** (also written as: Republic of Zambia)
- **Zimbabwe** (also written as: Republic of Zimbabwe)

The AU member state below is outside this task's country universe because the UPR arm is limited to countries with UPR review records:

- **Sahrawi Arab Democratic Republic** (also written as: Sahrawi Republic, SADR, Western Sahara, République arabe sahraouie démocratique, República Árabe Saharaui Democrática)

The policy areas are:

- **Trade** — customs / tariff / non-tariff / trade-promotion legislation; trade-policy implementation orders; national-level domestication or ratification acts and tariff schedules for continental or regional-trade-bloc protocols; WTO accession or notification documents at country level
- **Tech** — data protection / privacy acts; cybersecurity laws; cybercrime acts; digital-economy / AI governance national strategies; e-government / digital-ID enabling legislation; technology / startup / innovation acts
- **Media** — broadcasting acts; press / media regulation laws; access-to-information / right-to-information acts; defamation or cybercrime statutes whose primary effect is on press / journalism activity; community-radio licensing frameworks; press-council / media-authority establishment acts
- **Telecom** — ICT / electronic communications acts; spectrum management regulations; universal-service-fund rules; major-operator licensing actions; OTT / number-portability / mobile-money policy regulations; ITU-related domestications
- **ADR** — Alternative Dispute Resolution: national arbitration acts and reforms; mediation acts; country-authored commercial-dispute-resolution centre enabling legislation and reforms; AfCFTA Dispute Settlement Body protocol implementations; ODR pilot frameworks; investment-treaty ICSID-related ADR domestications
- **UPR** — Universal Periodic Review state-authored artifacts specific to the country: National Report / state-authored submission, Addendum / Views on conclusions and recommendations, and equivalent state-authored responses or submissions whose official distribution, review-session, or Council-session date falls within the target window

UPR claims are limited to state-authored artifacts from the UN Human Rights Council's per-cycle review process, such as National Reports and state addenda / responses. Review materials authored by UN offices or stakeholders can help discover the cycle, but they are not the country-authored action requested here.

Requirements:
- The page must identify the action's specific identity by citation, number, official title, or treaty-body document number, sufficient that a reader could uniquely locate the action.
- The page must evidence country-of-origin authorship for the claimed country.
- The page must place the action substantively in the claimed policy area.
- The page must pin the action's first-adoption, promulgation, or official UPR document date within 2013-01-01 through 2026-04-30.
- The page must communicate (possibly via URL among other things) that it is on a country-authoritative national-publication channel for the country's policy artifacts of that area, on a recognized legal archive carrying the official text for the country, or — when the action is the country's domestication of a pan-African instrument — on an institutional surface controlled by the issuing pan-African body. For UPR claims, the page must instead carry a state-authored UPR artifact for that country's review on a UN HRC per-cycle documentation channel or faithful document mirror.

Write one JSON object per line to `results_au_member_state_policy_actions.jsonl`:
{"item": { "country": "<country>", "area": "<area>", "action": "<action>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
