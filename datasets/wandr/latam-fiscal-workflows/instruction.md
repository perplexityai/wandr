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

## `latam_fiscal_workflows`

For each of the 6 jurisdictions listed below, cover 1+ regulator-owned fiscal software/provider program, 6+ registry legal entities per program, 1+ commercial brand/product identity per legal entity, and 1+ regulator-to-product join per commercial identity. For each join, supply 3+ source-owner evidence legs and 1+ URL per evidence leg.

Jurisdictions:
- Colombia
- Mexico
- Peru
- Chile
- Panama
- Dominican Republic

Regulator programs:
- `Colombia DIAN Proveedores Tecnologicos`
- `Mexico SAT PAC`
- `Peru SUNAT OSE`
- `Chile SII Empresas Proveedoras de Soluciones FE`
- `Panama DGI PAC`
- `Dominican Republic DGII e-CF Providers`

This is an identity-resolution benchmark for public fiscal software/provider evidence. A useful record starts from, or is checked against, a regulator-owned registry/program surface that names a legal entity and identifying metadata. It then joins that legal entity to a public commercial brand, product, app, setup flow, API, or source-bounded negative state through official regulator, vendor, legal, platform, or developer artifacts.

For a positive registry-product join, the URL for a positive evidence leg must expose a source-owned bridge object in the same bounded source context as the submitted legal/provider identity or regulator program. A source-owned bridge object can be a listed website, software name, product/service name, setup provider selection, app/developer identity, API/service object, certificate/document type, authorization object, or comparable fiscal-product object. A page that only lists a legal entity in a regulator registry, or only markets a vendor's fiscal product, is not enough for a positive join leg unless that same page also carries the other side of the join.

Evidence legs:
- `regulator_registry_record`: Regulator-owned registry, catalog, list, PDF, or program page that names the exact legal entity plus identifier/status metadata and also exposes a source-owned bridge object such as listed website, software name, product/service name, platform/app reference, authorization object, or comparable commercial-facing object for the submitted join.
- `vendor_authorization_claim`: Official vendor-controlled page that claims authorization/provider status for the jurisdiction and names the submitted commercial product/service together with the registry legal entity, tax identifier, regulator-listed provider name, or regulator program in the same bounded source context.
- `legal_entity_bridge`: Official vendor/legal/platform source that connects the commercial brand/product to the registry legal entity, tax identifier, listed website, setup-provider name, legal footer, developer identity, or other source-owned bridge object in the same bounded context.
- `product_capability_or_setup_doc`: Official vendor setup, support, product, or how-to page showing country-specific fiscal software capability while also naming the provider legal entity, regulator-listed provider name, regulator program, setup provider, authorization object, or comparable bridge object.
- `platform_app_or_integration_artifact`: Platform-owned listing, app-store page, marketplace page, or platform help artifact naming the app/developer/product, the fiscal integration, and a bridge to the vendor/legal/provider identity; generic app categories do not pass.
- `developer_or_technical_artifact`: Official developer, API, endpoint, schema, webservice, certificate, document-type, or field-level implementation artifact tied to the jurisdiction and naming the product/API/service object plus the vendor, provider legal entity, developer identity, or regulator program it belongs to.
- `negative_registry_or_bridge_state`: Named official registry, platform, legal, or vendor surface supporting absence, revocation, stale status, legal-entity-only state, or missing bridge for the exact target.
- `technical_context_only`: Regulator or platform technical context that is useful for the jurisdiction but does not by itself name the exact provider, legal entity, app, product, or technical object required for a positive join.

Bridge types:
- `same_legal_name`: Commercial brand/product uses the same legal name shown in the registry.
- `registry_listed_website`: The regulator record lists a website that resolves to the commercial brand or product surface.
- `vendor_legal_footer`: Official vendor legal/footer/privacy text names the same legal entity or tax identifier.
- `vendor_setup_names_provider`: Official setup or onboarding documentation tells users to select the registry legal entity/provider name.
- `vendor_authorization_claim`: Official vendor page claims the same regulated-provider authorization or capability.
- `platform_developer_identity`: Platform or app marketplace names a developer/merchant identity that must be joined to the vendor or legal entity.
- `developer_docs_identity`: Developer/API docs name the product, account, endpoint, provider, or technical object that bridges to the brand.
- `no_public_bridge_found`: The checked public source-owner surface does not expose a reliable brand/legal-entity bridge.
- `registry_absence_or_revocation`: A regulator-owned source supports absence, revocation, stale status, or a status change for the named entity/brand.

Join states:
- `brand_matches_legal_entity`: The brand/product name and registry legal entity are effectively the same public identity.
- `brand_requires_bridge`: The commercial brand differs from the registry legal name and needs a source-owned bridge.
- `third_party_developer_bridge_required`: A platform app or integration is developed by a third party and needs a developer/vendor bridge.
- `legal_entity_only_no_product`: The registry legal entity is listed, but the cited evidence does not establish a public product/service capability.
- `vendor_claim_without_registry_match`: A vendor claims capability, but the cited regulator surface does not match that legal entity.
- `claimed_but_not_in_registry`: The brand/product claim is checked against a named registry and no matching listed entity is supported by the submitted excerpts.
- `registry_status_stale_or_revoked`: The regulator or source-owner evidence shows stale, revoked, inactive, archived, or date-limited status.
- `context_only_no_registry`: The page is only regime or technical context and does not name the provider/legal entity/product/app.

Positive regulator evidence must be regulator-owned and must name the exact legal entity plus a tax ID, registry identifier, resolution, authorization date, status, or comparable official metadata. To count as `regulator_registry_record` for a positive registry-product join, the regulator-owned URL must also expose the submitted commercial-facing object or bridge object, such as a listed website/domain, software/product name, app/platform reference, authorization object, or product/service object. A plain provider list with only legal name and tax ID is registry evidence, but it is not a positive registry-product join leg.

Official commercial evidence must connect the same jurisdiction and commercial identity to the registry legal entity or to the claimed bridge state in one bounded source context. Acceptable bridges include legal footers, privacy/legal pages, registry-listed websites, vendor setup steps naming the provider company, vendor authorization claims that name the relevant program or provider identity, platform-owned listings that name the app/developer and fiscal integration, and developer/API artifacts that name the product or technical object. A brand such as Alegra, Siigo, NubeFact, Facturama, EDICOM, Alanube, or Gurusoft does not pass by reputation; the cited page must carry the submitted legal-entity/product join.

Argentina/ARCA/AFIP technical pages can be useful context for a negative or technical-asymmetry finding, but they should not be treated as registry-positive peers unless the submitted source actually names a comparable regulator-owned provider registry entry. Broad ARCA/AFIP, DIAN, SUNAT, SAT, SII, DGI, or DGII regime pages do not by themselves establish a commercial product capability.

Requirements:
- The page must fit the submitted source owner and exact object: the regulator program, registry legal entity, commercial brand/product/app, technical object, or named negative surface claimed by the row.
- The page must support the regulator/legal-entity basis for the row: a positive registry/program record with legal entity metadata, or a scoped official registry/platform/legal surface that shows what the named surface can or cannot prove.
- The page must support the submitted commercial identity, bridge_type, and join_state for the legal-entity to brand/product relationship, including negative, stale, third-party-developer, legal-entity-only, or context-only states when those are claimed.
- For every positive evidence leg, the page must expose at least two source-owned object classes in the same bounded context: the legal/provider/regulator side and the product/app/API/service/commercial side. Do not satisfy this by combining separate pages, brand familiarity, search snippets, homepage navigation, or a solver's inference.
- The page must match the submitted evidence_leg with source-specific substance rather than generic regime, homepage, category, or third-party background text.
- The finding must stay source-bounded: report registry status, vendor claims, bridge evidence, technical objects, platform/app status, or absence/staleness only to the level the cited page itself supports.

Write one JSON object per line to `results_latam_fiscal_workflows.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "regulator_program": "<regulator_program>", "registry_source_owner": "<registry_source_owner>", "registry_legal_name": "<registry_legal_name>", "registry_tax_id_or_identifier": "<registry_tax_id_or_identifier>", "commercial_brand": "<commercial_brand>", "product_or_service": "<product_or_service>", "bridge_type": "<bridge_type>", "join_state": "<join_state>", "claim_summary": "<claim_summary>", "evidence_leg": "<evidence_leg>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
