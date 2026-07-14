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

## `earnings_qna_themes`

For 55+ public-company ticker/company pairs, identify at least 3 company-specific themes that recur in analyst Q&A during earnings or results calls dated January 1, 2025 through March 11, 2026. For each company/theme pair, cover 2+ distinct calls; for each call, name 1+ concrete analyst-management Q&A exchange about the theme, with 1+ public transcript-like URL exposing the exchange text.

The target is public evidence of what analysts asked and what management answered, not a ranking, investment view, answer-quality assessment, or recommendation. The theme should be a substantive operating, financial, product, demand, customer, margin, backlog, guidance, capital-allocation, regulatory, or comparable company-specific question pattern visible in the Q&A itself. Very broad labels such as "growth", "outlook", "earnings", or "AI" are too vague unless narrowed to the specific recurring topic shown in the exchange.

Eligible pages should expose the actual speaker-labeled or otherwise clearly attributable Q&A passage: official transcripts, transcript-provider pages, SEC exhibits containing call transcripts, webcast transcript pages, or comparable transcript-like pages can qualify. Earnings releases, event pages, replay-registration pages, slide decks, search results, transcript indexes, investor-relations landing pages, summaries of analyst reactions, and stock commentary do not qualify unless the cited page itself contains the actual analyst question and management answer text.

The transcript's own attribution is the relevant evidence: when it states the analyst and firm, that attribution belongs in the claim; when the questioner is visibly unidentified or the firm is not stated, outside-page enrichment does not count. The metric or KPI language should come from the claimed Q&A exchange or its immediate answer, not from unrelated prepared remarks or later market analysis.

Requirements:
- The page must identify the claimed public company and the claimed earnings or results call, including a call date or fiscal period that places the call within January 1, 2025 through March 11, 2026.
- The page must show the actual analyst or outside-participant question and a management answer from the claimed exchange, rather than only summarizing that a question was asked.
- The exchange must be about the claimed question theme and question focus at a company-specific level.
- The page must support the claimed analyst attribution from the transcript itself, including any claimed analyst firm; an unidentified or unstated marker is acceptable only when that is the page-visible attribution.
- The page must include concrete operating, financial, KPI, customer, product, guidance, backlog, margin, demand, capital-allocation, or comparable metric language in the claimed question or answer.

Write one JSON object per line to `results_earnings_qna_themes.jsonl`:
{"item": { "ticker": "<ticker>", "company": "<company>", "question_theme": "<question_theme>", "fiscal_quarter": "<fiscal_quarter>", "call_date": "<call_date>", "analyst_name": "<analyst_name>", "question_focus": "<question_focus>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
