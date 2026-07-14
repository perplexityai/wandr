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

## `swedish_invoice_finance`

For 120+ Swedish-market or Sweden-serving Nordic providers of invoice finance, factoring, receivables purchase, invoice discounting, reverse factoring / supply-chain finance, or adjacent SME working-capital finance, name at least 1 concrete public service, product, marketplace, embedded-finance, or source-stated channel/program surface per provider and supply each of the 2 evidence roles for every provider-service surface (1+ URL per role).

The evidence roles are:
- `service`: public service, product, marketplace, embedded-finance, or concrete channel/program evidence.
- `identity`: public legal, FI/regulatory, company-registration, official legal-information, annual-report, or comparable identity evidence.

The task asks for public evidence, not affiliate targeting, partner recommendation, meeting-list building, reseller pitching, financial advice, contact discovery, outreach planning, lead scoring, or contact enrichment. Public channel, partner, program, referral, marketplace, or integration evidence is useful only when a source states a concrete surface; generic partner language and inferred fit are not enough.

Requirements:
- The page must clearly bind the cited evidence to the named provider-service surface.
- The page must visibly fit the role declared by `evidence_role`: `service` pages are primary public service, product, marketplace, embedded-finance, or concrete channel/program surfaces for the provider; `identity` pages are public legal, FI/regulatory, company-registration, official legal-information, annual-report, or comparable identity surfaces tying the provider brand to a legal or registered entity.
- The page must satisfy the declared role's content bar: `service` evidence states an eligible invoice-finance or adjacent SME working-capital finance service and a Sweden / Sweden-serving Nordic market tie; `identity` evidence states legal name, FI/regulatory posture, registration, licensed/registered status, or comparable public identity information for the provider.

Write one JSON object per line to `results_swedish_invoice_finance.jsonl`:
{"item": { "provider": "<provider>", "service_surface": "<service_surface>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
