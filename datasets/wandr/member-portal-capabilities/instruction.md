You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `member_portal_capabilities`
  - `member_portal_capabilities.member_portal_deployments`

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

## `member_portal_capabilities`

For 130+ public member-portal software platforms serving coworking/flexible workspace, fitness/gym, or adjacent membership-based facility operators, cover the 2 artifact evidence roles below for each platform with 1+ URL per platform and evidence role.

Each evidence note must be a positive factual public-evidence note for the submitted platform and evidence role. Include the target vertical, the role-specific evidence claim, source class/owner, visible source date/status/version if any, checked date, and any source-visible caveat that limits the claim. Do not rank vendors, recommend a purchase or switch, infer ROI, give procurement or migration advice, collect contacts, offer implementation guidance, or assess legal, privacy, security, or compliance adequacy.

Evidence roles:
- `integration_or_developer_surface`: public evidence for a concrete integration, API, webhook, developer surface, partner connector, app/marketplace listing, or integration setup path tied to the platform. The page must expose how the surface operates or is configured, such as trigger/action behavior, endpoint/API/webhook/authentication mechanics, data-flow behavior, setup steps, or a partner relationship that describes what is connected, automated, exchanged, or required. A connector name, marketplace placement, app listing, partner logo, generic "integrations" label, or broad feature grid is not enough by itself.
- `operational_change_or_assurance_artifact`: public operational evidence such as a support/help artifact, release note, changelog, status/trust/security/privacy/DPA page, implementation requirement, availability limitation, version/update marker, or deployment caveat that affects member-facing portal, facility-management, integration, access, payment, app, or data-processing operation. The page must provide load-bearing operational substance: a concrete constraint, limitation, change, current or historical status signal, scoped assurance statement, implementation requirement, deployment detail, or version/update marker. Broad support overviews, generic app listings, broad feature summaries, trust badges, privacy boilerplate, or unspecific "we take security seriously" language are not enough by themselves. The evidence note records what the public artifact says, not whether the platform is adequate.

Positive evidence should come from public sources whose role and owner are clear. Ordinary vendor product pages, broad feature indexes, navigation menus, all-in-one marketing pages, pricing cards, comparison blurbs, and review/directory profiles do not pass merely because they mention member-portal capabilities. They pass only when the cited page section is itself a role-specific artifact: a concrete integration/developer surface or an operational assurance/change/limitation artifact. Labeled app stores, partner marketplaces, support centers, docs, release notes, status pages, trust/security/privacy pages, and developer docs can all qualify when their load-bearing text fits the submitted role.

Requirements:
- The page must identify the named platform or product and tie it to member-portal, member-management, facility-management, or member-facing self-service software for a coworking/flexible workspace, fitness/gym, or adjacent membership-based facility context.
- The page must make its source role and owner clear enough for the submitted evidence role. For `integration_or_developer_surface`, this means a labeled developer, API, integration, marketplace, app, partner, vendor, or partner-owned surface visibly about an integration or developer function rather than a generic listing. For `operational_change_or_assurance_artifact`, this means an owned or clearly labeled support/help, release/changelog, status, trust/security/privacy/DPA/legal, implementation, limitation, or requirement artifact rather than a broad feature, review, directory, or marketing page.
- The page must support the submitted `evidence_role` with a specific factual public claim, not just adjacent marketing language, a source label, a listing placement, or a generic software category.
- Caveats about visible date, source limits, stale wording, conflicts, pricing absence, integration uncertainty, or missing context must not substitute for the positive role-specific evidence. An evidence note with only absence, uncertainty, or a generic capability mention fails.

Write one JSON object per line to `results_member_portal_capabilities.jsonl`:
{"item": { "platform": "<platform>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `member_portal_capabilities.member_portal_deployments`

Cross-tasknode identifier discipline: this task is for the same {= platform =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= platform =}+ public member-portal software platforms serving coworking/flexible workspace, fitness/gym, or adjacent membership-based facility operators, cover 2+ distinct deployment contexts per platform with 1+ URL per platform and deployment context.

Each deployment note must be a positive factual public-evidence note for the submitted platform and deployment context. Include the target vertical, the named operator/customer/venue/deployment context, the deployment-use claim, source class/owner, visible source date/status/version if any, checked date, and any source-visible caveat that limits the claim. Do not rank vendors, recommend a purchase or switch, infer ROI, give procurement or migration advice, collect contacts, offer implementation guidance, or assess legal, privacy, security, or compliance adequacy.

A deployment context is an identifiable facility operator, customer, venue, workspace, studio, gym, branded deployment, or public portal/app instance using or exposing the submitted platform for member-facing or facility-management workflows. Vendor-owned customer stories, operator-owned pages, branded public portals or apps, customer quotes with named operators, and public deployment artifacts can qualify when the load-bearing text identifies a real context and actual platform use. Generic vendor logos, customer indexes, unsourced "trusted by" counts, anonymous testimonials, broad feature claims, and ordinary directory/review profiles are not enough.

Requirements:
- The page must identify the named platform or product and tie it to member-portal, member-management, facility-management, or member-facing self-service software for a coworking/flexible workspace, fitness/gym, or adjacent membership-based facility context.
- The page must identify the submitted `deployment_context` as a real operator, customer, venue, workspace, studio, gym, branded deployment, or public portal/app instance, not just a generic customer category or source section.
- The page must support actual use or public exposure of the platform by that deployment context for member-facing or facility-management workflows.
- Caveats about visible date, source limits, stale wording, conflicts, pricing absence, missing context, or deployment uncertainty must not substitute for the positive deployment evidence. A deployment note with only absence, uncertainty, a customer/logo listing, or a generic capability mention fails.

Write one JSON object per line to `results_member_portal_capabilities.member_portal_deployments.jsonl`:
{"item": { "platform": "<platform>", "deployment_context": "<deployment_context>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
