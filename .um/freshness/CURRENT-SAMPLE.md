# Current-catalog evaluation: 60 fresh entries

The larger sample found **two clear factual corrections and three factually supported but optional wording improvements**. All 20 workflow runs completed, and 5 proposed patches passed history and mechanical validation. This demonstrates useful semantic research, but the workflow does not yet distinguish necessary corrections from optional editorial changes.

## Scope and results

Evaluated November 9, 2026 (Pacific), using Opus 5.5 medium and workflow revision `18177f0eb39d57b81d8aadc0c6ef8f72bd7fe194`. The current upstream catalog was pinned at `968f13c81044e2815bee481b163446e8eb8aebce`. All 60 entries were new to this evaluation, excluding earlier pilot and backtest entries and their renamed identities.

The sample covers all 28 subsections: two entries from each, plus one additional entry from each of the four largest eligible subsections. Selection used a fixed SHA-256 seed before model execution. This oversamples small subsections; it is not a uniform sample for estimating catalog-wide error rates.

| Measure | Result |
| --- | --- |
| Entries assessed | 60 of 586 |
| Live seven-stage workflow runs | 20/20 completed |
| Keep recommendations | 55 |
| Update recommendations | 5 |
| Removal/replacement recommendations | 0 |
| Ready preview patches | 5 |
| Proposals held | 0 |
| Recommendations independently reviewed | 5 of 5 |
| Keep decisions independently spot-checked | 12 |
| Recorded model usage equivalent | $13.49 |
| Workflow wall time, three concurrent batches | 13.1 minutes |
| Median batch without a proposed edit | 38.4 seconds |
| Slowest batch with an edit | 5.1 minutes |

This was a local UM run with the production agent prompts, schemas, history retrieval and validators. Only the three-entry selection was adapted. Current-upstream freshness checks remained active. The workflow was frozen throughout; no prompts, gates or unfavorable model outputs were changed or retried. Recorded costs are Claude usage equivalents, not a claim about an additional subscription charge.

## Findings and independent review

| Entry | Evaluator classification | Workflow preview |
| --- | --- | --- |
| glues | Factual correction | Ready |
| tui-box-text | Factual correction | Ready |
| amtr | Optional wording improvement | Ready |
| passepartui | Optional wording improvement | Ready |
| ratatui-image | Optional wording improvement | Ready |

**glues — factual correction.** The catalog advertises Git, CSV and JSON support. Current docs and source expose memory, local files, redb, Git, MongoDB and proxy backends. The TUI storage menu and core entry handler have no CSV/JSON note option. CSV remains an internal configuration store, which is different from offering it as a note backend. The proposal removes the obsolete storage claims. Verified against the [README](https://github.com/gluesql/glues/blob/main/README.md), [storage menu](https://github.com/gluesql/glues/blob/main/tui/src/context/entry.rs), [core entry handler](https://github.com/gluesql/glues/blob/main/core/src/state/entry.rs), and [configuration implementation](https://github.com/gluesql/glues/blob/main/tui/src/config.rs).

**tui-box-text — factual correction.** The catalog says it displays text surrounded by a box. The widget actually renders large letter glyphs made from box-drawing characters. Its `BoxChar` implementation looks up a glyph table and writes the glyph into buffer cells; it does not surround text with a border. Verified against the [crate README](https://github.com/ratatui/tui-widgets/blob/main/tui-box-text/README.md) and [rendering source](https://github.com/ratatui/tui-widgets/blob/main/tui-box-text/src/lib.rs).

**ratatui-image — optional enrichment.** Adding Kitty and iTerm2 support is factually correct, but the existing statement about Sixel and Unicode half-blocks remains true and does not explicitly claim to list every backend. Verified against [crate metadata](https://crates.io/api/v1/crates/ratatui-image) and the [README](https://github.com/ratatui/ratatui-image/blob/master/README.md).

**amtr — optional scope expansion.** It now supports Codex CLI, Gemini CLI and OpenCode as well as Claude Code. The original Claude Code capability is still true; its own README headline still describes it as a debugger for Claude Code. Broadening the catalog description is useful but not a demonstrated correction of a false claim. Verified against the [README](https://github.com/arian-shamaei/anthropometer/blob/main/README.md) and [Rust manifest](https://github.com/arian-shamaei/anthropometer/blob/main/rust/Cargo.toml).

**passepartui — optional precision.** Its README explicitly says it cannot add or delete passwords. Describing browsing, searching and copying is more precise than “managing,” but that generic original word does not explicitly promise editing. The independent review recorded this as optional precision before reading the model's recommendation; it is not counted as an objective stale-entry fix. Verified against the [README](https://github.com/kardwen/passepartui/blob/main/README.md).

All five suggestions are factually supported. Only two satisfy the stricter evaluator criterion of correcting a clear factual error. This is a distinction between necessity and factual support, not evidence that three suggestions contain false information.

## Keep audit

A deterministic 12-entry sample of keep decisions was checked independently against official READMEs, canonical repository metadata and manifests. Workspace members were inspected for wrkflw and vincenzo rather than judging their root manifests alone. The sampled entries were: traxor, hustle-tracker, timr-tui, tubetui, tts-tui, wrkflw, rrtop, noble, vincenzo, bluetui, absorb, ratatui-wasm.

No confirmed missed correction was found in those 12. Older tui-rs projects were not incorrectly discarded for inactivity, and Ratatui's supporting tools remained in scope. This does not prove the other keep decisions correct or establish recall. Source snapshots, blob identities and per-entry evaluator reasoning are retained in `audit-sources/` and `keep-audit.json`.

## What the bigger run exposed

1. **Optional edits are mixed with corrections.** The same update action and ready status cover factual errors and feature-list expansion. Ready currently means the proposal passed history and mechanical checks; it does not mean the edit is necessary. Add a correction-versus-editorial distinction before relying on ready status to prioritize work.
2. **History search can miss changes mentioned only in diffs.** The tui-box-text searches returned no records, but local Git history shows [PR #444](https://github.com/ratatui/awesome-ratatui/pull/444) added the entry. Its title/body do not name the crate; the name appears in its README diff. This missed related context did not conceal a known competing correction here, but demonstrates a real coverage gap in title/body/comment search. A file-history/diff fallback would improve it.
3. **Repeated full-catalog link checks dominate edit latency.** The validators encountered HTTP 429 responses on unrelated GitLab URLs. Matching baseline and patched failures were correctly reported as pre-existing, while changed destinations were positively verified. No rate-limit failure was interpreted as a dead project. Reusing a baseline for the same catalog revision would reduce repeated traffic and delay; the observed rate limiting may also reflect shared network conditions.
4. **Research sometimes used unauthenticated API calls.** 27 entry assessments mentioned API rate limits. The models generally recovered through raw official files and HTML, but authenticated reads should be preferred consistently. The read-only credential was available; the independently checked authenticated quota was not exhausted.
5. **Empty history reviews still incur model calls.** 15 history-agent sessions had no candidates, accounting for approximately $1.09. A deterministic empty-result path would avoid that work.

No correction PRs, issues or comments were submitted. These are current-catalog advisory previews, unlike the earlier historical replays. The two factual corrections are the strongest candidates for maintainer review; the other three should be labeled optional. Before a full-catalog sweep, prioritize clearer edit classification, a history fallback, and less repetitive network validation.

## Retained evidence

The evaluation directory is `targets/awesome-ratatui/current-sample-60-20261109/`. It contains the predeclared protocol and manifest, isolated execution runner, all reports and model transcripts, checker logs, independent source snapshots, proposal reviews, keep audit, summary and operational metrics. Raw per-batch reports use slice 0 as the transport input; the actual stratified entry IDs are recorded in each catalog packet and the manifest. No historical cutoff or synthetic freshness override was used.
