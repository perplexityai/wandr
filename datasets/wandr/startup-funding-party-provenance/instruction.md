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

## `startup_funding_party_provenance`

For each of the 4 market segments listed below, identify 20+ private or growth-stage companies that announced a Seed, pre-Series A, Series A, Series B, or clearly labeled extensions or bridges of those stages financing during May 8, 2026 through June 22, 2026; for each company, name one institutional investor that participated in the round, and for each such round participation cover each of the 2 announcement sides with a side-substantiating source (i.e. 1+ URL per side).

The work is about public provenance from parties to the financing relationship, not marketing-lead gaps, outreach, lead scoring, contact enrichment, or hiring advice. Funding databases and news roundups can be useful for discovery, but the proof here comes from the company and investor sides themselves.

Market segments:
- `fintech`: financial technology companies, including payments, banking infrastructure, lending, spend management, payroll, insurance, wealth, capital markets, risk, compliance, and related financial workflows.
- `ai_saas`: AI-native or AI-heavy software companies whose main product is sold as software, workflow automation, agents, model tooling, model operations, analytics, or comparable application-layer SaaS.
- `b2b_saas`: business software companies selling recurring software to organizations, excluding cases better classified as fintech, AI-native SaaS, or web3/crypto infrastructure.
- `web3_crypto_infrastructure`: crypto, blockchain, stablecoin, custody, tokenization, wallet, on-chain data, exchange, protocol, and developer infrastructure companies.

Announcement sides:
- `company_side`: a company-issued, company-controlled, or visibly official company release channel statement about the round.
- `investor_side`: an investor-issued or investor-controlled statement about the investor's participation in the round.

A valid company should be plausibly in the claimed market segment and should not be a listed public-company universe row, fund, accelerator, directory, lead list, contact database, or generic news-index entry. A valid round participation uses a real, meaningfully distinct institutional investor or capital provider; broad unlabeled strategic financings, Series C+ growth rounds, debt-only facilities, IPOs, acquisitions, grants, or accelerator acceptances do not count unless the same page also labels the financing as one of the in-scope early-round stages. The amount is useful context when the page states it, but absence of amount does not by itself invalidate an otherwise clear side announcement.

Requirements:
- The page should communicate that it is controlled by or officially issued for the side being cited: for `company_side`, the cited party is `company`; for `investor_side`, the cited party is `investor`. Press-wire publication can pass on `company_side` when the page visibly presents an official company-issued release, such as by naming the company as the release provider. A company release, third-party article, database profile, roundup, generic news index, contact/prospecting directory, or unrelated portfolio directory does not satisfy `investor_side` merely because it quotes or names the investor.
- The page must identify the named company and the named investor as participating in the same claimed financing round, with the claimed round stage or a clear stage-equivalent label.
- The page must communicate an announcement date or page-level publication date inside May 8, 2026 through June 22, 2026.

Write one JSON object per line to `results_startup_funding_party_provenance.jsonl`:
{"item": { "market_segment": "<market_segment>", "company": "<company>", "investor": "<investor>", "round_stage": "<round_stage>", "announcement_date": "<announcement_date>", "announcement_side": "<announcement_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
