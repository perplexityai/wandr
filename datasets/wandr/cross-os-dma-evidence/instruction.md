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

## `cross_os_dma_evidence`

For each of the 5 operating systems and each of the 4 DMA scoping lenses, name 2+ distinct concrete scope anchors. Under each scope anchor, name 2+ distinct scoped DMA signals. For every scoped signal, supply each of the 2 public-evidence roles with 1+ public URL per role.

This is a factual public-evidence comparison of DMA semantics. It is not a driver tutorial, exploit guide, performance-tuning guide, or proof that a cross-OS DMA abstraction is correct. Scope labels from the page, such as version, architecture, driver framework, bus, public-header status, or limited-support wording, should stay attached to the signal when they limit the claim.

The operating systems are:
- `Linux`
- `Windows`
- `FreeBSD`
- `macOS`
- `Zephyr`

The DMA scoping lenses are:
- `version_or_release_specific`: a DMA behavior tied to a named OS release, kernel/API version, interface version, branch/tag, dated manual, or versioned documentation scope.
- `architecture_or_bus_specific`: a DMA behavior tied to a named CPU architecture, platform, SoC, bus, device class, address-width model, cache-coherency model, IOMMU/mapper, or bounce buffer condition.
- `driver_framework_or_subsystem_specific`: a DMA behavior tied to a named public driver framework, kernel subsystem, DMA controller API, bus-DMA layer, driver-family interface, or official sample family rather than to the whole OS.
- `unsupported_limited_or_conflict`: a DMA limitation, unsupported case, exception, documented absence, non-portability statement, deprecation, or conflict between public evidence surfaces where the page states the scope of the caveat.

The public-evidence roles are:
- `doc_semantics`: official OS/project documentation, manual pages, API reference, or official driver documentation that explains the scoped DMA behavior in prose. Raw headers or source without explanatory text are not enough for this role.
- `public_interface_or_source`: official project/vendor-hosted public source, public header, public interface declaration, official sample, or official doc-source evidence exposing declaration-level or code-like public DMA constructs. Official API references count only when they visibly expose signatures, prototypes, types, enums, members, code samples, or similar public interface content; narrative documentation alone does not. Unofficial mirrors do not create independent source standing.

Requirements:
- The page must communicate source standing appropriate to `evidence_role`: official explanatory DMA documentation for `doc_semantics`, or official public declaration/source/header/sample/doc-source evidence exposing an interface or code-like construct for `public_interface_or_source`. Official narrative documentation can support `doc_semantics`; it supports `public_interface_or_source` only when it visibly exposes declaration-level public interface content. Community posts, third-party driver code, decompilations, blogs, forums, Q&A pages, and unofficial mirrors do not count as primary evidence here.
- `scope_anchor` must preserve a concrete narrowing token from the page: a named release/API version, architecture, platform, bus, coherency/IOMMU/address-width condition, driver framework, kernel subsystem, source/header path, official sample family, or page-stated limitation/conflict/unsupported scope. Generic anchors such as "DMA API", "driver documentation", "public header", "architecture", "framework", or "limitation" do not count unless they include the concrete page-supported token that narrows the claim.
- The page must tie its DMA content to the claimed operating system, `scope_lens`, and `scope_anchor`. The same `dma_signal` must preserve that anchor under both evidence roles; a documentation page and a source/interface page cannot be paired if they only share a generic DMA topic.
- The page must directly support `dma_signal` as a concrete scoped DMA operation, policy, lifecycle rule, interface constraint, cache or coherency responsibility, segment/list behavior, addressability/translation limit, controller/channel setup rule, or documented absence/limited-scope statement. A generic "this OS has DMA docs" or "this page mentions DMA" signal does not count.

Write one JSON object per line to `results_cross_os_dma_evidence.jsonl`:
{"item": { "os": "<os>", "scope_lens": "<scope_lens>", "scope_anchor": "<scope_anchor>", "signal": "<signal>", "evidence_role": "<evidence_role>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
