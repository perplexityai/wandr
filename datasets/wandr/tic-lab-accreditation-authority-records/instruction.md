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

## `tic_lab_accreditation_authority_records`

For 70+ distinct TIC provider brands or corporate groups, supply at least 1 concrete formal lab accreditation, recognition, notified-body, testing-lab, scope-expansion, or authority-appointment packet per provider. Each provider/event packet needs one source for each of the 2 evidence roles. Provider diversity is the volume driver: target 70-85 scored provider packets at or above the 70-provider floor, and spend surplus effort on new provider packets rather than extra events for one provider or repeated source-family patterns.

Provider-packet discipline:
- Before writing the final answer, build a private provider packet ledger. Each ledger row is one candidate provider packet with: global provider group/brand, shared event/status label, company-side URL, authority-side URL, legal entity/site/body details, recognition family, and a keep/replace decision.
- Build 90-105 candidate provider packets first, then keep 70-85 distinct-provider packets in the final answer, using the candidate buffer to replace weak one-side packets and bias toward the upper end of that range so ordinary judging losses still leave at least 70 qualified provider brands.
- Treat 70 as the accepted-provider floor after judging, not the final-output target. A final answer aiming at only 70 providers is fragile and likely incomplete.
- Use the same stable `provider_brand` and the same `event_or_recognition_title` in both role records. `provider_brand` is the global provider group/brand being evidenced, not a lab-site suffix, authority name, certificate number, notified-body number, directory name, accreditation program, or source-owner label.
- Treat `event_or_recognition_title` as the shared packet label. Certificate numbers, lab IDs, body numbers, sites, dates, scope expansions, and standards belong in `answer`/`excerpts` unless both role URLs visibly support that exact detail.
- If one side only supports a broader current status while the other exposes a narrower ID/date/site/scope record, use the broader shared status as the event title or find a sharper paired source. Do not submit an authority-only detail as if the company source also proved it.
- Keep event titles source-faithful and same-event: if both pages only prove broad ISO/IEC 17025 accreditation or current notified-body status, title the packet at that broad level. Do not title it as a specific authority, legislation, program, site, scope, date, or certificate unless both cited pages visibly show that same detail.
- Count a candidate packet as keepable only when both role rows independently have role-appropriate support before final output: the company-side URL must visibly support the provider/legal entity and the shared recognition family from provider-controlled material, and the authority-side URL must visibly support the same provider/legal entity or body and recognition family from an official authority-side record. If either role is source-weak, broad, generic, or only matched by inference from the other row, drop both rows for that one-side-weak packet and replace the whole packet in the ledger rather than hoping extra rows will compensate.
- Every kept provider packet must become exactly two adjacent final JSONL rows with identical `provider_brand` and identical `event_or_recognition_title`: one `company_announcement` row and one `authority_record` row. Do not rely on separated rows, later explanations, tables, or duplicate events to make the pair obvious.
- Do not emit singleton authority directories, singleton provider announcements, duplicate role rows, authority-only packets, company-only packets, or packets whose two rows use different provider/event keys. Replace those packets in the private ledger before final output.
- A final answer with fewer than 70 provider brands that each have both `company_announcement` and `authority_record` rows is under-buffered, even if some providers have multiple events; below 70 paired providers is incomplete.
- Do not submit a second event for any provider until at least 70 distinct provider brands each have one clean two-role packet. Before final output, discard surplus events, site/lab/certificate/scope rows, and legal-entity variants from already-used provider families while the provider buffer is unmet.
- Treat source-family clustering as a final-output smell, not a source ban. Large authority registries such as A2LA, OSHA, NANDO, UKAS, and IECEE, and large TIC groups such as Element, Eurofins, Intertek, SGS, Bureau Veritas, and TUV, can supply valid paired row evidence for distinct provider/event packets, but they must not become the answer pattern while the provider buffer is unmet.

Hard packet-output gate: the final answer must contain adjacent two-row JSONL blocks for 70-85 distinct provider brands whenever possible, and never fewer than 70 distinct provider brands with both roles. Each block has exactly one `company_announcement` row followed immediately by exactly one `authority_record` row for the same `provider_brand` and `event_or_recognition_title`, so the judged result can still clear the 70 accepted-provider floor after ordinary citation losses. Never stop after 6, 9, 16, 18, 20, 24, 26, 32, 45, 50, or 60 provider brands if more paired packets remain available. If your draft has singleton rows, duplicate/source-family padding, one-side-weak packets, repeated providers before 70 distinct provider brands, or fewer than 140 paired-role rows, repair the private ledger and add new provider packets before writing any explanation, caveat, table, or second event for an existing provider.

Final-output compaction contract:
- This task is scored on distinct `provider_brand` packets, not on total certificates, total lab sites, total events, or total rows. It is not asking for a 150-event, 160-packet, or 300-row certificate-mining sweep. A 200-row answer with only 20 provider brands is worse than a compact 140-row answer with 70 provider brands.
- Until 70 distinct provider brands are keepable, the final file should have exactly one two-row packet per provider brand. Delete extra Element, SGS, Eurofins, Intertek, TUV, Bureau Veritas, UL, DEKRA, or other repeated-provider events before deleting distinct-provider packets.
- The required file should be JSONL-first and JSONL-only: no prose preamble, methodology, caveats, markdown tables, rankings, provider summaries, or explanatory paragraphs in place of rows. Use compact one-line JSON objects with one or two short quote-like excerpts per row.
- The only acceptable final packet shape is two adjacent rows: first `company_announcement`, then `authority_record`, with identical `provider_brand` and identical `event_or_recognition_title`. Start the next provider only after the two rows for the current provider are complete.
- Before finalizing, recount after all deletions and deduplication: number of distinct provider brands with at least one clean adjacent company row and authority row under the same event label. If that count is below 70, the draft is not ready; keep finding new provider brands instead of adding rows for already-used providers.

Pair-lock self-audit before final output:
- For every kept provider packet, first read the two rows together. Both URLs must support the same provider/legal entity and the same broad event/status label without relying on details visible on only one side.
- If the authority row supports an OSHA expansion, NANDO designation, A2LA certificate, IECEE/CBTL status, NRTL status, or similar formal status, the company row must visibly support that same recognition family for that same provider/legal entity. A different accreditation, lab capability, unrelated news item, or generic approvals page is not a match.
- For NANDO and similar official authority records, use the body/detail record or PDF only when the cited page visibly shows the submitted provider/body, identifier, legislation/program/family, and status. Generic NANDO free-search shells, broad indexes, and official PDFs for the wrong-legislation or wrong program do not support an authority row.
- Use a broad shared `event_or_recognition_title` when it is safer, such as "OSHA NRTL recognition", "A2LA ISO/IEC 17025 accreditation", or "EU MDR notified body designation". Do not put certificate numbers, sites, dates, standards, or scope expansions in the title unless both role URLs visibly support those exact details.
- Each row's `excerpts` must include exact source phrases or compact quote-like snippets naming the provider/legal entity and the formal status, authority/program, identifier/date/scope when visible. Do not use inferred, synthesized, or cross-row text as an excerpt.
- If either role would require the judge to infer that it is the same event as the other role, discard the packet and replace it with a cleaner provider packet before final output.
- After discarding weak packets, count distinct `provider_brand` values that still have exactly one company row and one authority row under the same event label, with both rows independently strong for their role. If the count is below 70, keep finding new providers; do not pad by adding second events for already-qualified providers.

Output skeleton for each adjacent two-row packet:
```jsonl
{"item":{"provider_brand":"...","event_or_recognition_title":"...","evidence_role":"company_announcement"},"url":"https://...","excerpts":["provider/legal entity ...; program/status ...; authority or standard ...; date/scope/id when visible ..."],"answer":{"legal_entity":"...","site":"...","authority":"...","id":"...","scope":"...","match_status":"clean"}}
{"item":{"provider_brand":"...","event_or_recognition_title":"...","evidence_role":"authority_record"},"url":"https://...","excerpts":["provider/legal entity ...; program/status ...; authority or standard ...; date/scope/id when visible ..."],"answer":{"legal_entity":"...","site":"...","authority":"...","id":"...","scope":"...","match_status":"clean"}}
```

Clean field separation:
- `evidence_role` declares which side of the packet the URL supplies; it is not itself the event evidence. Use only `company_announcement` or `authority_record`.
- Source-role/page fit asks whether the URL is on the right side of the packet: provider-controlled for `company_announcement`, official authority-side for `authority_record`.
- Substantive event support belongs in the event evidence: provider/legal entity, lab/site/body, recognition family, authority, certificate or program identifier, formal status, date/scope/standard, and enough traceable detail to reconcile the two rows.

Anti-degenerate source rule:
- Do not build the answer by sweeping A2LA, NANDO, IECEE, FDA, OSHA, SONCAP, or similar authority directories into standalone rows. Authority rows count only when paired to an official company-side source for the same provider/event packet.
- Do not let one provider/corporate family or one authority/source family dominate the answer while the provider floor is still unmet.
- Count one global TIC group as one provider brand for the floor: lab sites, legal subsidiaries, certificate numbers, scopes, and authority-program records are row details, not new provider rows.
- Reused URLs must be row-level evidence: the visible text or returned record for that packet must name the relevant lab/site/body, certificate/accreditation identifier, notified-body number, authority action, scope, standard, or program status. Generic accreditation hubs, broad service pages, directory indexes, and search shells are not enough.
- Prefer provider/source-family spread within the provider quota. Avoid having one authority domain, one URL family, one broad PDF, or one source hub carry most accepted packets unless each reused page has exact row-level event labels and the provider quota is still met.

Discovery spread cues:
- Do not treat the recognition-family list as a canon, quota, or search menu. It is a reminder to avoid solving the task from one familiar directory or one cluster of global providers.
- Spread provider discovery across the TIC ecology: global groups, regional and niche labs, medical-device labs, electrical/product-safety labs, EMC/RF/cybersecurity labs, calibration/metrology labs, inspection or certification bodies, notified/designated bodies, and national-program appointees can all produce valid packets when the two-source event fit is real.
- Company-side anchors are not limited to newsrooms; provider accreditation tables, lab profile pages, status pages, downloadable certificates/scopes, approval lists, and program pages can work when they share a concrete recognition anchor with the authority record.
- Authority-side anchors should be detail-bearing records: registry rows, certificate or scope PDFs, public notices, designation pages, scheme records, program lists, or current-list conflict records that expose the provider/legal entity, body/lab/site, program, identifier, date, scope, standard, or status being paired.
- During drafting and final self-audit, count only provider brands with both roles under the same event label and independent support on both sides; if the count is below 70, keep finding new providers instead of adding second events for already-qualified providers.
- If a well-known global group is hard to pair cleanly, move to a regional or program-specific provider with a direct authority record and provider-controlled accreditation page. Provider-count completion is more important than including famous brands.

Evidence roles:
- `company_announcement`: an official provider- or corporate-group-controlled source that makes the company-side recognition or status claim.
- `authority_record`: an official authority-side record, certificate, scope, registry, public notice, scheme source, national-program source, or current-list conflict basis for the recognition or status.

Recognition/source ecologies worth exploring include:
- product-safety laboratory recognitions, expansions, renewals, recognized-site records, and scope records.
- medical-device testing-laboratory recognition or accredited-lab program records.
- notified-body, designated-body, approved-body, or recognized third-party body status records.
- CB-scheme body, test-laboratory, or scheme-specific scope/status records.
- ISO/IEC 17025 or comparable lab-accreditation certificates, scope PDFs, directory details, and field or scope expansions.
- national or sector-specific conformity-assessment appointments, approved-firm lists, public notices, suspensions, withdrawals, and current-list conflict records.

Record details to preserve when visible: legal entity exactly as sourced, lab/site/body identifier, authority body or jurisdiction, source/effective/approval/start/expiry/scope date, NB/TL/NRTL/CBTL/NCB/SPTL/accreditation/program identifier, scope or standard, and `match_status` such as `clean`, `partial`, or `conflict`.

Do not use this as a generic TIC newsroom tracker. Ordinary lab openings, partnerships, earnings items, marketing updates, regulatory-newsletter articles, alerting services, competitive rankings, sales strategy, and company-only claims without a modeled authority-side record do not count.

Requirements:
- The submitted `provider_brand` must be a real TIC or conformity-assessment provider brand/corporate group, not an authority, standard, client, product line, generic lab type, or source directory.
- The page must fit the submitted `evidence_role` source side: provider-controlled for `company_announcement`, or official authority-side for `authority_record`.
- For provider-controlled pages, the page must visibly claim the submitted accreditation, recognition authority, program, or status for the submitted provider/legal entity; generic service, testing, capability, or accreditation language is not enough.
- The page must connect to the submitted provider and recognition event closely enough for source reconciliation: provider brand, legal entity, lab or body site, recognition family, authority, regulation/standard, identifier, current-program conflict basis, or scope should be visible.
- The page must substantively support a formal accreditation, recognition, notified-body designation, testing-lab status, scope expansion, or authority appointment, not just a generic capability, service, lab-opening, or marketing claim.
- The page must expose traceable event details such as legal entity, site/body/lab identifier, source/effective/approval/start/expiry/scope date, authority body, jurisdiction, scope, recognized standard, regulation, or program role.

Write one JSON object per line to `results_tic_lab_accreditation_authority_records.jsonl`:
{"item": { "provider_brand": "<provider_brand>", "event_or_recognition_title": "<event_or_recognition_title>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
