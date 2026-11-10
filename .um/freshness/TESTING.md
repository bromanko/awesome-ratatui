# Opus revision: validation results

November 9, 2026. Both production agent stages now use Opus 5.5 at medium effort.

## Changes

- Separate proposal-specific blockers from informational caveats. Caveats remain in reports and PR text; only real blockers stop a proposal before history review.
- Verify canonical identities and concrete description claims separately from relevance, using official source files and workspace members.
- Support name changes and move the renamed entry within its existing contiguous list. Preserve all other entries and section boundaries; reject duplicate names and malformed Markdown.
- Verify the changed destination even after a rename. Require per-link success evidence, use detailed Lychee output, and normalize implicit trailing slashes and local path aliases.
- Generate valid Git patches when the source has no final newline.

## Results

| Test | Result |
| --- | --- |
| Offline regression suite | 41 passed |
| Real checker fixtures | Bad spelling/formatting and excluded renamed destination held; existing local link positively verified |
| Actual seven-stage UM graph with synthetic agent results | All stages and report/ZIP exports passed |
| Live Opus end-to-end runs | 6 completed; 18 entry assessments |
| Original historical regression corrections | rootle move, Planner123 rename and Unifly description all produced checked previews |
| Fresh historical cases | Budget Tracker rename and Pyratatui description both produced supported checked previews |
| Additional relevance finding | Gitu removal suggestion supported by its explicit Ratatui-removal changelog; human scope decision still required |
| Final checked preview patches | 6 passed baseline and edited awesome-lint, typos, and Lychee checks |
| Other comparison entries | 12 keep decisions; no changes proposed |
| Live Opus history classification on synthetic records | 6/6 expected decisions; deterministic gates agreed |
| Recorded model usage equivalent | $4.2881 total, including history scenario tests |

The history scenarios cover a same-project unrelated change, an open duplicate, explicit maintainer rejection, closure without rejection, a merged correction, and incomplete collection. Duplicate, rejected, obsolete and incomplete proposals were held. The fixtures are controlled synthetic evidence, not real duplicate discoveries.

## Failures found during testing

The expanded tests caught the renamed-destination lookup and end-of-file patch bugs. The first live validation attempts also revealed that Lychee's default JSON omits per-link successes. Those attempts correctly withheld URL/description corrections despite successful aggregate check totals. Detailed output and URL normalization fixed the gap. The move, rename and description proposals were revalidated from their unchanged model assessments and collected history; no model retry was used to improve their answers. Original held results are retained alongside final validation. The later fresh cases used the fixed checker directly.

The positive real-tool fixture also caught macOS temporary-directory aliases, which are now normalized before comparing local-link results. Two initial history-test launches failed before model invocation because their run directories overlapped their input directory; retries used separate directories. No model or checker failures were silently dropped.

## What these results mean

The six patches are **historical replay previews**, not six outstanding corrections ready to submit to today's catalog. Historical snapshots were taken immediately before correction PRs 412, 455, 501, 431 and 457. Current official project sources were used. Snapshot freshness is checked against the frozen input, not current upstream. The current-catalog batch (rat-widget, ttyper and meteo-tui) returned keep for all three.

The three original corrections are regression tests used to develop the fix. The two additional historical cases were selected before observing the revised model outputs. Budget Tracker's old description remained supported, so its preview fixes the canonical name/URL without forcing the exact historical editorial change. Pyratatui's current changelog explicitly removes TachyonFX, supporting a factual description correction. Their official evidence was independently fetched and retained.

Historical history searches exclude records created or updated after each target PR's creation. This avoids supplying the target outcome but can omit legitimate earlier context updated later. Instruction-based isolation is not a hardened security boundary. These small, selected cases establish useful behavior and exercise the real validation path; they do not establish a general accuracy or false-positive rate. Passing checks establishes patch mechanics and link evidence, not correctness of a removal policy decision. Every preview still requires maintainer review.

## Reproducibility

Production tests run with `python3 -m unittest discover -s .um/freshness/tests -v`. After installing the pinned tools, `python3 .um/freshness/tests/check_tools.py` exercises real positive and negative checker paths. GitHub CI also executes the actual seven-stage UM graph with deterministic synthetic agents; it does not make paid model calls.

The evaluation workspace retains the predeclared protocol, selected revisions, runner, all 12 end-to-end agent transcripts, two history-agent transcripts, original held outputs, final validation logs, source snapshots, and final summary under `targets/awesome-ratatui/backfill-20261109-v2/`. The original Sonnet/Opus comparison remains unchanged in `backfill-20261109/`. `summary.json` records the initial runs; `final-summary.json` incorporates the three deterministic checker revalidations. Recorded costs are usage equivalents from Claude receipts, not a statement about an additional subscription charge.
