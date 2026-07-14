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

## `vp_marketing_saas`

For each of the 50 companies listed below, find 1+ people who currently hold a senior marketing-leadership role at that company, and supply a personal page URL (at least 1 per person) whose content shows the role.

Companies in scope:
- SAP — SAP SE, SAP AG
- Sage — Sage Group, Sage Software, The Sage Group
- AVEVA — AVEVA Group, AVEVA Solutions
- Elastic — Elastic NV, Elasticsearch, Elastic.co
- Software AG — SoftwareAG, Software AG (now StreamServe / IBM acquisition)
- TeamViewer — TeamViewer Germany, TeamViewer SE
- Darktrace — Darktrace plc, Darktrace Limited
- Celonis — Celonis SE, Celonis Inc, Make by Celonis
- OutSystems — OutSystems, Inc., OutSystems Software
- Onfido — Onfido Ltd, Onfido (Entrust)
- Salesforce — Salesforce.com, Salesforce, Inc., salesforce.com
- ServiceNow — ServiceNow, Inc., Service Now
- Workday — Workday, Inc.
- Adobe — Adobe Inc., Adobe Systems, Adobe Digital Experience
- Atlassian — Atlassian Corporation, Atlassian Plc
- Intuit — Intuit Inc.
- Snowflake — Snowflake Inc., Snowflake Computing
- Datadog — Datadog, Inc.
- MongoDB — MongoDB Inc., MongoDB, Inc.
- Cloudflare — Cloudflare, Inc.
- Confluent — Confluent, Inc., Confluent Inc
- GitLab — GitLab Inc., GitLab Ltd
- Splunk — Splunk Inc., Splunk (Cisco)
- Dynatrace — Dynatrace LLC, Dynatrace, Inc.
- New Relic — New Relic, Inc., New Relic Inc
- PagerDuty — PagerDuty, Inc.
- JFrog — JFrog Ltd
- Okta — Okta, Inc., Auth0 (an Okta company)
- CrowdStrike — CrowdStrike Holdings, CrowdStrike, Inc.
- Palo Alto Networks — Palo Alto Networks, Inc., PANW
- Zscaler — Zscaler, Inc.
- Twilio — Twilio Inc., Twilio Segment
- HubSpot — HubSpot, Inc., Hubspot
- Zendesk — Zendesk, Inc., Zendesk Inc
- Slack — Slack Technologies, Slack (Salesforce)
- Freshworks — Freshworks Inc., Freshdesk, Freshservice
- Sprinklr — Sprinklr, Inc.
- DocuSign — DocuSign, Inc., Docusign
- Bentley Systems — Bentley, Bentley Systems Incorporated
- Procore — Procore Technologies, Procore Technologies, Inc.
- BlackLine — BlackLine, Inc., Blackline
- Coupa — Coupa Software, Coupa Software, Inc.
- Anaplan — Anaplan, Inc.
- UiPath — UiPath, Inc., UiPath Inc
- Pegasystems — Pega, Pega Systems, Pegasystems Inc.
- Veeam — Veeam Software, Veeam Software Group
- Shopify — Shopify Inc., Shopify Plus
- Wix — Wix.com, Wix.com Ltd
- Klaviyo — Klaviyo, Inc.
- BILL — Bill.com, Bill.com Holdings, BILL Holdings

Requirements:
- The page must show the person holding a senior marketing-leadership role at the named company — VP- / Head-of- / CMO- / SVP-EVP-level marketing roles. Director-level and below or individual-contributor marketing roles don't count.
- The page must identify the named company as the employer (or under a recognized alias).
- The role at the named company must be currently held (no end-date or `Present`).

Write one JSON object per line to `results_vp_marketing_saas.jsonl`:
{"item": { "company": "<company>", "person": "<person>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
