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

## `london_maritime_company_operator_fleet`

For each of the 3 role claims listed below, supply public-source evidence for 40+ London-linked maritime vessel companies supporting that claim; for each such role-company pair, cover each of the 3 evidence axes (i.e. 1+ URL per axis).

The scope is intentionally broader than ocean-going shipping: Thames passenger, charter, RIB, tug, barge, waste-river, workboat, offshore, and inland vessel fleets count when the source itself supports London or Thames operating presence and a vessel or fleet role.

Role claims:
- `vessel_owner`: the company owns vessels, is described as a vessel/ship owner, is a registered owner, or is explicitly said to own and operate named vessels or a fleet.
- `ship_or_fleet_manager`: the company provides ship, fleet, technical, crew, commercial, or ISM management for vessels or fleets.
- `fleet_or_vessel_operator`: the company operates vessels, a fleet, routes, river services, charter services, tug/barge/workboat services, waste-river transport, or another public vessel service.

Evidence axes:
- `london_identity`: public evidence that the company has a Greater London registered office, headquarters, office/contact address, explicit London-based management, or explicit London/Thames vessel-operation presence.
- `role_claim_evidence`: public evidence that the company fits the selected `role_claim`.
- `fleet_or_vessel_evidence`: public evidence of concrete vessels, fleet pages, fleet counts, named vessels, vessel classes, tugs, barges, boats, or public fleet operation.

The sources should be fully public, accessible, and usable. Official company pages, Companies House pages, official fleet pages, official PDFs, annual reports, investor reports, and reputable maritime profiles are strongest. UK Chamber, Maritime London, MagicPort, Equasis, TfL, trade directories, and similar surfaces can help when their page text directly supports the relevant axis, but membership labels, snippets, and combined labels such as "Ship Owner / Manager" do not by themselves establish the role or fleet claim. Lead-generation lists, paid contact databases, private revenue/headcount estimates, rankings, and lead scores do not count. Generic logistics, freight forwarding, brokerage, port-only, legal, insurance, consulting, and maritime-services pages do not count unless the page explicitly shows vessel ownership, ship/fleet management, or direct vessel/fleet operation.

Preserve the source's entity wording. Legal entities, trading brands, groups, subsidiaries, SPVs, parents, branch offices, and stale or conflicting fleet-size claims should not be silently normalized or reconciled.

Requirements:
- The page must clearly identify the named company, legal entity, group, or trading brand for the role-company pair.
- The page should visibly fit the selected evidence axis as a source for London identity, role-claim evidence, or fleet/vessel evidence.
- The page must support the selected evidence axis for the named company: London identity for `london_identity`; the selected role for `role_claim_evidence`; concrete fleet, vessel, or public fleet-operation evidence for `fleet_or_vessel_evidence`.

Write one JSON object per line to `results_london_maritime_company_operator_fleet.jsonl`:
{"item": { "role_claim": "<role_claim>", "company": "<company>", "evidence_axis": "<evidence_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
