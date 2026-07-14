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

## `payment_integrity_service_lines`

For 25+ current healthcare payment-integrity vendors as of June 2026,
name 4+ distinct first-class payment-integrity offerings
per vendor and supply 1+ official public URLs for each vendor/capability
pair. A qualifying offering has its own vendor-presented identity: a named
product, module, platform, package, service line, or service offering. That
identity can appear on a dedicated product/solution page, navigation/menu
entry, product sheet, brochure, or distinct solution card/block when the label
has its own operational description. Loose workflow phrases, feature/benefit
labels or cards, stitched descriptions, metrics, use-case headings, and
sections inside another offering do not count.

Vendor identity should use the current vendor, current parent, or maintained
brand. Legacy or acquired names visible on current pages are aliases or context,
not separate vendors when they are now part of the same current vendor family.

Sources must be public first-party surfaces controlled by the submitted vendor
or its current parent/maintained brand family. Product or brand pages, official
press releases, vendor-authored PDFs/brochures, and comparable vendor-owned
pages qualify. Each URL must independently prove the submitted vendor/capability
pair. Analyst reports, marketplace or procurement summaries, press-wire
republications, third-party news, login-only pages, generic redirects, and pages
owned by a different entity do not qualify. A broader suite or overview page
works only when it separately presents the submitted capability as a first-class
offering identity, not merely as a suite banner, feature, or benefit card.

The target is breadth within each vendor's payment-integrity offerings, not only
subrogation offerings. Recovery and responsibility language matters when the
page explicitly says it; silence is not a no-recovery claim.

Requirements:
- The page must tie the submitted vendor and capability to healthcare payer,
  health-plan, TPA, government-program, or comparable medical-claims payment
  integrity work: payment accuracy, program integrity, improper-payment review,
  claim audit, payer responsibility, or similar.
- The page must identify the capability as a first-class vendor-presented
  payment-integrity offering, not merely a suite banner, generic
  savings/analytics/workflow/consulting/transformation/payer-services language,
  a feature/benefit label or card, use-case heading, or stitched phrase.
- The page must expose at least two capability-specific operational details,
  for example claim stage, reviewed data, audit target, workflow,
  payer-responsibility or recovery method, product component, line of business,
  or operational outcome.
- If the vendor/capability pairing depends on a current-parent, legacy,
  acquired, or maintained-brand relationship, the page must support that
  relationship.
- If you characterize the offering as recovery- or
  payment-responsibility-oriented, the page must explicitly support that
  characterization through language such as recovery, COB/TPL, subrogation,
  other-party/third-party liability, payer responsibility, overpayment
  recovery, credit balance, MSP, workers' compensation, or legal recovery.

Write one JSON object per line to `results_payment_integrity_service_lines.jsonl`:
{"item": { "vendor": "<vendor>", "capability": "<capability>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
