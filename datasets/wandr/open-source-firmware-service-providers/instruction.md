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

## `open_source_firmware_service_providers`

For 200+ organizations with public evidence of open-source firmware service or delivery capability, supply 1+ URL for each of the 4 evidence aspects listed below. The task is descriptive provenance only: inclusion means public evidence exists, not that the organization is recommended, ranked, procurement-ready, commercially superior, or worth contacting.

Open-source firmware includes below-OS and firmware-adjacent open stacks such as host firmware, boot firmware, BMC firmware, bootloaders, RTOS or MCU firmware, firmware update systems, trusted firmware, embedded-controller firmware, platform firmware distributions, and embedded Linux when it is used as firmware. Named projects such as coreboot, Dasharo, OpenBMC, U-Boot, Zephyr, TianoCore/EDK II, LinuxBoot, fwupd/LVFS, Trusted Firmware, and MCUboot are examples, not a closed universe.

Evidence aspects:
- `service_capability`: a provider-owned official page that names an in-scope open firmware stack, service, support program, engineering capability, training capability, productized distribution, or comparable provider capability.
- `open_source_role`: stated contribution, maintainer role, authored open-source firmware repository or tool, project membership, upstream integration work, or equivalent active open-source role. Passive forks, mirrors, or unmaintained copies do not count.
- `ecosystem_presence`: third-party community, foundation, project, conference, standards, OCP-style, Zephyr/coreboot-style, or comparable ecosystem evidence that names the organization and ties it to an in-scope firmware ecosystem.
- `concrete_offering_or_delivery`: public product, distribution, integration, case study, press release, training or support program, deployment claim, platform enablement, or delivery evidence tied to an in-scope open firmware stack.

Sources should be fully public, accessible, and usable. Generic embedded-firmware or software-outsourcing pages do not count unless they name or clearly tie the provider to an in-scope open firmware stack or active open-source firmware role. Job postings, contact details, sales lead lists, private customer targeting, generic market-size pages, and provider rankings are outside the task.

Requirements:
- The page must clearly identify the named provider organization.
- The page must clearly tie the provider to an in-scope open-source firmware project, stack, domain, or below-OS open firmware ecosystem.
- The page should make its evidence-aspect-appropriate source role visible. For `service_capability`, it should read as the provider's own official capability or offering surface. For `open_source_role`, it should show active open-source participation such as authored tooling, upstream contribution, maintainership, membership, or project work. For `ecosystem_presence`, it should read as an independent ecosystem/community/project/conference/foundation surface. For `concrete_offering_or_delivery`, it should describe a public product, distribution, integration, deployment, platform enablement, case study, support/training program, or delivery claim.
- The page should expose a concrete finding for the named provider and evidence aspect, not just a generic firmware keyword or a broad company description.

Write one JSON object per line to `results_open_source_firmware_service_providers.jsonl`:
{"item": { "provider": "<provider>", "evidence_aspect": "<evidence_aspect>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
