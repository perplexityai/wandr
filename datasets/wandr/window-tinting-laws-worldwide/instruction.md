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

## `window_tinting_laws_worldwide`

As of May 7, 2026, vehicle-window tinting compliance remains highly local: the same product can be legal for a rear passenger window, illegal on the driver's window, and exempt only through a medical or inspection process in another country.

For each of the 30 countries listed below and each of the 7 tinting-law axes, name the country's operative rule for that axis (at least 1 per cell). Supply source URLs for each rule (1+ per rule), each on a page that substantiates the country-specific rule and its current or as-of legal force.

The countries in scope are:

- **Argentina** (also written as: Argentine Republic, Republica Argentina)
- **Australia** (also written as: Commonwealth of Australia)
- **Brazil** (also written as: Brasil, Federative Republic of Brazil)
- **Canada** (also written as: CA)
- **China** (also written as: People's Republic of China, PRC)
- **France** (also written as: French Republic, Republique francaise)
- **Germany** (also written as: Deutschland, Federal Republic of Germany)
- **India** (also written as: Republic of India, Bharat)
- **Indonesia** (also written as: Republic of Indonesia)
- **Ireland** (also written as: Eire, Republic of Ireland)
- **Italy** (also written as: Italia, Italian Republic)
- **Japan** (also written as: Nippon, Nihon)
- **Kenya** (also written as: Republic of Kenya)
- **Malaysia** (also written as: Persekutuan Malaysia)
- **Mexico** (also written as: United Mexican States, Estados Unidos Mexicanos)
- **Netherlands** (also written as: Nederland, Holland, Kingdom of the Netherlands)
- **New Zealand** (also written as: Aotearoa)
- **Nigeria** (also written as: Federal Republic of Nigeria)
- **Philippines** (also written as: Republic of the Philippines)
- **Singapore** (also written as: Republic of Singapore)
- **South Africa** (also written as: Republic of South Africa, RSA)
- **South Korea** (also written as: Korea, Republic of Korea, ROK)
- **Spain** (also written as: Espana, Kingdom of Spain)
- **Sweden** (also written as: Sverige, Kingdom of Sweden)
- **Thailand** (also written as: Kingdom of Thailand)
- **Turkey** (also written as: Turkiye, Republic of Turkey)
- **United Arab Emirates** (also written as: UAE)
- **United Kingdom** (also written as: UK, Great Britain, Britain)
- **United States** (also written as: USA, US, United States of America)
- **Vietnam** (also written as: Viet Nam, Socialist Republic of Vietnam)

The jurisdictions below are outside this task's country universe:

- **California** (also written as: CA state)
- **New South Wales** (also written as: NSW)
- **Ontario** (also written as: ON)
- **Dubai**
- **Hong Kong** (also written as: Hong Kong SAR, HKSAR)
- **Puerto Rico** (also written as: PR)

The tinting-law axes are:

- **front_side_vlt** - country-specific minimum visible light transmission / transmittance rule for the driver and front passenger side windows, including combined glass-plus-film rules or an explicit national no-rule / subnationally varying statement
- **rear_side_vlt** - country-specific minimum visible light transmission / transmittance rule for rear side windows or rear passenger windows, including any vehicle-class split or no-rule statement
- **windshield_vlt_or_strip** - country-specific windscreen / windshield transparency rule, sun-strip or anti-glare band allowance, clear windshield no-film rule, or explicit national no-rule / subnationally varying statement
- **medical_exception_process** - country-specific medical exemption, permit, certificate, endorsement, approved-doctor, no-exemption process, or explicit national no-process / subnationally varying statement for tinting below the ordinary limit
- **penalty_schedule** - country-specific tinting offense penalty, fine, demerit / penalty points, prohibition, inspection failure, immobilization, summons, equivalent sanction, or explicit national no-penalty / subnationally varying statement
- **enforcement_mechanism** - country-specific enforcement method such as roadside VLT meter testing, inspection / warrant check, authorized inspection centre testing, police / agency examination, or technical-control rejection, or explicit national no-mechanism / subnationally varying statement
- **aftermarket_oem_distinction** - country-specific distinction between aftermarket film / overlay / tinting material and manufacturer / OEM tinted glass, including combined-VLT measurement where applicable, or explicit national no-distinction / subnationally varying statement

Per-axis authoritative-source scope:

- **front_side_vlt** - traffic code, motor-vehicle authority, vehicle inspection authority, or a high-quality legal/compliance mirror that reproduces the jurisdiction-specific front-side threshold or national no-rule / subnational-variation statement
- **rear_side_vlt** - traffic code, motor-vehicle authority, vehicle inspection authority, or a high-quality legal/compliance mirror that reproduces the jurisdiction-specific rear-window threshold or explicit no-rule / vehicle-class split
- **windshield_vlt_or_strip** - traffic code, motor-vehicle authority, vehicle inspection authority, or a high-quality legal/compliance mirror that states the windscreen threshold, strip allowance, or windscreen overlay rule, or national no-rule / subnational-variation statement
- **medical_exception_process** - government medical-driving, permit, licensing, or traffic-code source; a legal mirror or compliance page only when it clearly reproduces the jurisdiction-specific medical exception process
- **penalty_schedule** - traffic-code, police, motor-vehicle authority, official inspection, or legal source that ties the sanction to tint / glazing non-compliance
- **enforcement_mechanism** - traffic-code, police, motor-vehicle authority, inspection authority, or legal source that states how tint / glazing compliance is checked or enforced
- **aftermarket_oem_distinction** - traffic-code, motor-vehicle authority, inspection authority, or high-quality compliance source that distinguishes film / overlay / tinting material from glass, original equipment, or total combined VLT

Official traffic-code, transport / motor-vehicle authority, police, inspection, and government medical-driving pages are preferred. Trade-association, installer, distributor, or aftermarket-compliance pages can work only when they identify the governing jurisdiction-specific legal authority or clearly reproduce the operative legal threshold / process. Wikipedia, unsourced tint charts, generic global tables, and product pages that merely advertise a "legal" shade do not work as sole evidence.

Requirements:
- The page must pin the claimed specific tinting rule for the claimed (country, axis) cell, not only a generic international table, another country's rule, or a subnational rule submitted as national.
- The page must support the claimed axis's required rule type: front-side VLT, rear-window VLT or no-rule statement, windshield threshold / strip rule, medical exception process, penalty schedule, enforcement mechanism, or aftermarket/OEM distinction. For federal or decentralized countries, an explicit national no-rule / subnational-rules-vary statement can satisfy the relevant axis when the page ties that statement to the claimed country and axis.
- The page must support the claimed exact operative claim with enough precision for the relevant axis: threshold direction and percent basis, affected window position, vehicle class, process step, sanction, enforcement method, or film/glass/combined-VLT distinction.
- The page must communicate (possibly via URL among other things) an accepted source class for that axis, with a jurisdiction-specific legal citation or reproduced legal rule when the page is not an official government / legal source.
- The page must provide current legal force, active official guidance, inspection-current framing, publication / update date, or a clearly dated as-of status sufficient for the claim, with no on-page superseded / archived / proposed / pre-effective flag contradicting the claim.

Write one JSON object per line to `results_window_tinting_laws_worldwide.jsonl`:
{"item": { "country": "<country>", "tinting_axis": "<tinting_axis>", "rule": "<rule>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
