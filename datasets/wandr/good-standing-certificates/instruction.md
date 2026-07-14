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

## `good_standing_certificates`

For each of the 51 U.S. state and DC filing jurisdictions listed below, supply official home-jurisdiction evidence for each of the 3 evidence roles below, with 1+ URL per jurisdiction and role. The evidence should document the jurisdiction's currently published business-entity certificate used to show good standing, status, existence, compliance, subsistence, authority, or the local equivalent.

Official sources can be home-jurisdiction business-filing office pages, official state business portals, agency PDFs/forms/fee schedules, or official statute/regulation pages. Third-party certificate vendors, law-firm guides, cross-state comparison lists, and another jurisdiction's certificate-name table do not count.

The same official URL can support multiple roles when the page really carries each role's evidence.

Target jurisdictions:
- **Alabama** (also written as: AL, State of Alabama)
- **Alaska** (also written as: AK, State of Alaska)
- **Arizona** (also written as: AZ, State of Arizona)
- **Arkansas** (also written as: AR, State of Arkansas)
- **California** (also written as: CA, State of California)
- **Colorado** (also written as: CO, State of Colorado)
- **Connecticut** (also written as: CT, State of Connecticut)
- **Delaware** (also written as: DE, State of Delaware)
- **District of Columbia** (also written as: DC, D.C., Washington DC, Washington D.C., Washington, DC, Washington, D.C.)
- **Florida** (also written as: FL, State of Florida)
- **Georgia** (also written as: GA, State of Georgia)
- **Hawaii** (also written as: HI, State of Hawaii)
- **Idaho** (also written as: ID, State of Idaho)
- **Illinois** (also written as: IL, State of Illinois)
- **Indiana** (also written as: IN, State of Indiana)
- **Iowa** (also written as: IA, State of Iowa)
- **Kansas** (also written as: KS, State of Kansas)
- **Kentucky** (also written as: KY, Commonwealth of Kentucky)
- **Louisiana** (also written as: LA, State of Louisiana)
- **Maine** (also written as: ME, State of Maine)
- **Maryland** (also written as: MD, State of Maryland)
- **Massachusetts** (also written as: MA, Commonwealth of Massachusetts)
- **Michigan** (also written as: MI, State of Michigan)
- **Minnesota** (also written as: MN, State of Minnesota)
- **Mississippi** (also written as: MS, State of Mississippi)
- **Missouri** (also written as: MO, State of Missouri)
- **Montana** (also written as: MT, State of Montana)
- **Nebraska** (also written as: NE, State of Nebraska)
- **Nevada** (also written as: NV, State of Nevada)
- **New Hampshire** (also written as: NH, State of New Hampshire)
- **New Jersey** (also written as: NJ, State of New Jersey)
- **New Mexico** (also written as: NM, State of New Mexico)
- **New York** (also written as: NY, N.Y., New York State, State of New York)
- **North Carolina** (also written as: NC, State of North Carolina)
- **North Dakota** (also written as: ND, N.D., State of North Dakota)
- **Ohio** (also written as: OH, State of Ohio)
- **Oklahoma** (also written as: OK, State of Oklahoma)
- **Oregon** (also written as: OR, State of Oregon)
- **Pennsylvania** (also written as: PA, Commonwealth of Pennsylvania)
- **Rhode Island** (also written as: RI, State of Rhode Island)
- **South Carolina** (also written as: SC, State of South Carolina)
- **South Dakota** (also written as: SD, State of South Dakota)
- **Tennessee** (also written as: TN, State of Tennessee)
- **Texas** (also written as: TX, State of Texas)
- **Utah** (also written as: UT, State of Utah)
- **Vermont** (also written as: VT, State of Vermont)
- **Virginia** (also written as: VA, Commonwealth of Virginia)
- **Washington** (also written as: WA, Washington State, State of Washington)
- **West Virginia** (also written as: WV, State of West Virginia)
- **Wisconsin** (also written as: WI, State of Wisconsin)
- **Wyoming** (also written as: WY, State of Wyoming)

Evidence roles:
- `document_identity`: the official certificate name or variant and the standing/status/existence/compliance/subsistence/authority meaning it carries
- `fee_or_fee_schedule`: the raw official amount, free status, or fee-table entry, preserving the certificate/entity/channel/portal-fee scope shown by the source
- `request_or_access`: the official mechanics for ordering, requesting, checking, or otherwise accessing the certificate

Requirements:
- The page must communicate (possibly via URL among other things) that it is a home-jurisdiction official source for that jurisdiction's business-entity filing or certificate system.
- The page must tie the cited certificate evidence to the claimed jurisdiction and to a business-entity certificate that evidences good standing, status, existence, compliance, subsistence, authority, or the jurisdiction's equivalent.
- The page must satisfy the claimed `evidence_role`: for `document_identity`, identify the certificate name or official variant and the standing/status/existence/compliance/subsistence/authority meaning; for `fee_or_fee_schedule`, state the raw official amount, free status, or fee-table entry with enough surrounding scope to know what certificate/entity type/channel/portal fee it covers; for `request_or_access`, explain how the certificate is requested, ordered, checked, or accessed through official channels.

Write one JSON object per line to `results_good_standing_certificates.jsonl`:
{"item": { "jurisdiction": "<jurisdiction>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
