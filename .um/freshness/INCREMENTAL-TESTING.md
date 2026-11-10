# Incremental workflow trial — 2026-11-10

This revision adds a persisted review baseline and model-free source comparison.
It contains no budget gate, schedule, or rotating sample.

## Full-catalog source inventory

The model-free collector examined all **586 entries** in the pinned catalog
`968f13c81044e2815bee481b163446e8eb8aebce`:

- 576 complete source snapshots.
- 10 incomplete snapshots, retained as pending.
- **Zero model calls.**

The inventory was approximately 1.17 MB. Seven incomplete entries were crates.io
sources for which the collector could not establish its required repository
snapshot; three failed GitHub requests. An incomplete snapshot does not establish
that a project is dead, incorrect, or unchanged. Inventory generation does not
constitute review and is never imported as a completed baseline.

## Live initial and repeat runs

The production workflow reviewed slice 1: `dumo`, `egui-ratatui`, and `mousefood`.
All three received supported keep recommendations. Their actual completed reviews,
source fingerprints and evidence are included in `baseline.json` in this PR.

| Scenario | Entries researched | Entries skipped | Model sessions | Recorded usage equivalent | Wall time |
| --- | ---: | ---: | ---: | ---: | ---: |
| Initial review, no baseline | 3 | 0 | 1 | $0.4055 | 42.07 s |
| Same entries, saved baseline | 0 | 3 | 0 | **$0** | **3.48 s** |
| One controlled source change | 1 | 2 | 1 | $0.1928 | 19.02 s |

For the controlled-change test, only dumo's *previous snapshot* was altered to
represent an earlier repository description. Live evidence fetching and Opus
research remained real. No upstream source was modified. The selector identified
dumo as source-changed and skipped both controls. This tests routing, not the
accuracy of detecting a naturally occurring new defect.

Both research runs had no correction candidates. No history model was started and
no full-catalog correction validators were run. The unchanged run executed only
preparation and reporting; the six research/correction stages were skipped.

A separate live test of the conditional history command reused three labeled
history cases: related context, duplicate correction and explicit rejection.
Opus returned all three expected classifications, using $0.038272 of recorded
usage equivalent. The model-free history path is also tested to reject any attempt
to start a model when there are no candidates.

All live model tests used local Claude Code authentication. The dollar figures are
reported model-usage equivalents, not a claim of additional subscription charges.
They do not establish future monthly costs or savings for changed entries.

## Regression and integration checks

- 57 offline tests, including initial/unchanged/changed selection, catalog/rule
  changes, stable identity despite line shifts, fetch failure, unresolved reviews,
  source changes during research, workspace manifests, and truncated source trees.
- Actual UM graph tests for correction, keep-only and unchanged scenarios.
- Real validation-tool fixtures verify that invalid edits are held and a positively
  checked destination is accepted.
- Native workflow schema validation passes.

Testing caught two integration issues before publication: UM blocks conditions
that reference unavailable outputs even when another predicate is false; and
Claude Code's native schema validator rejects the Draft 2020-12 dialect header.
The final graph gates its branches on an always-available preparation decision;
the history command returns a typed empty result without starting a model and
removes only the dialect header when invoking Claude. Schema validation remains
in UM, and downstream checks still require exact candidate coverage.

At the end of this trial, the baseline contained **three reviewed entries**.
The subsequent [initial catalog review](INITIAL-REVIEW.md) records the full pass
and supersedes that initial coverage count. Watched evidence is limited to the source
fields documented in README.md; an unchanged fingerprint is not proof that every
project behavior is unchanged. The previously observed GitHub history-search gap
for entries mentioned only in PR diffs remains a limitation.

The evaluation workspace retains inventory data, input packets, model results,
transcripts, usage receipts and run outputs under
`targets/awesome-ratatui/incremental-20261110/` in the integration workspace.
