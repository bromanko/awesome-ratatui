# Advisory freshness review

This opt-in workflow investigates three catalog entries and puts an evidence-led
report in the GitHub Actions summary. It checks whether descriptions and Ratatui/TUI
relevance still hold. Existing lint, typo and daily link workflows remain useful;
this investigation addresses questions they cannot answer.

The workflow produces proposed README patches and PR text, without editing the
checkout, opening PRs, commenting, submitting reviews or merging. Suggestions
always require a maintainer. It is a manual pilot:
no recurring schedule, coverage checkpoint or automatic advancement is installed.

## Run a fork trial

1. Review and merge this integration into the fork's default branch when ready.
2. Configure the `awesome-ratatui-review` environment with required reviewers and
   an `ANTHROPIC_API_KEY` environment secret.
3. Set repository variable `UM_FRESHNESS_ENABLED=true`.
4. Manually run **UM freshness review** on the reviewed branch, supplying
   a zero-based slice number. Read the research in the Actions summary.

No fork-name restriction is imposed. The collector uses the selected checked-out
commit for README and contribution rules, then selects consecutive groups of three
entries. IDs are README line numbers within that pinned revision, not permanent
project IDs. The current 586-entry snapshot has 196 slices (0 through 195); this
flat grouping differs from the earlier experiment's 203 section-specific slices.
Catalog changes can shift slices. Keep a manual record of reviewed entries during
the trial; slice numbers alone do not establish continuing coverage.

The report rechecks upstream's current README. Changed or unavailable content is
explicitly marked. Even an unchanged catalog does not establish that project sources
haven't changed since investigation. Failures produce a summary directing the reader
to the failed step, rather than silently implying a successful audit.

## Implementation

One GitHub job prepares a commit-pinned packet, invokes the published UM run action,
and renders the structured export. Python only selects entries, checks output
consistency and renders the report. Claude owns research into official project docs,
workspace members, optional tools and legacy branches. Citations are agent-reported
observations, not independently verified facts. Uncertainty is visible in the report.

Runtime matches the reviewed awesome-testing integration: UM 0.72.1, official
Claude Code 2.1.284, Sonnet 5 at medium effort, and run-action commit
`3b5d29379bc349df8d95b29b599e71701aa1d017`. Explicit UM version selection avoids the
older action default that failed on Claude ToolSearch responses. The native installer
is used without a wrapper or custom tool restrictions. The job timeout is 30 minutes;
there is no dollar cap. Provider usage is billable once enabled.

The Anthropic key is passed to the model step. The read-only GitHub token is passed
only to the final catalog recheck; checkout does not persist credentials. Normal
agent tools are available. Instructions prohibit external changes and executing
project code; those instructions are not an execution sandbox. Enable only reviewed
workflow branches and use environment review for the trial.

## Evidence and limits

The earlier local prototype recovered a known Yardlet removal, kept selected control
projects, and held a potentially mistaken Burn removal. Its 14 tests and roughly
$0.23 experimental cost describe that older constrained implementation. They do not
validate this agent-led integration, its accuracy, or its costs. No accuracy or time
savings claim is made here.

The Burn case informs a general research rule: a framework's root README/manifest
can omit its Ratatui tools and workspace dependencies. Absence from those excerpts
is not sufficient evidence for removal. Low activity, archival, non-Rust language
and temporary access failures likewise do not establish loss of relevance.

Before scheduling, inspect real reports across ordinary controls and ambiguous
cases, measure usefulness and unsupported claims, and choose revisit latency.
Preserve unseen evaluation cases rather than tuning repeatedly to familiar outcomes.
A recurring successor needs a coverage/resume policy for failures and catalog changes.

## Validation

```sh
python3 -m unittest discover -s .um/freshness/tests -v
um workflow validate --source-root .um/freshness --json .um/freshness/workflow.yaml
actionlint .github/workflows/um-freshness.yml .github/workflows/um-freshness-checks.yml
```

Local tests, configuration validation and actual-catalog packet preparation pass.
No paid model call or GitHub-hosted run has been made for this integration. A live
fork trial remains necessary after review and explicit enablement.

## Preview proposed changes on GitHub

Open the Actions run summary to see each suggested change's PR title/body and
README diff. Download `freshness-proposals` from the run's Artifacts section for
`report.md`, one `.patch` per proposal and its corresponding PR description.
Each proposal changes one entry, following the contribution guidelines.

A changed or unverifiable catalog, or unresolved questions on a recommendation,
withholds its patch. Keep/uncertain decisions produce research only. Patches are
constructed from the exact pinned entry; no model-generated arbitrary diff is
applied. The preview does not certify factual accuracy or run the full upstream
lint/link checks. A maintainer must verify it before opening a correction PR.

The **Check UM freshness integration** PR check also renders an **Example preview**
using fictional entries and `example.com` URLs. Its summary and downloadable
`freshness-example` show the output format without secrets, model calls or external
research. This is a rendering/integration demonstration, not a live audit result.
