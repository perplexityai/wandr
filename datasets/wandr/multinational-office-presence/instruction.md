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

## `multinational_office_presence`

Cross-border BD, corporate-development, and commercial-real-estate workflows often start by mapping the per-country granular face of a multinational corporation's operational footprint — not just whether the company has an office in country X, but who runs that country office and where exactly it is, on per-company authoritative surfaces rather than third-party aggregator estimates.

For at least 100+ genuinely multinational companies, for each of 5 countries in the company's office footprint, for each of 2 info aspects of the company's office in that country, supply at least 1 URL per (company, country, info) row from a current company-controlled page or authoritative corporate disclosure that substantively evidences the row's info aspect for the row's company in the row's country.

The info aspects are:
- **local_head** — the named individual heading the country office for the claimed company in the claimed country — country CEO / regional managing director / regional president / country general manager / managing partner for the country / office administrator for the country, with a country-leadership-role anchor tying the named individual to the country office (not the global CEO, and not a region-wide chair such as `EMEA Chair` whose remit spans many countries).
- **local_office_address** — the country office's physical street address — street + city, or full postal block (street, city, postal code, country) — that the page presents as the company's own office address in the claimed country. A bare city name with no street is not enough; the page must communicate a street-level or building-level address line for the office.

Use office, location, contact, careers-location, team, leadership, or per-person bio pages from the company itself, or corporate disclosures such as annual reports, 10-K Item 2 property listings, or investor real-estate / office-footprint disclosures. Third-party office directories, one-off job postings, historical opening announcements, generic market articles, scraped location databases, and social-media profiles do not count. A single (company, country) cell's two info-aspect URLs can be the same page when the page substantively carries both (an offices page that also names the country lead, for instance), or two different pages — both shapes are first-class.

The country axis is closed-canon to the following 28-country roster (the realistic per-(company, country) universe top multinationals actually publish per-country office entries for):

- **United States** — also written as USA, U.S.A., U.S., US, United States of America, America, Estados Unidos.
- **Canada** — also written as CA, CAN.
- **United Kingdom** — also written as UK, U.K., Great Britain, Britain, England, GB, GBR.
- **Germany** — also written as Deutschland, DE, DEU, Federal Republic of Germany.
- **France** — also written as FR, FRA, République française, French Republic.
- **Italy** — also written as IT, ITA, Italia, Italian Republic.
- **Japan** — also written as JP, JPN, 日本, Nippon, Nihon.
- **Spain** — also written as ES, ESP, España, Kingdom of Spain.
- **Netherlands** — also written as NL, NLD, Nederland, Holland.
- **Belgium** — also written as BE, BEL, België, Belgique.
- **Switzerland** — also written as CH, CHE, Suisse, Schweiz, Svizzera.
- **Ireland** — also written as IE, IRL, Éire, Republic of Ireland.
- **Sweden** — also written as SE, SWE, Sverige, Kingdom of Sweden.
- **Poland** — also written as PL, POL, Polska, Republic of Poland.
- **China** — also written as CN, CHN, People's Republic of China, PRC, 中国, 中華人民共和國, Mainland China.
- **Hong Kong** — also written as HK, HKG, Hong Kong SAR, 香港.
- **Singapore** — also written as SG, SGP, Republic of Singapore.
- **India** — also written as IN, IND, Bharat, भारत, Republic of India.
- **Australia** — also written as AU, AUS, Commonwealth of Australia.
- **South Korea** — also written as KR, KOR, Republic of Korea, ROK, 대한민국, 한국.
- **Mexico** — also written as MX, MEX, México, United Mexican States, Estados Unidos Mexicanos.
- **Brazil** — also written as BR, BRA, Brasil, Federative Republic of Brazil, República Federativa do Brasil.
- **Argentina** — also written as AR, ARG, Argentine Republic, República Argentina.
- **United Arab Emirates** — also written as UAE, U.A.E., AE, ARE, Emirates, الإمارات العربية المتحدة.
- **Saudi Arabia** — also written as SA, SAU, KSA, Kingdom of Saudi Arabia, المملكة العربية السعودية.
- **South Africa** — also written as ZA, ZAF, RSA, Republic of South Africa.
- **Turkey** — also written as TR, TUR, Türkiye, Republic of Türkiye, Republic of Turkey.
- **Indonesia** — also written as ID, IDN, Republic of Indonesia.

Submissions naming a country outside this roster fail the country canon. Bare ambiguous strings (such as plain `Korea` for South Korea) also fail; use the canonical short name from the roster. Regional buckets (`EMEA`, `APAC`, `Latin America`, `MENA`) are not single-country jurisdictions and fail the canon — submit the specific country whose office is being communicated. Pages may surface the country via native-language naming (`Estados Unidos`, `Deutschland`, `中国`), ISO 3166 codes, or a city-only entry in a city unambiguously inside the country (`Tokyo` for Japan, `Frankfurt` for Germany); the row's `country` value must be the canonical short name from the roster.

Requirements per row:
- The page must identify the same company as the organization whose country-office head or country-office address is being communicated.
- The page must tie the row's info content (the named country-office head, or the country-office street address) to the row's country — country-anchoring on the row's single country, not a regional rollup or a different country's content.
- The page must substantively evidence the row's claimed info aspect for the row's (company, country) cell — a named individual with a country-leadership-role anchor on `local_head` rows, or a street-level physical address line on `local_office_address` rows.

Write one JSON object per line to `results_multinational_office_presence.jsonl`:
{"item": { "company": "<company>", "country": "<country>", "info": "<info>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
