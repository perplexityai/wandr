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

## `llmops_provenance`

For 25+ public LLM/agent observability, evaluation, prompt-management, tracing, or AI-gateway products, cover each of the 3 workflow areas below; for every platform-area pair, cover 2+ distinct source-surface classes, and for each platform-area-surface cell supply 1+ dated capability or source-state event from 2024-01-01 through 2026-07-01, backed by 1+ first-party public source URL.

This is a public provenance ledger for the observe/evaluate/improve loop, not a product ranking, recommendation, benchmark verdict, pricing recommendation, implementation guide, architecture guide, or Langfuse-only canon.

The workflow areas of interest, which we refer to as `workflow_area`, are:
- `observe`: tracing, spans, observations, sessions, logs, token or cost telemetry, AI-gateway request observability, agent trace / step metadata, monitoring, dashboards, alerts, or comparable runtime visibility.
- `evaluate`: scores, evals, datasets, experiments, LLM-as-judge, human review, annotation queues, feedback workflows, dataset item curation, online or offline evaluation, or comparable quality-measurement workflows.
- `improve_operate`: prompt versioning or labels, playgrounds, deployment or experiment workflows, SDK / instrumentation / standards support, self-hosting or deployment state, source/license/source-availability state, rebrands, acquisitions, shutdowns, deprecations, or comparable public operating state.

The first-party source-surface classes, which we refer to as `source_surface`, are:
- `release_or_changelog`: dated changelog entries, release-note entries, versioned release posts, GitHub releases/tags, or comparable official release streams. Prefer entry-specific or release-specific URLs when they exist; a broad changelog index qualifies only when excerpts localize the exact dated entry.
- `docs_or_standard`: official docs, API/SDK/instrumentation/standards pages, repository docs/README/LICENSE pages, integration docs, or comparable source-state pages whose visible page or section itself carries the dated event/source-state. Broad undated docs overviews do not qualify.
- `product_or_lifecycle`: first-party product or release blog posts, acquisition/rebrand/shutdown/deprecation posts, pricing/self-host/deployment/source-availability posts, or comparable lifecycle/source-state pages that directly carry the dated event.

Platforms are open-set. Generic APM / observability vendors count only when the cited product or module explicitly targets LLM, GenAI, or agent observability/evaluation/prompt/gateway work. Generic model providers, vector databases, bare prompt playgrounds, and ordinary observability pages do not count without that LLM/agent-workflow evidence.

The source should preserve the platform's current or canonical name, the source-stated feature / artifact / product term, the event or source-state claim, the chosen `source_surface`, the source's visible date or date bucket, the checked date, and confidence where those are not already obvious from excerpts. Use the source's actual date granularity: exact day, date range, month-only page, release timestamp, bundled release-list date, frozen/tombstone date, or similar.

Accepted first-party sources include official docs, changelog / release notes, first-party product or release blog posts, GitHub releases or tags, repository docs / README / LICENSE when the cited source-state is visible, SDK / API / integration docs, standards or instrumentation docs, pricing / self-host / deployment pages, and first-party acquisition, rebrand, shutdown, or deprecation posts. Classify each row into the most specific `source_surface` above; do not use the same broad changelog or release-index URL as the only proof for both required source-surface cells of a platform-area pair.

Third-party listicles, vendor "alternatives" pages, Reddit/community threads, news articles, and third-party developer blog posts can help find candidates, but they do not prove a platform's positive capability or source-state claim here. Vendor-authored competitive comparisons do not prove a rival's capability. Missing/no-source states do not count unless the cited first-party source itself directly demonstrates a public state such as sunset, removal, deprecation, rebrand, gated availability, or source/deployment status.

Requirements:
- The page must be a first-party public source for the claimed platform, project, or owning organization.
- The page must visibly attach the claimed event or source-state to a source date or date bucket from 2024-01-01 through 2026-07-01; after-window events are outside scope.
- The page must substantiate a distinct shipped capability, release, documented current source-state, rebrand, acquisition, sunset, deprecation, standards/SDK/deployment/source state, or comparable public event for the claimed platform and `workflow_area`.
- The page must expose source-stated terminology more specific than the normalized workflow area alone: a feature name, release title, version or tag, API / SDK / instrumentation label, source-state wording, product term, or comparable artifact anchor.
- The page and excerpts must fit the claimed `source_surface`; a broad root changelog, release index, or docs index cannot satisfy a different source-surface class merely because it links to or summarizes material from that class.

Write one JSON object per line to `results_llmops_provenance.jsonl`:
{"item": { "platform": "<platform>", "workflow_area": "<workflow_area>", "source_surface": "<source_surface>", "capability_event": "<capability_event>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
