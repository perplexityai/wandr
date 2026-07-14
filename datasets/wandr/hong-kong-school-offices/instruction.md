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

## `hong_kong_school_offices`

For each of the 25 schools listed below, cover each of the 3 school-office types and supply a source (i.e. 1+ URL) on the school's own website that names the office for that school and exposes a contact email address routed to that office, so the office can be reached directly.

We are lining up outreach for a Global Impact Internship Programme (GIIP) that places high-school students in summer placements at a legal NGO, and we want to reach the right people at each school — the admissions front door, the team that runs activities, and the team that advises students on life after school — rather than a single general enquiries inbox.

The office types, which we refer to as `office`, are:
- `admissions`: the office handling enrolment, applications, prospective-family enquiries, and registration. Admissions / enrolment / registrar pages and "how to apply" / "contact admissions" pages count.
- `activities`: the office or coordinator running the school's co-curricular life — extra-curricular activities (ECA), clubs, after-school programmes, service learning, or student activities. An activities / ECA / co-curricular / clubs page or a named activities-office contact counts.
- `careers`: the office advising students on university applications and careers — university / college counselling, careers guidance, futures, or higher-education advising. A university-counselling / college-counselling / careers / futures page or a named counselling-office contact counts.

Schools in scope (canonical name — accepted aliases):
- **Hong Kong International School** — HKIS, HK International School
- **Canadian International School of Hong Kong** — CDNIS, Canadian International School, CDNIS Hong Kong
- **German Swiss International School** — GSIS, German Swiss International School Hong Kong
- **French International School** — FIS, Lycée Français International, French International School Hong Kong
- **Chinese International School** — CIS, Chinese International School Hong Kong
- **Australian International School Hong Kong** — AISHK, Australian International School
- **Singapore International School (Hong Kong)** — SIS, Singapore International School Hong Kong
- **Korean International School** — KIS, Korean International School Hong Kong
- **Japanese International School** — JIS, Hong Kong Japanese School, Japanese International School Hong Kong
- **Yew Chung International School of Hong Kong** — YCIS, Yew Chung International School, YCIS Hong Kong
- **American International School Hong Kong** — AIS, American International School
- **Harrow International School Hong Kong** — Harrow Hong Kong, Harrow International School HK
- **Nord Anglia International School Hong Kong** — NAIS Hong Kong, Nord Anglia Hong Kong, NAIS HK
- **Kellett School** — Kellett, The British International School in Hong Kong
- **Shrewsbury International School Hong Kong** — Shrewsbury Hong Kong, Shrewsbury International School HK
- **Malvern College Hong Kong** — Malvern College HK, Malvern Hong Kong
- **Discovery College** — DC, Discovery College Hong Kong
- **Renaissance College Hong Kong** — RCHK, Renaissance College
- **ESF King George V School** — KGV, King George V School
- **ESF West Island School** — WIS, West Island School
- **ESF South Island School** — SIS South Island, South Island School
- **ESF Island School** — Island School, ESF Island
- **ESF Sha Tin College** — Sha Tin College, STC
- **ESF West Island School of the Air** — WISA
- **Victoria Shanghai Academy** — VSA, Victoria Shanghai Academy Hong Kong

The cited page should naturally belong to the office in scope and present the email as that office's own contact channel: an admissions / enrolment / registrar page or "contact admissions" panel for `admissions`; an activities / ECA / co-curricular / clubs / after-school page for `activities`; a university-counselling / college-counselling / careers / futures page for `careers`. A general "contact us" page counts only when it labels the listed email as belonging to the office in scope (e.g. an "Admissions" row with its own address) rather than offering a single catch-all enquiries inbox.

The cited page should be fully public, accessible, and usable as a normal page (e.g. not paywall-guarded, login- or app-only shells, or broken pages).

Requirements:
- The page must be on the named school's own official website — its primary domain or a documented subdomain of it. Third-party school directories, listing aggregators, agent or relocation sites, and recruiter pages do NOT count even when they reproduce the email.
- The page must identify the named school in scope — through site branding, page header, or institutional naming — and the office in scope must be the one the listed email is presented as serving, per the definitions above. A bare email with no office attribution does NOT count.
- The page must expose a contact email address shown as the office's own channel — a mailto link or a written-out address tied to that office. A phone number, postal address, or web enquiry form without an email does NOT count, and a personal staff email surfaced only in a directory listing without office attribution does NOT count.

Write one JSON object per line to `results_hong_kong_school_offices.jsonl`:
{"item": { "school": "<school>", "office": "<office>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
