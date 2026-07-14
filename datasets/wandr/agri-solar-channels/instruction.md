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

## `agri_solar_channels`

For 375+ solar companies or solar equipment trade-channel companies serving Great Britain, Northern Ireland, the Republic of Ireland, or cross-border/all-island markets, supply evidence for each of the 2 evidence types, with at least 1+ source URL per type. Include installers, EPCs, installer-EPCs, and solar equipment distributors or wholesalers when the public sources tie them to agri, farm, rural commercial, ground/yard-mounted, non-domestic/C&I solar, or solar trade-channel work. This is a public provenance table as of 2026-06-16, not a prospect list, buyer guide, recommendation, contact-enrichment exercise, or outreach plan.

The evidence types are:
- `capability_source`: an official company-owned, company-controlled, or otherwise official company capability/project/channel page for the submitted company, proving agri, farm, rural commercial, ground-mounted, yard-mounted, non-domestic/C&I solar PV work or solar equipment distributor/wholesale channel capability.
- `independent_corroboration`: a separate non-company or high-authority public source identifying or bridging the same company through a concrete registry, scheme, certification, association, public-framework, outside manufacturer/distributor, trade/project, or entity-directory fact.

For downstream reading, optional factual notes can include canonical company name, legal or trading name when source-stated, operating regime, country/county/service geography, organization type only as source-stated, service or channel role, capability signal, source-stated project size when available, scheme/certification/channel corroboration when source-stated, source class, source date or observed date, checked date, confidence, and source notes. Use 2026-06-30 as the checked date unless the source was checked later.

Operating regime should be factual and source-grounded. Useful values include:
- `great_britain`
- `northern_ireland`
- `republic_of_ireland`
- `cross_border_or_all_island`
- `not_clear`

Useful capability signals include:
- `farm or agricultural solar PV design or installation`
- `rural commercial or non-domestic solar PV`
- `C&I solar PV for businesses, farms, estates, food production, or rural facilities`
- `ground-mounted or yard-mounted solar tied to on-site consumption or rural/C&I use`
- `farm roof, barn roof, dairy, poultry, pig, mushroom, cold-store, or grain-drying project evidence`
- `EPC or installer-EPC delivery for relevant solar PV projects`
- `solar equipment distribution, wholesale supply, trade accounts, or installer-channel support`

Useful capability-source surfaces include:
- `official company capability or service page`
- `official company project or case-study page`
- `official company sector page for agriculture, farms, rural commercial, or C&I solar`
- `official company distributor, wholesale, trade-account, or installer-channel page`
- `official company brochure, PDF, video, or profile controlled by the submitted company`

Useful independent corroboration source types include:
- `official registry or scheme page`
- `certification directory`
- `public procurement or framework supplier page`
- `association or member directory page`
- `non-company manufacturer, distributor, or installer-channel partner page`
- `non-company trade, farming, or project article`
- `entity-specific public directory with concrete role or accountability facts`
- `public company record or other high-authority public accountability source`

Source class should be factual, not promotional. Useful public source classes include:
- `official company capability page (capability_source only)`
- `official company project or case-study page (capability_source only)`
- `official company distributor or wholesale channel page (capability_source only)`
- `official registry or scheme page (independent_corroboration only)`
- `certification or association directory (independent_corroboration only)`
- `public framework or procurement page (independent_corroboration only)`
- `non-company manufacturer or distributor page (independent_corroboration only)`
- `non-company trade, farming, or project article (independent_corroboration only)`
- `entity-specific public directory/profile (independent_corroboration only)`
- `other non-company high-authority public source (independent_corroboration only)`

Boundary classes to keep out unless the page meets the submitted role's source and substance bars:
- `generic SEO or cost-guide page`
- `quote funnel or lead-generation matching page`
- `search result or broad installer list without entity-specific evidence`
- `company-owned certification logo or claim used as independent corroboration`
- `non-company article, directory, registry, or framework page used as a capability source`
- `company-owned page used as independent corroboration`
- `broad grant or scheme explainer with no company-specific facts`
- `review-only or customer-opinion page`
- `utility-scale solar farm developer evidence with no farm/rural/C&I self-consumption or channel role`
- `contact, outreach, recommendation, prioritization, or lead-scoring material`

Public sources are role-specific. For `capability_source`, use only the submitted company's official or company-controlled capability, project, sector, channel, brochure, PDF, video, or profile page. For `independent_corroboration`, use only a source not controlled by the submitted company, such as an official registry, scheme page, certification directory, public framework, association/member page, outside manufacturer or distributor page, trade/farming/project article, or entity-specific public directory or profile. A non-company article, directory, registry, framework, or manufacturer page cannot satisfy `capability_source`; a company-owned page cannot satisfy `independent_corroboration`. If the same URL is submitted under both labels, one of the two roles must fail because a page cannot belong to both source classes.

Requirements:
- The page must identify the claimed company, or bridge the submitted trade name to a legal/trading name, with enough public context to distinguish it from unrelated same-name businesses and tie it to Great Britain, Northern Ireland, the Republic of Ireland, or a cross-border/all-island solar market.
- The submitted page itself must fulfill the claimed `evidence_type`: `capability_source` evidence must be an official company-owned, company-controlled, or otherwise official company capability/project/channel page for the submitted company, while `independent_corroboration` evidence must come from a separate non-company or high-authority public source for the submitted company.
- The page must support role-specific solar channel substance. For `capability_source`, the official company page must show agri/farm/rural commercial/ground-mounted/yard-mounted/non-domestic/C&I solar PV capability, project evidence, EPC/installer work, or distributor/wholesale channel capability. For `independent_corroboration`, the non-company or high-authority source must show a concrete public accountability, scheme, certification, association, framework, outside manufacturer/distributor, trade/project, or entity-directory fact for the same company, not just a name-only mention.

Write one JSON object per line to `results_agri_solar_channels.jsonl`:
{"item": { "company": "<company>", "evidence_type": "<evidence_type>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
