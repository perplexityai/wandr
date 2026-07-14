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

## `fiba_u20_women_sources`

For the 30 event teams listed here from the 2026 FIBA U20 Women's EuroBasket Division A and Division B fields, find at least 2+ distinct official publication states per team and supply a source for each state (i.e. 1+ URL).

The point is to map the official source trail for current youth national-team delegation facts, not to build a coach biography table. FIBA shells, federation team pages, preparation releases, staff announcements, and final roster/delegation releases can all matter at different moments before and during the tournament.

Event teams in scope:
- **Division A - Belgium**
- **Division A - Croatia**
- **Division A - France**
- **Division A - Germany**
- **Division A - Hungary**
- **Division A - Iceland**
- **Division A - Israel**
- **Division A - Italy**
- **Division A - Latvia**
- **Division A - Lithuania**
- **Division A - Poland**
- **Division A - Serbia**
- **Division A - Slovenia**
- **Division A - Spain**
- **Division A - Sweden**
- **Division A - Turkiye**
- **Division B - Albania**
- **Division B - Azerbaijan**
- **Division B - Bosnia and Herzegovina**
- **Division B - Bulgaria**
- **Division B - Czechia**
- **Division B - Greece**
- **Division B - Ireland**
- **Division B - Montenegro**
- **Division B - Netherlands**
- **Division B - Portugal**
- **Division B - Romania**
- **Division B - Slovakia**
- **Division B - Switzerland**
- **Division B - Ukraine**

Source phases:
- `fiba_event_team_shell`: official FIBA event/team shell, team-list entry, or equivalent event page
- `federation_team_hub`: official federation U20 women's national-team hub or current season team page
- `federation_dated_preparation_or_roster_release`: dated federation preparation, training, preliminary roster, final roster, or tournament-preview release
- `federation_staff_announcement`: official federation staff or coach appointment page tied to U20 women / the 2026 campaign
- `fiba_final_roster_or_release`: official FIBA final roster, delegation page, team roster page, or final-roster news release

For each source, state the roster/delegation publication state the page supports and any staff roles or staff names visible on that same page. Staff facts count only when the cited official page itself exposes them. As source notes, include the page title or source label, source date if visible, and checked date.

Sources must be official FIBA surfaces, official national federation surfaces, or clearly federation-controlled official channels. Third-party roster aggregators, databases, fan sites, media previews, player-school pages, betting/fantasy/recruiting pages, and private/social-profile enrichment do not count.

Requirements:
- The page must tie the source to the claimed event team and to U20 women, the 2026 FIBA U20 Women's EuroBasket / Division B campaign, or a clearly current 2025/2026 U20 women's national-team context. Generic senior-team pages and generic federation pages without that tie do not count.
- The page must fit the claimed source phase. A FIBA team profile can count as an event shell even when it has no roster; a federation team hub can count when it is visibly a U20 women's national-team hub; a dated federation article can count for preparation, roster, or staff announcement only when the article itself ties to the relevant team/campaign.
- The page must support the submitted publication-state classification. Preliminary, preparation, final, stale, mixed-season, undated shell, and no-staff-visible-on-this-page states are fine when the claim is restrained to this cited page as checked. Do not turn a missing/no-staff state on one page into a claim that no official source exists anywhere.
- The page must support the submitted date, currentness, or finality classification through a visible date, event date, season label, 2026 campaign tie, final/preliminary wording, or a restrained stale/mixed/undated classification.
- Named staff, role, tenure, or continuity facts are optional and must be copied only from the cited official page. Do not infer staff continuity from prior-year pages, preparation-game articles, or roster timing unless the official source says it.

Write one JSON object per line to `results_fiba_u20_women_sources.jsonl`:
{"item": { "event_team": "<event_team>", "source_phase": "<source_phase>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
