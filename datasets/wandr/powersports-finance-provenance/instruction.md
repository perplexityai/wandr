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

## `powersports_finance_provenance`

For 290+ organizations, build a public provenance panel for motorcycle, powersports, or adjacent recreation-vehicle finance. For each organization, cover 2+ of the evidence surfaces below with at least 1+ URL per surface.

Evidence surfaces:
- `powersports_offering`: official or primary evidence that the organization offers or administers motorcycle, powersports, or adjacent recreation-vehicle financing
- `private_party_support`: source-stated direct or dealer-mediated support for private-party, private-seller, individual-seller, person-to-person, rider-to-rider, or equivalent purchases tied to an in-scope vehicle class
- `access_eligibility`: descriptive access, eligibility, availability, membership, geography, or authorized-dealer-network provenance tied to the organization or finance program
- `partner_dealer_relationship`: public evidence of an existing dealer program, marketplace listing, lender-network participation, API, embedded-finance, or integration relationship tied to powersports or adjacent vehicle finance

This is public provenance of what sources say. It is not a lender ranking, rate comparison, suitability judgment, partner target list, contact search, lead-enrichment exercise, or outreach plan. Organizations can qualify through partial but meaningful public powersports-finance evidence rather than every listed surface.

Official or primary-source pages include organization-owned product pages, branded finance-program pages, membership or availability pages, dealer-program pages, official marketplaces, API/developer pages, lender-network surfaces, and named counterparty integration pages. Generic personal-loan pages with no motorcycle, powersports, or clearly in-scope recreation-vehicle class do not count; affiliate rankings, consumer advice articles, comparison listicles, forums, social posts, event-sponsor pages, target lists, contact lists, and outreach/enrichment surfaces do not count.

Requirements:
- The page must identify the claimed organization, branded finance program, or named relationship counterparty clearly enough to tie the evidence to that organization.
- The page must fit the claimed `evidence_surface`: `powersports_offering` for direct offering proof; `private_party_support` for source-stated direct or dealer-mediated private-party / private-seller / rider-to-rider support; `access_eligibility` for descriptive geography, membership, availability, or authorized-dealer-network access evidence; and `partner_dealer_relationship` for existing named dealer, marketplace, lender-network, API, embedded-finance, or integration relationship evidence.
- The page must provide a concrete source-stated finding for the claimed surface and tie that finding to motorcycle, powersports, recreation-vehicle, outdoor vehicle/equipment, RV, marine, dealer F&I, lender-routing, or comparable vehicle-finance context.

Write one JSON object per line to `results_powersports_finance_provenance.jsonl`:
{"item": { "organization": "<organization>", "evidence_surface": "<evidence_surface>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
