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

## `macos_privilege_elevation_controls`

For 30+ macOS elevation offerings, cover each of the 5 control facets listed below for each offering across each of the 2 source surfaces listed below, with a public source (i.e. 1+ URL) that claims, documents, or shows a concrete public control finding for that facet and source-surface role.

The task maps public claims about managed macOS privilege-elevation controls. It is not about whether a control works, whether a product is secure, how to deploy it, how to bypass it, what to buy, or whether a vendor is trustworthy.

The control facets of interest, which we refer to as `control_facet`, are:
- `temporary_elevation_model`: a temporary admin session, self-service promotion, per-app/process run-as-admin, policy-based elevation, sudo/command plugin, timer/demotion, or comparable managed elevation behavior.
- `approval_or_request_workflow`: a user request path, approval queue, role/IdP gate, ticket/manager/admin approval, self-service request workflow, or comparable control gate.
- `reason_or_justification_capture`: reason prompts, justification fields, preset reasons, request/ticket reasons, or comparable rationale capture.
- `audit_log_or_report`: logs, audit trail, session/elevation history, reports, SIEM/webhook/export, event messages, or comparable record of elevation activity.
- `mdm_or_management_integration`: MDM/profile/policy management, management-console controls, Mac-management platform support, release-note management keys, or comparable managed deployment/control support.

The source surfaces of interest, which we refer to as `source_surface`, are:
- `primary_product_surface`: provider, project, maintainer, product, or support documentation that directly presents the selected facet as a maintained product-control capability of the offering.
- `operational_surface`: configuration, release, integration, deployment, administration, API/event/export, management-key, or local support evidence that shows how the selected facet is configured, administered, changed, emitted, exported, deployed, or otherwise used in a concrete operational setting for the maintained offering.

The macOS elevation offering ought to be a real public macOS managed/admin elevation, temporary-admin, endpoint privilege-management, or Mac-management elevation offering maintained by a provider, project, or platform. Local institutional deployment pages, help-desk articles, and process KBs are not distinct offerings; they can only be supporting sources for the underlying maintained offering when they visibly name or anchor that offering and provide facet-specific operational detail. Exploit proof-of-concept pages, bypass helpers, CVE pages, hardening/offensive writeups, generic PAM concept pages, Windows-only EPM pages, pure MDM suites with no elevation feature, mirrors, search/listing pages, generic reviews/listicles, and forum chatter are outside the task's product-control evidence scope.

Requirements:
- The page must identify the claimed provider/offering, or make the match unambiguous through page title, navigation, repository/project identity, product docs, support framing, or equivalent page content.
- The page must tie the offering or feature to macOS/Mac endpoints and managed/admin privilege elevation, not merely generic endpoint security or identity administration.
- The page should show the claimed `source_surface` role through concrete page anchors: for `primary_product_surface`, provider/project/maintainer authorship, product/support framing, repository identity, or comparable maintained-offering context that directly presents the selected facet as product capability; for `operational_surface`, configuration keys, admin-console workflow, release-note changes, integration/deployment instructions, event/API/export details, management settings, or local support steps anchored to the maintained offering. The two source-surface roles are not interchangeable: a broad product overview, request-management page, or support hub does not satisfy both roles from the same generic prose. It can support a selected facet only when it has a facet-specific section, table, heading, paragraph, configuration key, release note, API/event/export detail, management-setting description, support step, or example for the selected `control_facet` and `source_surface`.
- The page must claim, document, or show a concrete finding for the claimed `control_facet`, not only a generic least-privilege, endpoint-security, request-management, visibility, reporting, or MDM statement. The finding should be local to the selected facet; all-purpose product prose that could be reused unchanged for several facets is not enough.

Write one JSON object per line to `results_macos_privilege_elevation_controls.jsonl`:
{"item": { "provider": "<provider>", "offering": "<offering>", "control_facet": "<control_facet>", "source_surface": "<source_surface>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
