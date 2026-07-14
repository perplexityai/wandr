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

## `fed_it_primes`

For each of the 8 selected federal IT contract vehicles listed below, supply side-specific source evidence (1+ URL per side) for 20+ prime awardees per vehicle, identifying each awardee by legal name or UEI. Each (`vehicle`, `legal_name_or_uei`) pair needs evidence for each of the 3 evidence sides listed below.

Selected federal IT contract vehicles:
- **NITAAC CIO-SP3**
- **NITAAC CIO-SP3 Small Business**
- **NITAAC CIO-CS**
- **GSA 8(a) STARS III**
- **GSA Alliant 2**
- **GSA Polaris**
- **GSA VETS 2**
- **GSA MAS IT SIN 54151S**

The evidence sides, referred to as `evidence_side`, are:
- `roster_placement`: an official U.S. government source showing that the submitted legal entity, joint venture, or UEI is a prime awardee, contract holder, schedule holder, or roster holder for the named vehicle.
- `business_standing`: an official U.S. government source showing current or source-dated business standing for the submitted legal entity or UEI, such as business size, socioeconomic designation, pool/set-aside status, active entity status, recipient business type, or an explicit no-designation / other-than-small status.
- `vendor_capability`: an awardee-controlled source showing concrete IT service capability relevant to federal work or to the named vehicle, such as cloud, cybersecurity, systems integration, software development, data/analytics, health IT, infrastructure, help desk, managed services, or comparable IT professional services.

Use NITAAC contract-holder directory pages only for contract-holder facts such as contract holder name, contract number, PIID, contract type, SAM UEI, task areas, business size, business type, and contract URL. Do not use person-level details, direct outreach channels, or office-location blocks as evidence.

Requirements:
- The page must clearly identify the submitted awardee entity by legal name, recognizable awardee name, joint-venture name, UEI, or a first-party brand identity that is unambiguously tied to the submitted legal entity.
- The page must have the source role required by `evidence_side`: official U.S. government roster or award-system evidence for `roster_placement`; official U.S. government entity, recipient, roster, award, schedule, or registration evidence for `business_standing`; awardee-controlled web evidence for `vendor_capability`.
- The page must substantiate the side-specific attestation: for `roster_placement`, that the entity is a prime awardee / contract holder / roster holder for the named vehicle; for `business_standing`, the entity's current or source-dated official business standing; for `vendor_capability`, a concrete IT service capability relevant to federal work or the named vehicle.

Write one JSON object per line to `results_fed_it_primes.jsonl`:
{"item": { "vehicle": "<vehicle>", "legal_name_or_uei": "<legal_name_or_uei>", "evidence_side": "<evidence_side>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
