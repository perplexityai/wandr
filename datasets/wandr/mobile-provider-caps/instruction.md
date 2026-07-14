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

## `mobile_provider_caps`

For 100+ U.S.-serving consumer mobile service provider brands, supply evidence for each of the 4 capability areas and at least 1+ URL per area. The provider universe is open and can include MNOs, carrier-owned prepaid or flanker brands, independent MVNOs, cable or ISP wireless brands, regional wireless carriers, Lifeline or public-benefit mobile providers, app-first wireless lines, and hybrid consumer mobile providers when the public evidence supports the mobile phone-number service path.

The capability areas are:
- `phone_number_service`: provider-controlled evidence that the brand offers a U.S.-serving consumer mobile or wireless service path with a phone number, voice, SMS, talk/text, new-number, port-in, or equivalent line-number handling.
- `sim_esim_delivery`: provider-controlled evidence for the SIM or eSIM activation, purchase, delivery, transfer, swap, or device-compatibility path attached to the consumer service.
- `network_identity`: public evidence for the current network, host network, owned network, multi-network labels, owner/brand/legal distinction, or a source-backed not-disclosed state.
- `lifecycle_policy`: public evidence for a harder operational or policy capability such as port-out mechanics, transfer PIN, identity/KYC or credit-check posture, app/IMEI/device constraints, account lock, activation constraints, or a source-backed not-publicly-documented state.

For downstream reading, include the canonical provider brand, owner or legal/DBA name when public, provider type, service layer, number path, SIM/eSIM path, host network or network labels when public, hard policy topic when relevant, capability value, source class, documentation state, visible source date or as-of date, checked date, confidence, and source notes. Use 2026-06-29 as the checked date unless the source was checked later.

Provider type should use these meanings when they fit:
- `MNO or facilities-based carrier`
- `carrier-owned prepaid or flanker brand`
- `independent MVNO`
- `cable or ISP wireless brand`
- `regional wireless carrier`
- `Lifeline or public-benefit mobile provider`
- `app-first wireless line`
- `hybrid or other consumer mobile provider`

Service layer should be factual, not advisory:
- `carrier_mobile_line`
- `app_first_wireless_line`
- `voip_or_app_number_only`
- `travel_data_esim`
- `data_only_esim`
- `unclear_or_hybrid`

Number path should use these meanings when they fit:
- `new_us_number`
- `port_in_existing_number`
- `new_number_or_port_in`
- `existing_number_transfer_or_swap`
- `temporary_number`
- `no_phone_number`
- `unclear`

SIM/eSIM path should use these meanings when they fit:
- `esim_new_activation`
- `esim_transfer_or_swap`
- `physical_sim_activation`
- `physical_sim_and_esim`
- `app_installed_esim`
- `device_compatibility_check_required`
- `no_public_esim_evidence`
- `unclear`

Source class and documentation state should use these meanings when they fit:
- `official_product_or_plan_page`
- `official_activation_or_checkout_flow`
- `official_help_center_or_support_doc`
- `official_policy_or_terms_page`
- `official_broadband_label_or_disclosure`
- `platform_carrier_support_page`
- `public_registry_or_regulator`
- `reputable_comparison_or_directory_source`
- `corroborated_public_community_or_forum_source`
- `other_public_source`
- `positively_documented`
- `negatively_documented`
- `not_publicly_documented_after_relevant_check`
- `conflicting_or_ambiguous`

Public sources can include provider product pages, activation and checkout flows, help-center articles, support docs, policy or legal pages, official broadband labels or disclosures, platform carrier-support pages, public registries, comparison directories, and corroborated community sources. The two core capability areas, `phone_number_service` and `sim_esim_delivery`, should be proven from provider-controlled sources. Third-party directories, platform pages, app-store listings, comparison sites, and community pages can help discover and corroborate providers, but they are not a closed source menu and should not be the only proof that a provider qualifies as a phone-number-bearing mobile service.

Requirements:
- The page must identify the claimed provider brand, or bridge a trade name, legal name, app name, or owner/brand label to it, with enough public context to distinguish it from unrelated same-name entities, host networks, parent companies, plan-comparison sites, device makers, pure travel eSIMs, and VoIP-only number apps.
- The page must fit the claimed `capability_area`: `phone_number_service` evidence should show phone-number, voice, SMS, talk/text, new-number, port-in, or equivalent mobile-line handling; `sim_esim_delivery` evidence should show SIM/eSIM activation, purchase, delivery, transfer, swap, compatibility, app installation, QR-code, or equivalent service setup; `network_identity` evidence should show current network/host/owner/legal identity, multi-network labels, or a visible public non-disclosure state; `lifecycle_policy` evidence should show a harder operational or policy mechanic, constraint, or source-backed public silence.
- The page must support the claimed capability value at the submitted specificity, such as service layer, number path, SIM/eSIM path, host network or network labels, policy topic, device/platform constraint, activation mode, identity/KYC posture, port-out or transfer-PIN mechanic, or documented absence.
- The record must preserve source posture and uncertainty: official versus third-party support, current/as-of state, negative documentation, ambiguity, conflicting network names, app-first or VoIP boundaries, travel/data-only exclusions, and `not publicly documented` states should be labeled rather than recast as clean positive facts.

Write one JSON object per line to `results_mobile_provider_caps.jsonl`:
{"item": { "provider_brand": "<provider_brand>", "capability_area": "<capability_area>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
