You are solving a research task that is organized as a task tree.

The root task defines the main deliverable. Some requirements are split into sidecar subtasks over overlapping entities (those subtasks may themselves have subtasks).

Treat it as one unit of work: solve the whole tree in one run, but write a separate JSONL file per task node.

## Task Tree
- `quantum_photonics_suppliers`
  - `quantum_photonics_suppliers.atom_ion_supplier_role`
  - `quantum_photonics_suppliers.window_signal`

## Universal rules

The following rules apply to every task (and subtasks) below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets. (Exception: in a subtask, the overlapping entities need only cover the parent's set. Non-overlapping axes still follow "more is better.")

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `quantum_photonics_suppliers`

For 25+ public suppliers of photonics, laser/reference, optical-control, timing/control, trap/atom optics, integrated photonics, or related enabling subsystems used in atom/ion quantum platforms, cover 2+ capability axes per supplier by supplying 1+ page-specific URL per supplier-axis pair.

Capability axes:
- `laser_wavelength_stack`: laser systems, laser heads, wavelength stacks, cooling, repump, clock, lattice, tweezer, or comparable species-specific optical wavelength capability
- `frequency_reference`: frequency combs, ultra-stable cavities, optical-frequency references, clock lasers, optical clocks, low-noise stabilized lasers, or related frequency-transfer infrastructure
- `control_timing`: quantum-control electronics, timing and synchronization systems, waveform generation, RF, microwave, AOM drivers, feedback, or real-time control infrastructure
- `trap_atom_optics`: ion-trap or atom-trap optics, trap-chip or foundry capability, SLMs, AODs, high-NA optics, wavefront sensing, integrated photonics, photonic packaging, or related atom/ion optical subsystems

Capability sources should be product pages, datasheets, application pages, technical project pages, official supplier pages, or comparable page-specific technical surfaces. Directories, marketplaces, buyer guides, market reports, rankings, broad quantum-overview pages, and vague supplier tags are discovery aids, not capability evidence.

Keep the work to public factual evidence. Do not rank suppliers, recommend vendors, enrich contacts, infer prices, negotiate procurement, draw export-control conclusions, or give technical design advice.

Requirements:
- The page must identify the named supplier and attribute the cited capability, product, project, or technical surface to that supplier.
- The page should be a page-specific capability surface for the claimed capability axis.
- The page must support a concrete capability finding for the claimed capability axis.
- The page must tie that capability to atom/ion, trapped-ion, neutral-atom, atomic-clock, cold-atom, optical-clock, ion-clock, or closely adjacent atom/ion quantum technology.
- A company page that only describes the named organization's own quantum computer, QPU, cloud service, or full-system platform does not count by itself. It counts only when the cited page establishes a qualifying enabling subsystem/component capability supplied by that organization, such as laser/reference, timing/control, trap/atom-optics, integrated-photonics, packaging, or comparable subsystem technology.

Write one JSON object per line to `results_quantum_photonics_suppliers.jsonl`:
{"item": { "supplier": "<supplier>", "capability_axis": "<capability_axis>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `quantum_photonics_suppliers.atom_ion_supplier_role`

Cross-tasknode identifier discipline: this task is for the same {= supplier =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= supplier =}+ suppliers, supply 1+ public URL per supplier establishing that the named organization has an atom/ion quantum supplier role.

Eligible role evidence can come from supplier, customer, project, institutional, government, award, technical, or comparable public pages. A supplier role means providing, developing, manufacturing, integrating, commercializing, or otherwise supplying a photonics, laser/reference, optical-control, timing/control, trap/atom optics, integrated-photonics, or related enabling subsystem for atom/ion, trapped-ion, neutral-atom, atomic-clock, cold-atom, optical-clock, ion-clock, or closely adjacent atom/ion quantum technology.

Directories, marketplaces, buyer guides, market reports, rankings, vague partner lists, and broad quantum pages without atom/ion supplier-role grounding do not count.

Requirements:
- The page must identify the named supplier.
- The page should be a suitable public source for supplier-role evidence.
- The page must support that the supplier has an atom/ion or closely adjacent atom/ion quantum supplier role.
- A company that only builds, operates, or sells its own quantum computer, QPU, cloud service, or full-system platform is not a qualifying supplier for this node. The page must establish an enabling subsystem/component supplier role for the named organization, or a separate product/technology surface showing that role.

Write one JSON object per line to `results_quantum_photonics_suppliers.atom_ion_supplier_role.jsonl`:
{"item": { "supplier": "<supplier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}

### `quantum_photonics_suppliers.window_signal`

Cross-tasknode identifier discipline: this task is for the same {= supplier =} instances requested above. Use the exact same identifier values in this task's item fields as you emitted in the parent to bind a submission to the same entity.

For {= supplier =}+ suppliers, supply 1+ public URL per supplier with a dated public activity signal from 2024-01-01 through 2026-05-17, inclusive.

The signal should name the supplier and describe a relevant customer, contract, award, deployment, partnership, technical project, public program, grant, letter of intent, or commercialization activity for atom/ion, trapped-ion, neutral-atom, atomic-clock, cold-atom, optical-clock, ion-clock, or closely adjacent quantum technology. Supplier-owned announcements can count when the dated event, counterpart, project, program, award, or commercialization activity is clear.

The date window applies to this activity or dated publication context. It does not date-gate timeless product pages elsewhere in the task. Directories, marketplaces, buyer guides, market reports, rankings, trusted-by logo walls, vague partner lists, acquisitions by themselves, out-of-window events, and broad quantum pages without a supplier-specific signal do not count.

Requirements:
- The page must name the supplier.
- The page must contain an explicit date or dated publication context inside the window.
- The page should be a suitable dated public source for an activity signal.
- The page must substantively describe a relevant supplier-specific activity signal.

Write one JSON object per line to `results_quantum_photonics_suppliers.window_signal.jsonl`:
{"item": { "supplier": "<supplier>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
