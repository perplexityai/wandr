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

## `japan_telephony_provider_capabilities`

For 80+ public communications providers or provider-branded offerings whose public materials address Japanese phone numbers, voice, SMS, SIP, programmable telephony, or AI voice-agent telephony, cover each of the 8 capability facets below by supplying at least 1 public URL per provider and facet.

This is a dated public-evidence atlas, not a provider comparison. Rows should describe what the cited source directly states, restricts, or contradicts. Do not rank providers, recommend a provider, describe a fastest prototype path, give signup or procurement instructions, interpret telecom law, or advise implementation choices.

Capability facets:
- `japan_number_availability`: public evidence that the provider addresses Japanese phone numbers, Japan DIDs, Japan virtual numbers, Japan phone service, or Japan-country telephony availability.
- `number_type_profile`: public evidence of the Japan number types or prefixes addressed, such as 050, 0ABJ/local/geographic, 0120/0800 toll-free, mobile, national, unspecified, or a documented negative.
- `inbound_voice`: public evidence of inbound voice, receive-call, forwarding, IVR/contact-center, or inbound-number support for Japan.
- `outbound_voice_or_sip`: public evidence of outbound calling, SIP trunking, local/A-Z termination, caller ID, porting, or outbound-number restrictions for Japan.
- `sms`: public evidence of Japan SMS, sender ID, inbound/outbound messaging, SMS-enabled-number support, or documented SMS non-support.
- `programmable_or_ai_voice_telephony`: public evidence that the provider exposes API, webhook, SIP, contact-center automation, programmable voice, or AI voice-agent telephony tied to Japanese phone service.
- `kyc_or_numbering_requirement`: public evidence of provider-stated identity, KYC, local-address, business-use, telecom-numbering, or other Japan number requirement information.
- `public_pricing_or_fee`: public evidence of Japan-number, voice, SMS, SIP, setup, application, recurring, or maintenance pricing/fees, or a source-stated Japan-specific no-price/no-public-price policy on a pricing or country-fee surface.

For each row, report the source class, the source-stated capability state, any Japan number types that matter for that facet, the source date or last-updated date when visible, the checked date, and a confidence note. Provider-controlled sources are the normal bar for positive capability support. Reputable third-party telecom directories, numbering datasets, comparison pages, or country guides can help with discovery, documented negatives, restrictions, or conflicts, but should not become standalone proof of a provider-owned positive capability claim.

The source should be fully public, accessible, and usable. Console-only availability, private quotes, sales calls, account dashboards, paywalled pages, private API responses, and login-only signup flows do not count.

Requirements:
- The page must clearly identify the named provider or provider-branded offering.
- The page must source-address Japan-specific telephony, phone-number, calling, SMS, SIP, programmable voice, contact-center, or AI voice-agent phone service.
- The page must make its facet-appropriate source role visible. A country coverage page, number catalog, support article, regulatory/KYC page, product documentation page, API/voice/SMS documentation page, official pricing page, official product page, or reputable telecom source can count when it is visibly suited to the claimed facet.
- The page must support a concrete, source-stated public-evidence state for the requested facet: positive support, documented negative, restriction, a source-stated partial/unspecified support state, or a clearly source-grounded conflict signal. A silent page, missing page, generic "coming soon" local-regulations block, no-current-page placeholder, or unrelated marketing page does not satisfy root facet evidence.
- Facets need facet-specific language: inbound rows need receive/inbound/forwarding/IVR/contact-center evidence; outbound/SIP rows need outbound calling, SIP, termination, caller-ID, or porting evidence; programmable/AI rows need API, webhook, SIP, contact-center automation, programmable voice, or AI voice-agent telephony tied to Japan phone service; KYC rows need provider- or authority-stated identity/local-address/business-use/numbering requirements; pricing rows need Japan-specific fees or source-stated Japan-specific no-public-price policy.

Write one JSON object per line to `results_japan_telephony_provider_capabilities.jsonl`:
{"item": { "provider": "<provider>", "capability_facet": "<capability_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
