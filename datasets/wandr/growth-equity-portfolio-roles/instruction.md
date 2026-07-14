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

## `growth_equity_portfolio_roles`

For each of the 12 investment firms listed below, identify 8+ public sponsor-role relationships per firm, where each relationship ties a named firm person to a named portfolio company; for every such (`investment_firm`, `person`, `portfolio_company`) relationship and each of the 2 evidence sides listed below, supply a relationship-substantiating source (i.e. 1+ URL).

The work is public relationship provenance for software/growth-equity sponsor involvement, not contact sourcing, private biography, CRM enrichment, outreach targeting, email/phone collection, or LinkedIn harvesting.

Investment firms in scope:
- **Level Equity** (also written as: Level, Level Equity Management, Level Equity Management LLC)
- **JMI Equity** (also written as: JMI, JMI Management, JMI Management LP, JMI Equity Management)
- **Summit Partners** (also written as: Summit, Summit Partners LP)
- **Spectrum Equity** (also written as: Spectrum, Spectrum Equity Management)
- **LLR Partners** (also written as: LLR)
- **Silversmith Capital Partners** (also written as: Silversmith)
- **FTV Capital** (also written as: FTV)
- **Mainsail Partners** (also written as: Mainsail)
- **Guidepost Growth Equity** (also written as: Guidepost, Guidepost Growth, Guidepost Growth Equity LLC)
- **PSG Equity** (also written as: PSG, Providence Strategic Growth)
- **Updata Partners** (also written as: Updata)
- **NewSpring Capital** (also written as: NewSpring)

The evidence sides of interest, which we refer to as `evidence_side`, are:

- `firm_role_side`: firm-authored or firm-controlled public evidence that ties `person` to `portfolio_company` or to a portfolio-company role.
- `portfolio_company_acknowledgment`: portfolio-company-owned or visibly portfolio-company-issued evidence acknowledging the sponsor/company relationship, investment/backing, financing, acquisition, board representation, co-investor relationship, or the same named person when available.

A valid role relationship is a public sponsor-side role, assignment, investment, board, observer, director, deal-team, operating/portfolio-support, works-with, serves-on, supports, or comparable wording tied to the named portfolio company. The portfolio-company side may prove the firm/company relationship even when it does not name the exact person. Public wording such as `board member`, `board observer`, `former`, `Level Team`, `operating partner`, `growth investment`, or `co-investor` remains meaningful as stated, rather than being converted into private contact or CRM categories. The cited page should be fully public and usable; contact-enrichment databases, stale org-chart/profile scrapers, generic business articles, and ordinary LinkedIn pages are not provenance substitutes for the side-specific source role.

Requirements:

- For `firm_role_side`, the URL must be a firm-owned, firm-authored, or firm-controlled source for `investment_firm`; for `portfolio_company_acknowledgment`, the URL must be owned by the portfolio company or visibly issued by the portfolio company.
- For `firm_role_side`, the page must identify the named `person` and `portfolio_company` and connect them in the same public role relationship; for `portfolio_company_acknowledgment`, the page must identify the `investment_firm` and `portfolio_company`, while naming the exact `person` is helpful but not required.
- For `firm_role_side`, a firm portfolio grid or company list without named person-role evidence is not enough; for `portfolio_company_acknowledgment`, a pure firm-owned page, generic news article, LinkedIn page, stale org chart, contact database, or generic aggregator is not enough.

Write one JSON object per line to `results_growth_equity_portfolio_roles.jsonl`:
{"item": { "investment_firm": "<investment_firm>", "person": "<person>", "portfolio_company": "<portfolio_company>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
