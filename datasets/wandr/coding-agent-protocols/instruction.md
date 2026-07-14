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

## `coding_agent_protocols`

For each of the 2 protocols listed below, cover the 4 role lanes listed for that protocol. Within each role lane, cover 6+ public implementations connected to AI coding agents, terminal or IDE coding clients, adapters, agent registries, SDKs, or coding-agent extension ecosystems; for each implementation, cover the 4 evidence facets listed below by supplying an official source (i.e. 1+ URL under each facet).

This is a protocol-boundary interoperability study, not a tool recommendation table. The evidence should show how protocol support is implemented, configured, controlled, distributed, or governed.

Protocols:
- `mcp`: Model Context Protocol support in coding-agent or developer-agent workflows.
- `acp`: Agent Client Protocol support for communication between coding agents and editor, IDE, client, adapter, or registry surfaces.

Protocol role lanes:
- `mcp`:
  - `agent_consumes_protocol`: A coding agent, terminal agent, IDE agent mode, or developer-agent client directly consumes MCP servers, tools, prompts, or resources.
  - `adapter_bridges_agent_to_protocol`: A bridge, proxy, adapter, SDK wrapper, or compatibility layer connects a coding-agent workflow to MCP rather than being the agent product itself.
  - `editor_or_client_hosts_agent`: An editor, IDE, terminal client, or coding-agent host exposes MCP tools to coding-agent workflows or lets users configure MCP servers for them.
  - `extension_or_server_ecosystem_for_coding_agent_use`: An extension, server, plugin, or server-definition ecosystem is presented for use by coding agents or developer-agent clients through MCP.
- `acp`:
  - `agent_implements_external_agent_protocol`: A coding agent or terminal agent runs as an ACP-compatible agent/server that ACP clients can launch or connect to.
  - `adapter_bridges_agent_to_protocol`: A maintainer-controlled adapter exposes a coding agent through ACP or translates between ACP clients and the agent's native interface.
  - `editor_or_client_hosts_agent`: An editor, IDE, extension, or client hosts ACP agents or lets users configure external coding agents over ACP.
  - `registry_or_distribution_surface`: A registry, package, marketplace, or distribution surface lists, verifies, installs, or updates ACP agents, adapters, or client integrations.

Evidence facets:
- `implementation_claim`: a role-appropriate primary source directly shows that the named project has the submitted role for the submitted protocol.
- `configuration_or_transport_detail`: a technical setup, reference, README, schema, source, or configuration page gives concrete mechanics, such as command invocation, config files, JSON-RPC over stdio, HTTP or WebSocket transport, OAuth or bearer auth, MCP server setup, adapter invocation, registry installation, or equivalent protocol-specific mechanics.
- `control_or_security_boundary_detail`: a security, configuration, permissions, auth, trust, sandboxing, storage, or delegation source shows concrete protocol-boundary controls, such as who owns authentication, tool permissions, approval decisions, sandbox/trust boundaries, token/config/log storage, allowlists, or client-to-agent delegation.
- `distribution_or_provenance_detail`: a package, registry, marketplace, release, manifest, extension-listing, or provenance source shows concrete distribution evidence, such as owner or maintainer identity, package or extension identifier, version or update channel, install source, release artifact, registry verification, or published distribution metadata.

Sources should be official or maintainer-controlled protocol docs, product docs, project repositories, release notes, security/configuration docs, official editor/client docs, official adapter repositories, package/marketplace pages, or official registry pages. The source role must match the submitted role and facet: native product, agent, adapter, and client roles need product-owned docs, maintainer-owned adapter repositories, official client docs, or comparable primary sources that directly establish that role. Registry pages and raw protocol-registry metadata count for registry/distribution-surface records, but registry presence alone does not establish native product/agent support or adapter/client behavior. Package registries, extension marketplaces, release pages, package manifests, plugin manifests, and similar metadata count for the submitted implementation's own distribution/provenance facet when they identify the implementation itself. A broad official overview page does not count for a technical, control, or distribution facet merely because it contains a protocol mention; the page or cited section should visibly be a setup/reference/configuration source, a security/control-boundary source, or a distribution/provenance source for the submitted implementation. Third-party comparisons, procurement roundups, Reddit/forum commentary, and pages that merely say "AI agent", "agentic", or "supports tools" without protocol-specific evidence do not count. Generic MCP servers unrelated to coding-agent or developer-agent workflows do not count unless the source ties them to a coding-agent, client, adapter, or developer-agent ecosystem. Visible source dates, version labels, beta/deprecation markers, and checked dates should be preserved when they affect the claim; undated current docs are fine.

Requirements:
- The page and URL must communicate the appropriate source role for the submitted protocol role and evidence facet: product/agent/client/adapter roles require primary sources for that implementation, registry/distribution roles may use registry or metadata authority, configuration facets require technical setup/reference/source shape, control facets require security/auth/permission/trust/sandbox/storage/delegation shape, and distribution facets require package/registry/marketplace/release/manifest/provenance shape.
- The page must directly tie the named project or agent to the submitted protocol and role, preserving distinctions such as native support versus adapter-mediated support, agent implementation versus client hosting, registry distribution versus product implementation, and MCP client/consumer behavior versus MCP server/extension behavior.
- The page must provide the evidence required by `evidence_facet` at the corresponding bar: protocol implementation/adoption claim, concrete configuration/transport mechanics, protocol-boundary control/security behavior, or package/registry/release/distribution provenance.

Write one JSON object per line to `results_coding_agent_protocols.jsonl`:
{"item": { "protocol": "<protocol>", "role": "<role>", "project_or_agent": "<project_or_agent>", "evidence_facet": "<evidence_facet>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
