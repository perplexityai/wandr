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

## `thailand_service_robot_channel_presence`

Identify 100+ companies as Thailand-market service-robot channel entities; for each company, cover each of the 3 presence facets listed below with a public source (i.e. 1+ URL) exposing a concrete, facet-scoped finding.

The interest is the public channel ecology around service robots in Thailand: distributors, integrators, rental operators, support providers, venue-facing robotics solution firms, and comparable actors whose public pages connect them to service-facing robots rather than only factory automation.

Presence facets of interest, which we refer to as `presence_facet`, are:
- `owned_channel_role`: the company's own or officially attributable Thailand service-robot channel role.
- `brand_model_signal`: a concrete service-robot brand, model, or named solution in the company's Thailand channel context.
- `public_market_trace`: a public Thai market activity trace involving the company and service robots, such as a customer, venue, deployment, event, trade-show, press, or comparable public activity.

Companies ought to be real Thailand-market service-robot channel entities. Industrial-only robotics firms, generic factory-automation sellers, consumer-only appliance sellers, pure manufacturers with no Thai-facing channel trace, source publishers, registries, directories, and contact-only identities do not qualify as companies for this task. Sources should be public and usable as normal pages.

Requirements:
- The page must clearly identify the named company.
- The page must tie the company, channel role, robot product, customer, venue, event, or activity to Thailand specifically; Southeast Asia or other regional pages that do not make Thailand visible are not enough.
- The page must place the evidence in service-facing robot scope: delivery, reception, hospitality, healthcare, retail, cleaning, facility-service, public guidance, or comparable public/commercial service use. Industrial arms, cobots, warehouse-only automation, generic automation software, and consumer household appliances do not count by themselves.
- The page should make its facet-appropriate source role visible. For `owned_channel_role`, the page should read as a company-controlled, official, or clearly attributable channel-role surface, such as an owned domain, official social/company profile, official partner/dealer page, or branded solution page. For `brand_model_signal`, the page should be organized around a concrete robot brand, model, product family, or named service-robot solution tied to the company rather than only broad robotics wording. For `public_market_trace`, the page should read as a public activity surface, such as a Thai customer/venue/deployment story, event or trade-show page, press item, public demo, or comparable market trace rather than a bare registry, contact page, or source directory.
- The page should expose a focused finding for the named company and `presence_facet`. For `owned_channel_role`, this means a concrete role such as selling, distributing, integrating, renting, deploying, maintaining, supporting, or operating service robots in Thailand. For `brand_model_signal`, this means a named robot brand/model/solution visibly tied to the company and Thai channel context. For `public_market_trace`, this means a concrete Thai market trace involving the company and service robots, not just generic service-robot marketing.

Write one JSON object per line to `results_thailand_service_robot_channel_presence.jsonl`:
{"item": { "company": "<company>", "presence_facet": "<presence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
