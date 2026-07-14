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

## `tiktok_shop_partner_api_evidence`

For 10+ public-support statuses in the official TikTok Shop Partner Center documentation, cover 3+ commerce capability areas per status, name 2+ distinct capability surfaces per area, and supply 2+ facet-specific public sources per surface (i.e. 1+ URL).

This is a public documentation provenance atlas, not API implementation guidance. Each source should show what the official public Partner Center docs state, omit, gate, or version for the claimed commerce API capability, app/access workflow, sandbox workflow, or console/support boundary.

Public-support statuses are:
- `endpoint-reference`
- `api-overview-only`
- `changelog-or-release-only`
- `authorization-or-access-doc`
- `app-or-sandbox-guide`
- `console-or-support-guide-only`
- `permission-gated`
- `no-public-field-source`
- `no-public-endpoint-locator`
- `version-unknown`

The evidence facets are:
- `locator`
- `fields_or_objects`
- `access_or_permission`
- `version_or_change_status`

Each citation should include a short checked-date note naming the page or locator and the facet-specific finding being claimed.

Cover the facets that the public documentation can support for that surface. Endpoint pages often support locator and fields/object evidence; access guides, release notes, sandbox guides, and console/support pages may instead carry permission, status, version, or boundary evidence without exposing a public endpoint path.

In-scope sources are official public TikTok Shop Partner Center documentation pages, normally `partner.tiktokshop.com/docv2/...` or legacy `partner.tiktokshop.com/doc/...` pages. Endpoint-reference pages, API overviews, release/changelog pages, authorization/access pages, app publication guides, sandbox/development-shop guides, and console/support guides can all count when they fit the claimed facet.

Third-party SDKs, blogs, integration vendors, search snippets, TikTok Research API pages, TikTok Business/ads API pages, private account screens, credentialed-only material, hidden JSON endpoints, scraping/bypass methods, seller analytics, rankings, procurement recommendations, lead scoring, outreach, contact enrichment, and account-specific data extraction do not count.

Missing, gated, and boundary statuses are valid only when anchored in an official public locator that states the capability or nearby workflow. Do not claim global absence from the whole internet; keep those records to what the public Partner Center page itself supports.

Requirements:
- The page must identify or locate the claimed capability surface in a TikTok Shop Partner Center commerce context.
- The page must support the submitted public-support status from public documentation evidence rather than from assumptions about hidden or credentialed material.
- For `locator`, the page must locate the claimed endpoint, API action, guide capability, app/sandbox workflow, or console/support module.
- For `fields_or_objects`, the page must state public fields, objects, parameters, metrics, request/response elements, or an anchored no-public-field/permission-gated field status.
- For `access_or_permission`, the page must state an authorization, access-scope, app review, signing, seller/creator/shop authorization, partner-type, market, sandbox, or credential caveat.
- For `version_or_change_status`, the page must state a version slug, release/changelog/update/deprecation/status note, rollout marker, or anchored version-unknown status.
- The page must support the submitted facet-specific detail without turning public documentation provenance into API-calling instructions, private seller data claims, or operational advice.

Write one JSON object per line to `results_tiktok_shop_partner_api_evidence.jsonl`:
{"item": { "public_support_status": "<public_support_status>", "capability_area": "<capability_area>", "capability_surface": "<capability_surface>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
