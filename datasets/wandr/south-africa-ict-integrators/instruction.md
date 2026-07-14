You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `south_africa_ict_integrators`
  - `south_africa_ict_integrators.public_credentials`
  - `south_africa_ict_integrators.hard_public_evidence`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `south_africa_ict_integrators`

For 120+ South Africa-operating ICT systems integrators, managed service providers, network / security / cloud / data-centre / telecom integrators, ICT infrastructure firms, or local subsidiaries / divisions, supply an official or owned identity source (i.e. 1+ URL per company) that anchors the company as a public ICT service provider in South Africa.

Blue Networks and Infrastructure is only an anchor example. The work is public provenance: no competitor rankings, supplier recommendations, procurement advice, sales strategy, contact lookup, outreach, lead scoring, or contact enrichment.

Official or owned identity sources include company websites, official local subsidiary or division pages, official capability pages, official reports, and other company-controlled public surfaces. Directories, listicles, LinkedIn, commercial company databases, trade articles, and procurement records can help discovery or later evidence facets, but they do not satisfy this identity-source task.

Requirements:
- The page must communicate that it is an official or owned identity source for the named company, local subsidiary, or local division.
- The page must establish a South Africa operating footprint for the named company, local subsidiary, or local division.
- The page must state a qualifying ICT service identity: systems integration, managed services, network integration, cybersecurity services, cloud or data-centre services, telecom integration, ICT infrastructure delivery, or a closely equivalent source-stated service role.

Write one JSON object per line to `results_south_africa_ict_integrators.jsonl`:
{"item": { "company": "<company>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `south_africa_ict_integrators.public_credentials`

Cross-tasknode identifier discipline: this task is for the same {= company =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For the same South Africa ICT companies, cover 1+ of the public credential facets below for each company by supplying a facet-fit source (i.e. 1+ URL under each facet).

Use source-stated wording for B-BBEE levels, ownership facts, vendor labels, partner tiers or designations, dates, legal names, geography, and service categories. Collect positive credential evidence only: do not submit no-BBBEE-source, no-partner-tier-source, no-headcount-source, no-date, or similar absence rows. The work remains public provenance, not ranking, supplier recommendation, procurement advice, sales strategy, contact lookup, outreach, lead scoring, or contact enrichment.

Public credential facets:
- `transformation_credential`: a public source naming the company and stating B-BBEE level, black ownership, black-woman ownership, certificate, affidavit, scorecard, procurement-recognition, or transformation status. Self-published official evidence can count; independent registry confirmation is not required.
- `vendor_channel_evidence`: a vendor-controlled locator or program page, vendor directory, official company partner page, or reputable channel / ICT trade source naming a vendor relationship, accreditation, specialization, partner status, designation, or award. Exact tier and status labels are source-stated text, not objective rank.

Directories, listicles, LinkedIn, and commercial company databases can help discovery or secondary context, but they should not satisfy these positive facets merely by listing the company.

Requirements:
- The page must clearly name the company, local subsidiary, or local division in scope.
- The page must make its credential source role visible for the declared `credential_facet`.
- The page must contribute positive source-stated credential evidence scoped to the declared `credential_facet`, not merely repeat the company's existence, generic service menu, logo wall, ranking opinion, or missing-source status.

Write one JSON object per line to `results_south_africa_ict_integrators.public_credentials.jsonl`:
{"item": { "company": "<company>", "credential_facet": "<credential_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `south_africa_ict_integrators.hard_public_evidence`

Cross-tasknode identifier discipline: this task is for the same {= company =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For the same South Africa ICT companies, cover 2+ of the hard public evidence facets below for each company by supplying a facet-fit source (i.e. 1+ URL under each facet).

Use source-stated wording for procurement roles, public-delivery references, trade-source framing, capability claims, customer or project names, dates, legal names, geography, and service categories. Collect positive hard public evidence only: do not submit no-BBBEE-source, no-partner-tier-source, no-headcount-source, no-date, or similar absence rows. The work remains public provenance, not ranking, supplier recommendation, procurement advice, sales strategy, contact lookup, outreach, lead scoring, or contact enrichment.

Hard public evidence facets:
- `public_delivery_procurement`: a public tender, bidder list, award, panel, RFP, deviation, contract notice, public procurement dataset, SITA / procuring-entity document, or public-sector delivery reference naming the company in an ICT / network / cloud / security / telecom scope.
- `independent_trade_recognition`: an editorial, trade-press, or reputable press source naming the company and an ICT service, implementation, award, partnership, deployment, rebrand, acquisition, contract activity, or market activity.
- `substantive_capability_reference`: a source showing a concrete capability instance, such as a named deployment, case study, technical certification or specialization, managed-service designation, public customer reference, or technical service surface. Generic services-menu bullets and logo walls do not satisfy this facet.

Directories, listicles, LinkedIn, and commercial company databases can help discovery or secondary context, but they should not satisfy these positive facets merely by listing the company.

Requirements:
- The page must clearly name the company, local subsidiary, or local division in scope.
- The page must make its hard-evidence source role visible for the declared `hard_evidence_facet`.
- The page must contribute positive substantive evidence scoped to the declared `hard_evidence_facet`, not merely repeat the company's existence, generic service menu, logo wall, ranking opinion, or missing-source status.

Write one JSON object per line to `results_south_africa_ict_integrators.hard_public_evidence.jsonl`:
{"item": { "company": "<company>", "hard_evidence_facet": "<hard_evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
