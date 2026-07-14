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

## `regulated_messaging_fees`

For 35+ vendors that sell programmable business messaging or notification services through at least one regulated messaging channel, supply source-stated public fee, compliance, and developer-channel evidence for every listed evidence kind, with 5+ distinct evidence-kind rows per vendor and 1+ URL per vendor/evidence-kind row. Do not count a vendor unless you can support both the `carrier_or_network_fee` row and the `registration_or_compliance_fee` row with vendor-tied public evidence.

The useful work is the public evidence anatomy around regulated messaging costs and compliance: headline usage prices, named carrier or network pass-throughs, sender assets, registration/compliance fee or process surfaces, and API/channel claims often live on different pages. Preserve the source's wording and time context; do not calculate total cost, rank vendors, recommend vendors, estimate engineering effort, or give legal/procurement advice.

The evidence kinds of interest, reported as `evidence_kind`, are:
- `usage_pricing`: public usage price, rate unit, volume tier, bundled credit, or source-stated price-publication state for a regulated messaging channel.
- `carrier_or_network_fee`: explicit carrier, network, pass-through, surcharge, or regime fee anatomy affecting message delivery, including a named fee component, carrier/regime, amount, unit, pass-through rule, or source-stated at-cost/not-itemized state.
- `sender_or_number_fee`: fee or public state for a sender identity, phone number, toll-free number, short code, 10DLC number, sender ID, WhatsApp sender, RCS agent, or comparable regulated sender asset.
- `registration_or_compliance_fee`: named registration, verification, compliance fee, approval process, penalty schedule, or vendor-managed compliance workflow tied to a regulated messaging program.
- `developer_channel_claim`: developer, API, SDK, webhook, integration, or channel-doc claim showing programmable access to the regulated messaging channel; generic API docs do not substitute for fee evidence kinds.

Eligible channels include SMS, MMS, RCS, WhatsApp Business, toll-free SMS, short codes, 10DLC, sender IDs, local phone numbers, and comparable regulated sender assets. Pure push, email, web, or in-app notification sources do not count unless the page also gives relevant regulated messaging evidence.

Vendor-owned pricing pages, support/help-center articles, developer docs, compliance guides, product pages, terms pages, vendor blogs, and public changelogs are the normal source base for vendor-specific claims. For `carrier_or_network_fee`, the page must expose a carrier/network/pass-through/surcharge/regime fee component, rule, table, named carrier/regime, amount, unit, or source-stated at-cost/not-itemized state; a generic pricing-page footnote that fees may apply is not enough by itself. For `registration_or_compliance_fee`, the page must expose a named registration, verification, approval, campaign, toll-free verification, sender-registration, penalty, managed-compliance workflow, or fee/public-state tied to the vendor's regulated messaging service. Carrier, registry, or industry-body pages can count only when the page itself ties the fee or rule to the vendor/service being recorded. Reputable communications-platform articles can support dated public-source contrast, but they should not replace a current vendor/source statement for vendor-specific pricing or API claims.

For each row, record the source-stated product/service, channel, fee or claim component, public amount or public state, unit/frequency, volume tier or threshold when stated, compliance regime/program when stated, source class, visible source/effective date when present, checked date, confidence, and brief notes for contact-sales, at-cost pass-through, not-itemized, no-visible-date, name-conflict, or price-not-public states.

Requirements:
- The page must tie the vendor or cited service to a regulated business messaging channel, not merely push, email, in-app messaging, or generic notification tooling.
- The page must fit the declared `evidence_kind`.
- The page must state the public amount, unit, frequency, tier, source-stated public-price state, named fee/pass-through component, compliance process/fee/claim, or developer/API/channel claim being recorded; inferred absence, TCO math, rankings, recommendations, and advice do not count.
- A broad pricing page can support multiple evidence kinds only when the submitted excerpts isolate the specific section, table, fee component, or process text for the declared evidence kind. A generic API/developer page can pass `developer_channel_claim`; it does not pass pricing, carrier/network, sender/number, or registration/compliance evidence unless the relevant fee/process claim is actually visible on that page.
- The row must preserve enough public time context for the source claim: a visible source date, update/effective date, current pricing-page state, or a no-visible-date state recorded with the checked date.

Write one JSON object per line to `results_regulated_messaging_fees.jsonl`:
{"item": { "vendor": "<vendor>", "evidence_kind": "<evidence_kind>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
