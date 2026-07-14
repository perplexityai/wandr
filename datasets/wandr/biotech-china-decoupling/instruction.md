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

## `biotech_china_decoupling`

For at least 260+ dated U.S. biotech-China decoupling signal events, classify each event under one of the closed source types listed below and supply a source URL for each event (i.e. 1+ URL). The ledger should represent at least 5 distinct source types overall, but sparse source classes do not need the same number of events as source-rich classes. The evidence window is January 1, 2024 through June 27, 2026; record the checked date as 2026-06-27.

This is a public-evidence ledger, not a legal, procurement, supplier-risk, geopolitical, or investment recommendation. Each signal should preserve the page's own date, issuer or source entity, source side, directly supported event or statement, signal/action status, any directly named Chinese counterparty, any directly supported U.S. company or public official, affected biotech/CDMO/data/manufacturing/supply-chain category when stated, stated rationale when stated, and a short raw excerpt.

The closed `source_type` values are:
- `proposed_legislation`: Official bill text, bill-status page, or legislative page for a proposed U.S. law or amendment.
- `enacted_policy_or_implementation`: Official enacted law, Federal Register notice, agency designation, OMB/FAR, or similar implementation source.
- `committee_or_commission_statement`: House Select Committee, NSCEB, or comparable U.S. committee or commission statement, report, letter, or hearing material.
- `industry_association_statement`: Industry association page or statement showing association posture, advocacy, or membership action.
- `company_disclosure_or_action`: U.S. company-controlled filing, press release, investor presentation, transcript, or official company page.
- `counterparty_response`: Chinese counterparty-controlled statement, filing, press release, open letter, or divestiture/action notice.
- `secondary_analysis_context`: Dated reputable reporting or analysis used only as labeled context or a discovery lead.

The closed signal/action status labels are:
- `proposed_law`: The source supports proposed legislation or a legislative proposal, not enacted implementation.
- `enacted_or_implementation_policy`: The source supports enacted law, implementation, designation, or official policy execution.
- `association_posture_or_membership_action`: The source supports industry-association posture, advocacy, or membership action.
- `explicit_company_termination`: A company-controlled source directly states a completed termination or exit from a named relationship.
- `diversification_or_transition_plan`: A company-controlled source supports supplier diversification, transition, replacement, or manufacturing plan language.
- `conditional_exit_or_termination_right`: The source supports termination-right, conditional-exit, effective-date, grandfathering, or may-terminate language rather than a completed exit.
- `risk_disclosure_only`: The source supports risk disclosure about China, BIOSECURE, foreign-adversary biotech, CDMO concentration, or a named counterparty without action.
- `continuing_relationship`: The source supports a continuing relationship, ongoing program, extension, current reliance, or no-current-impact statement.
- `counterparty_response_or_counterparty_action`: The source supports a Chinese counterparty response, denial, membership exit, divestiture, sale, or counterparty-only action.
- `secondary_only_claim`: The source is secondary reporting or analysis and cannot by itself prove company-controlled action.
- `stale_or_conflicting_evidence`: The source is stale relative to later official/current evidence or directly conflicts with another cited source.
- `no_company_specific_action_supported`: The source itself does not directly support any U.S. company-specific action.

Do not use one source side to prove another side's action. A House committee page can prove committee framing and named targets, not a U.S. company supplier termination. A counterparty statement can prove the counterparty's response or action, not a customer exit unless it directly states that exit. Secondary reporting is secondary-only context unless backed by company-controlled evidence in a separate row.

Positive source surfaces include official bill/law/status text, Federal Register or agency implementation notices, House Select Committee or NSCEB materials, BIO or comparable association statements, SEC filings, official company releases or investor materials, Chinese counterparty official statements or filings, and dated reputable secondary reporting used as context. Generic China policy, broad pharma reshoring commentary, vague risk boilerplate, law-firm client alerts substituting for official policy text, unnamed supplier language converted into named counterparties, and advice or risk scores do not count.

Requirements:
- The page must match the submitted source type by issuer, page class, and source side.
- The page must directly support the dated event or statement being recorded.
- The page must contain a concrete U.S. biotech-China decoupling tie, such as BIOSECURE, foreign-adversary biotech, Chinese CDMOs or suppliers, biological/genomic data, biomanufacturing, supply-chain reliance, named Chinese counterparties, or comparable separation pressure.
- The page must directly support the submitted signal/action status without upgrading weaker evidence into a stronger company-action claim.
- Any submitted Chinese counterparty, U.S. company, public official, source entity, supply-chain category, or rationale must be directly supported by this same page.

Write one JSON object per line to `results_biotech_china_decoupling.jsonl`:
{"item": { "signal_event": "<signal_event>", "source_type": "<source_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
