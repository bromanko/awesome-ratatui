# Initial catalog review — 2026-11-10

All **586 catalog entries** now have an initial review: 3 from the prior live trial and 583 from this pass.

**547 entries** have supported keep decisions and complete, stable source snapshots in `baseline.json`. **39 entries remain pending**; their complete findings are retained in `initial-review-findings.json`.

[Full entry-by-entry coverage](initial-review-coverage.csv)

The 39 held entries comprise 20 update suggestions, 4 removal suggestions, 2 uncertain relevance decisions, and 13 supported keeps whose snapshots could not be approved. These are not 39 confirmed catalog errors.

## Initial Opus results

| New review outcome | Count |
| --- | ---: |
| keep | 549 |
| remove | 4 |
| uncertain | 2 |
| update | 28 |

Successful batches: 30/30. The serial batch time totaled 86.6 minutes. Recorded model usage equivalent: **$28.74**. These were subscription-authenticated local runs; this figure is not an assertion of additional subscription charges.

## What was and was not approved

Independent source review resolved 8 optional wording suggestions as supported keeps. Their source fingerprints were rechecked against the original review before approval. The original Opus assessments and explicit adjudication reasons are preserved in the baseline and findings JSON.

A completed baseline means the research supported keeping the catalog claim and the watched source fingerprint was stable before and after that review. It does not prove every project behavior or promise that sources have remained unchanged since their recorded review time. The next maintenance run compares those saved fingerprints with current evidence.

All suggested edits remain advisory. This initial pass did not apply README changes, search correction history, validate correction patches, or open correction PRs. Suggested updates can include optional clarifications, not just factual errors. Inaccessible or unsupported snapshots are held even when the model found supporting evidence through another source.

## Pending findings

### xnano — update

<p>xnano is still a Python terminal framework built on Ratatui. The README says &#x27;built on ratatui&#x27;, shows the Built With Ratatui badge, and exposes all of ratatui&#x27;s widgets in xnano.widgets. The workspace crates depend on ratatui 0.30, ratatui-core and PyO3 bindings. However, the claim &#x27;built on … ratzilla&#x27; is unsupported: no mention of ratzilla appears in the root Cargo.toml, any of the 6 workspace member manifests, the pyproject files, the README, the docs index, or the v1 web docs. The legacy v1 branch&#x27;s xnano-core/Cargo.toml uses ratatui and tachyonfx, not ratzilla. Browser support is now through Pyodide/WebAssembly with an in-memory canvas. The word &#x27;declarative&#x27; described the legacy v1 (&#x27;incredibly declarative TUI framework&#x27;). The current main-branch v2 is described as &#x27;a terminal you put things on&#x27;, with imperative-style writes that stay live. The suggested wording drops the unsupported claims.</p>

Review note: supported description simplification; not patch validated. Current README and workspace explicitly identify Ratatui, and the legacy README identifies Ratatui and TachyonFX. Browser support is documented through Pyodide. The proposed wording follows those sources.

Proposed wording or identity:

<p>A terminal framework for Python built on Ratatui.</p>

- <https://raw.githubusercontent.com/hsaeed3/xnano/main/README.md>
- <https://raw.githubusercontent.com/hsaeed3/xnano/main/Cargo.toml>
- <https://raw.githubusercontent.com/hsaeed3/xnano/main/crates/xnano-terminal-runtime/Cargo.toml>

### ratatui-comfy-tabs — keep; snapshot incomplete or changed

<p>The packet snapshot was unavailable, but crates.io and GitLab were readable. ratatui-comfy-tabs 0.5.12 (GitLab comfyhome/crates/ratatui-comfy-tabs, active as of 2026-07-04) depends on ratatui-core and is described as an advanced, highly customizable tab-bar navigation widget for Ratatui. The listing&#x27;s description matches.</p>

- <https://crates.io/api/v1/crates/ratatui-comfy-tabs>
- <https://gitlab.com/comfyhome/crates/ratatui-comfy-tabs/-/raw/main/Cargo.toml>
- <https://gitlab.com/comfyhome/crates/ratatui-comfy-tabs/-/raw/main/README.md>

### ratatui-comfy-toaster — keep; snapshot incomplete or changed

<p>The packet snapshot was unavailable, but crates.io and GitLab were readable. ratatui-comfy-toaster 0.6.2 (GitLab comfyhome/crates/ratatui-comfy-toaster, active as of 2026-07-18) depends on ratatui 0.30. Its README calls it &#x27;An advanced toast notification engine for Ratatui terminal UI applications&#x27; and an enhanced fork of ratatui-toaster. The listing matches.</p>

- <https://crates.io/api/v1/crates/ratatui-comfy-toaster>
- <https://gitlab.com/comfyhome/crates/ratatui-comfy-toaster/-/raw/main/Cargo.toml>
- <https://gitlab.com/comfyhome/crates/ratatui-comfy-toaster/-/raw/main/README.md>

### tui-additions — update

<p>The project is still relevant, but &#x27;the rust tui crate&#x27; now usually means the archived tui-rs crate, which this project no longer uses. Current releases depend only on ratatui 0.30 and provide a declarative framework module and a widgets module (grid, textfield, textlist). The suggested wording describes what the crate actually provides.</p>

Review note: clarification depends on intended meaning. The phrase rust tui crate can refer generically to a Rust terminal UI crate rather than specifically to the predecessor tui-rs package. Explicitly naming Ratatui may clarify the entry without establishing that it was false.

Proposed wording or identity:

<p>A declarative framework and extra widgets for Ratatui.</p>

- <https://raw.githubusercontent.com/Siriusmart/tui-additions/master/Cargo.toml>
- <https://raw.githubusercontent.com/Siriusmart/tui-additions/master/src/lib.rs>
- <https://api.github.com/repos/Siriusmart/tui-additions/contents/src/widgets>

### tui-box-text — update

<p>The description is factually wrong. The crate does not draw text surrounded by a box. It draws large characters made from box-drawing characters (BoxChar::new(&#x27;A&#x27;)).</p>

Proposed wording or identity:

<p>Displays text using box-drawing characters.</p>

- <https://raw.githubusercontent.com/ratatui/tui-widgets/main/tui-box-text/Cargo.toml>
- <https://raw.githubusercontent.com/ratatui/tui-widgets/main/tui-box-text/README.md>

### tui-dialog — keep; snapshot incomplete or changed

<p>The packet snapshot failed because the source is on Codeberg, not GitHub. I read Codeberg directly: the crate is a single-line text-entry dialog widget for Ratatui, matching the description.</p>

- <https://crates.io/api/v1/crates/tui-dialog>
- <https://codeberg.org/kdwarn/tui-dialog/raw/branch/main/Cargo.toml>
- <https://codeberg.org/api/v1/repos/kdwarn/tui-dialog>

### tui-nodes — keep; snapshot incomplete or changed

<p>The packet snapshot failed because the source is on SourceHut. I read SourceHut directly: the crate is a node-graph visualization widget that now depends on ratatui 0.30, matching the description.</p>

- <https://crates.io/api/v1/crates/tui-nodes>
- <https://git.sr.ht/~jaxter184/tui-nodes/blob/HEAD/Cargo.toml>
- <https://git.sr.ht/~jaxter184/tui-nodes>

### opaline — update

<p>opaline is still relevant: ratatui is a default feature, and the ThemeSelector widget uses ratatui. The entry&#x27;s &#x27;20 builtin themes&#x27; is wrong, though. The current README says opaline ships 39 builtin themes. Per the guidance to avoid volatile counts, the suggested wording drops the number. All other claims are confirmed: token-based engine, gradients, discovery of user themes in ~/.config, and a ThemeSelector widget.</p>

Proposed wording or identity:

<p>Token-based theme engine for Ratatui with gradients, builtin themes, user theme discovery, and a reusable theme selector widget.</p>

- <https://raw.githubusercontent.com/hyperb1iss/opaline/main/README.md>
- <https://raw.githubusercontent.com/hyperb1iss/opaline/main/Cargo.toml>
- <https://crates.io/api/v1/crates/opaline>

### color-to-tui — keep; snapshot incomplete or changed

<p>The packet snapshot was unavailable, so this was checked directly. crates.io confirms that color-to-tui depends on ratatui and that its description matches the entry. The primary repository at git.uttarayan.me returned HTTP 502, which needs a recheck and is not evidence the project is dead. The GitHub mirror shows the crate parses hex and indexed colors into ratatui Color, with serde helpers.</p>

- <https://crates.io/api/v1/crates/color-to-tui>
- <https://docs.rs/crate/color-to-tui/latest>
- <https://github.com/uttarayan21/color-to-tui>

### ratatui-input-manager — keep; snapshot incomplete or changed

<p>The crate is live (v0.4.0). Its keymap attribute macro declares input handlers, and its crossterm, termion and termwiz features match the entry. The README does not use the phrase &#x27;Elm style&#x27;, but nothing contradicts it.</p>

- <https://crates.io/api/v1/crates/ratatui-input-manager>
- <https://raw.githubusercontent.com/garryod/ratatui-input-manager/HEAD/README.md>
- <https://docs.rs/ratatui-input-manager/latest/ratatui_input_manager/>

### gitu — remove

<p>Gitu is still a Magit-inspired terminal Git client, but official sources show it no longer uses Ratatui. The 0.44.0 changelog (2026-10-28) says &#x27;Remove Ratatui dep. Rendering is now simpler, no double-buffering and diffing.&#x27; The current master Cargo.toml and Cargo.lock contain no ratatui or tui crate. Rendering now goes through a custom crossterm backend in src/term.rs. Earlier releases (e.g. v0.43.0) did use Ratatui. This is affirmative evidence that the listed implementation no longer uses Ratatui, so I recommend removal for maintainer review.</p>

- <https://raw.githubusercontent.com/altsem/gitu/master/CHANGELOG.md>
- <https://raw.githubusercontent.com/altsem/gitu/master/Cargo.toml>
- <https://raw.githubusercontent.com/altsem/gitu/v0.43.0/Cargo.toml>

### OpenBitFun — update

<p>https://github.com/GCWing/OpenBitFun redirects to https://github.com/openBitFun/OpenBitFun, and the packet snapshot also names openBitFun/OpenBitFun. It is still relevant: the workspace CLI app (`openbitfun`) has an interactive TUI built with Ratatui. The name and description are still accurate. Only the URL should change.</p>

Proposed wording or identity:

<p>https://github.com/openBitFun/OpenBitFun</p>

- <https://github.com/GCWing/OpenBitFun>
- <https://raw.githubusercontent.com/openBitFun/OpenBitFun/main/src/apps/cli/Cargo.toml>
- <https://raw.githubusercontent.com/openBitFun/OpenBitFun/main/src/apps/cli/README.md>

### Forge — remove

<p>Forge&#x27;s default branch has dropped its Ratatui TUI and is now a Tauri desktop app. Commit 3b1ce51 (2026-11-10) is titled &quot;refactor: drop the TUI; the workspace builds the desktop app&quot;. On main, the workspace has no forge-tui member and no ratatui dependency, and crates/forge-tui/Cargo.toml returns 404. The README now says &quot;Run, supervise, and resume AI coding work across your projects in one desktop app&quot;, and the `forge` CLI only opens that app or runs one headless benchmark prompt. Tags v0.1.0-beta.1 through beta.11 had the Ratatui forge-tui crate. So the listed &quot;keyboard-driven terminal workspace&quot; no longer describes the project at the listed URL.</p>

Review note: hold removal for maintainer judgment. The default branch explicitly removed the TUI, independently confirmed by its commit and workspace manifest. However, the latest published prerelease v0.1.0-beta.11 still includes forge-tui and Ratatui. This is not an unqualified case for removal; the published version remains relevant.

- <https://github.com/NorviaLabs/forge/commit/3b1ce5155d3916c1161cd7b00e107de9e7c397e1>
- <https://raw.githubusercontent.com/NorviaLabs/forge/main/Cargo.toml>
- <https://raw.githubusercontent.com/NorviaLabs/forge/main/README.md>

### lumen — remove

<p>The listed claim, &quot;runs a ratatui app as an agent session ... live cell-grid view&quot;, no longer holds on the default branch. Up to v0.13.7, Lumen was a Rust workspace with a `lumen-ratatui` crate that streamed Ratatui buffer cells. In v0.14.0 (2026-10-04) it became a C++/Qt Wayland compositor. Current main has no Cargo.toml and no lumen-ratatui crate. The README, repo description and changelog now describe only Qt and Quickshell sessions.</p>

Review note: current implementation change confirmed; legacy policy needs review. Independent reads confirm the current Qt/Wayland product and the 0.14.0 compositor transition. Legacy Ratatui tags remain available, so the research supports a current-description mismatch but does not establish that legacy releases are unsupported.

- <https://raw.githubusercontent.com/blackopsrepl/lumen/main/README.md>
- <https://raw.githubusercontent.com/blackopsrepl/lumen/main/CHANGELOG.md>
- <https://raw.githubusercontent.com/blackopsrepl/lumen/v0.13.6/README.md>

### pixtuoid — update

<p>https://github.com/IvanWng97/pixtuoid redirects to https://github.com/pixtuoid/pixtuoid, which is also the repository in the packet snapshot and in the README&#x27;s own links. The project and name are unchanged and still Ratatui-based. Only the URL needs updating.</p>

Proposed wording or identity:

<p>pixtuoid
https://github.com/pixtuoid/pixtuoid
Live pixel-art office for AI coding agents.</p>

- <https://github.com/IvanWng97/pixtuoid>
- <https://raw.githubusercontent.com/pixtuoid/pixtuoid/main/crates/pixtuoid/Cargo.toml>
- <https://raw.githubusercontent.com/pixtuoid/pixtuoid/main/README.md>

### SynapsCLI — update

<p>The project is still relevant: the synaps-tui workspace member and the root package depend on ratatui 0.30. But &quot;15MB, 2ms boot&quot; contradicts the current official docs. The README says &quot;one ~32 MB binary&quot;. BENCHMARKS.md reports about 7 ms warm start to first frame and about 41 ms cold start (synaps 0.11.0, 2026-10-26). The proposed description drops these volatile numbers.</p>

Proposed wording or identity:

<p>Lightning-fast terminal-native AI agent runtime with tools, extensions, and parallel subagents.</p>

- <https://raw.githubusercontent.com/HaseebKhalid1507/SynapsCLI/main/crates/agent-tui/Cargo.toml>
- <https://raw.githubusercontent.com/HaseebKhalid1507/SynapsCLI/main/README.md>
- <https://raw.githubusercontent.com/HaseebKhalid1507/SynapsCLI/main/BENCHMARKS.md>

### dekit — uncertain

<p>mprocs was renamed to dekit, now a &#x27;Process manager for dev and prod&#x27;. The listed description is the legacy mprocs tagline, so it is outdated. Relevance is also unresolved. Ratatui no longer appears in the current src/Cargo.toml or Cargo.lock. Tags v0.8.0/v0.8.3 still listed ratatui, v0.9.0 does not, and the changelog for 0.9.0 says terminal internals were rewritten. The console UI now imports the in-house crate::term module. The only ratatui-ecosystem dependency left is tui-input 0.15 with default-features = false. There is no official statement about Ratatui, and the TUI still exists. Maintainer should decide whether tui-input alone is enough for the list before any description update.</p>

- <https://raw.githubusercontent.com/pvolok/dekit/HEAD/src/Cargo.toml>
- <https://raw.githubusercontent.com/pvolok/dekit/HEAD/Cargo.lock>
- <https://raw.githubusercontent.com/pvolok/dekit/HEAD/src/console/ui_tasks.rs>

### adsb_deku/radar — update

<p>Listed URL github.com/wcampbell0x2a/adsb_deku returns 301 to github.com/rsadsb/adsb_deku, and the GitHub API reports the canonical full_name as rsadsb/adsb_deku. The radar TUI still exists and still uses ratatui, and the description is accurate. Only the URL needs updating; keep the #radar-tui anchor, which still matches the README heading &quot;radar tui&quot;.</p>

Proposed wording or identity:

<p>https://github.com/rsadsb/adsb_deku#radar-tui</p>

- <https://github.com/wcampbell0x2a/adsb_deku>
- <https://github.com/rsadsb/adsb_deku/blob/master/apps/Cargo.toml>
- <https://github.com/rsadsb/adsb_deku/blob/master/README.md>

### JocalSend — keep; snapshot incomplete or changed

<p>Forgejo repo is live; the crate jocalsend is a Ratatui TUI implementing the LocalSend protocol. Description is accurate.</p>

- <https://git.kittencollective.com/nebkor/joecalsend/raw/branch/main/Cargo.toml>
- <https://git.kittencollective.com/nebkor/joecalsend>

### orbit-tui — update

<p>ziuus/orbit-tui is still relevant: it is a Ratatui keyboard-driven terminal dashboard. The description&#x27;s volatile numbers are not supported by the current README. I found no ~3MB binary claim anywhere in the README. The README gives idle CPU as &quot;roughly 0.5% of a core at idle&quot; and says &quot;four modes&quot;, while the GitHub description says &quot;six modes&quot;. The project also now covers a WASM plugin system and workspace/agent pages. The suggested wording keeps the supported features and drops the numbers, as the guidelines prefer.</p>

Proposed wording or identity:

<p>Keyboard-driven terminal system dashboard with CPU, memory, disk, network, GPU and process monitoring, an audio visualizer, and WASM plugins.</p>

- <https://raw.githubusercontent.com/ziuus/orbit-tui/main/Cargo.toml>
- <https://raw.githubusercontent.com/ziuus/orbit-tui/main/README.md>
- <https://github.com/ziuus/orbit-tui>

### kftui — update

<p>The tool is still relevant: kftui (crates/kftui) uses Ratatui and manages Kubernetes port-forwards, including UDP and forwarding through a cluster proxy. However, the listed anchor README.md#kftui is stale. The root README no longer has a &#x27;kftui&#x27; heading (current headings: About, Features, Get started, Contributing, License, …), so the link goes to the top of the README. The kftui crate has its own README in the monorepo, and that directory URL returns 200. The description is still accurate.</p>

Proposed wording or identity:

<p>https://github.com/hcavarsan/kftray/tree/main/crates/kftui</p>

- <https://raw.githubusercontent.com/hcavarsan/kftray/main/README.md>
- <https://github.com/hcavarsan/kftray/tree/main/crates/kftui>
- <https://raw.githubusercontent.com/hcavarsan/kftray/main/crates/kftui/Cargo.toml>

### dfdisk — update

<p>dfdisk is still a Ratatui forensic imaging tool, and &#x27;forensic disk imaging&#x27; and &#x27;damaged media rescue&#x27; (via GNU ddrescue) are documented. &#x27;Evidence management&#x27; is not documented as a capability. The tool records required case number, evidence number, and examiner metadata in acquisition reports, but it does not manage evidence. The official manifest description now says &#x27;…damaged media rescue and conversion CLI/TUI tool&#x27;, and the README documents image verification and RAW↔E01 conversion. A durable rewording follows the project&#x27;s own manifest.</p>

Proposed wording or identity:

<p>Forensic disk imaging, damaged media rescue, verification and image conversion.</p>

- <https://raw.githubusercontent.com/tylerstyle/dfdisk/main/Cargo.toml>
- <https://raw.githubusercontent.com/tylerstyle/dfdisk/main/README.md>

### pacman-utils — update

<p>The project is now branded &quot;archman&quot;: that is the README title, the Cargo package name and the logo. The repository slug is still pacman-utils, and https://github.com/ankur3-101106/pacman-utils returns 200 with no redirect, so the URL stays the same. The description is still accurate: it is a keyboard-driven Ratatui Arch system manager running pacman, AUR helpers (yay/paru) and reflector. Suggest renaming the entry to archman.</p>

Proposed wording or identity:

<p>archman
https://github.com/ankur3-101106/pacman-utils</p>

- <https://raw.githubusercontent.com/ankur3-101106/pacman-utils/main/Cargo.toml>
- <https://raw.githubusercontent.com/ankur3-101106/pacman-utils/main/README.md>
- <https://github.com/ankur3-101106/pacman-utils>

### pgtui — keep; snapshot incomplete or changed

<p>A Ratatui PostgreSQL TUI client that opens your terminal editor for inserts and updates.</p>

- <https://codeberg.org/kdwarn/pgtui/raw/branch/main/Cargo.toml>
- <https://codeberg.org/kdwarn/pgtui/raw/branch/main/README.md>

### pumas — uncertain

<p>The latest published release (0.5.0, on crates.io and tagged v0.5.0) depends on Ratatui with termion. The default branch `main` no longer lists ratatui and instead uses iocraft (0.9), a different, non-Ratatui TUI library. The project is still a terminal power-usage monitor for Apple Silicon, and the description stays accurate. Unresolved: whether the next release will ship without Ratatui. Until then, the currently installable version is Ratatui-based.</p>

- <https://raw.githubusercontent.com/graelo/pumas/main/Cargo.toml>
- <https://raw.githubusercontent.com/graelo/pumas/v0.5.0/Cargo.toml>
- <https://crates.io/api/v1/crates/pumas/0.5.0/dependencies>

### passepartui — update

<p>Project is a ratatui TUI for pass and remains relevant, but README explicitly says no password-store manipulation (adding/deleting) is implemented; it supports navigation, search/filter, and viewing/copying passwords and OTPs. &quot;Managing&quot; overstates this; a neutral wording matching the upstream tagline is more accurate.</p>

Review note: optional precision may be preferable to a factual correction. Managing passwords can include browsing and copying. The reported lack of add/delete operations supports narrower wording but does not unambiguously falsify the existing description.

Proposed wording or identity:

<p>A TUI for browsing and copying passwords from the pass password store.</p>

- <https://raw.githubusercontent.com/kardwen/passepartui/main/README.md>
- <https://raw.githubusercontent.com/kardwen/passepartui/main/Cargo.toml>

### sc-cli — update

<p>lnds/sc-cli remains a ratatui CLI+TUI client for Shortcut stories, but the entry has a spelling error (&quot;formerly know as&quot; → &quot;known&quot;) and missing punctuation; contribution rules require checking spelling/grammar. Clubhouse→Shortcut rename is real but README doesn&#x27;t mention it; the parenthetical is retained.</p>

Proposed wording or identity:

<p>A TUI for Shortcut (formerly known as Clubhouse), a project management tool for teams.</p>

- <https://raw.githubusercontent.com/lnds/sc-cli/main/Cargo.toml>
- <https://raw.githubusercontent.com/lnds/sc-cli/main/README.md>

### taskfinder — keep; snapshot incomplete or changed

<p>Packet snapshot was unavailable, but crates.io metadata was read directly: taskfinder 2.19.0 is a ratatui TUI extracting tasks from plain text files with editor hook, matching the entry; crates.io link is consistent with contribution guidance.</p>

- <https://crates.io/api/v1/crates/taskfinder>
- <https://crates.io/api/v1/crates/taskfinder/2.19.0/dependencies>

### glues — update

<p>Glues is still a relevant ratatui note-taking TUI, but the entry&#x27;s &#x27;Git, CSV, and JSON support&#x27; is out of date. The README up to v0.7.0 listed a &#x27;CSV or JSON&#x27; storage option. From v0.8.0 the README instead documents Instant, Local (file-per-note), redb, Git, MongoDB and Proxy backends, and no longer mentions CSV or JSON. The TUI still enables GlueSQL CsvStorage, but only for its own configuration (tui/src/config.rs). The suggested wording drops the unsupported CSV/JSON claim and avoids listing volatile backends.</p>

Proposed wording or identity:

<p>A Vim-inspired, privacy-first TUI note-taking app with Git sync and multiple storage backends.</p>

- <https://raw.githubusercontent.com/gluesql/glues/main/tui/Cargo.toml>
- <https://raw.githubusercontent.com/gluesql/glues/main/README.md>
- <https://raw.githubusercontent.com/gluesql/glues/v0.7.0/README.md>

### isw — keep; snapshot incomplete or changed

<p>GitLab project resolves at its canonical path and uses Ratatui. The README describes a TUI stopwatch with intervals and gives a pomodoro example, which matches the entry.</p>

- <https://gitlab.com/api/v4/projects/thom-cameron%2Fisw>
- <https://gitlab.com/thom-cameron/isw/-/raw/main/Cargo.toml>
- <https://gitlab.com/thom-cameron/isw/-/raw/main/readme.md>

### leetrs — update

<p>Relevant: canonical repo shadowmkj/leetrs ships a Ratatui TUI, and the identity is correct. The entry&#x27;s wording is inaccurate, though. It calls leetrs &#x27;A TUI for browsing, testing, and submitting&#x27;, but the official docs limit the TUI to searching, filtering and picking problems. Testing and submitting are separate CLI subcommands (&#x27;leetrs test&#x27; and &#x27;leetrs submit&#x27;) that act on solution files edited in Neovim. Suggested rewording describes it as a CLI and TUI.</p>

Proposed wording or identity:

<p>A CLI and TUI for browsing, testing, and submitting LeetCode problems from your terminal.</p>

- <https://github.com/shadowmkj/leetrs>
- <https://raw.githubusercontent.com/shadowmkj/leetrs/main/Cargo.toml>
- <https://raw.githubusercontent.com/shadowmkj/leetrs/main/README.md>

### angry-duiker — keep; snapshot incomplete or changed

<p>angry-duiker is a Ratatui TUI music player that streams from DLNA media servers. This matches the listed description.</p>

- <https://gitlab.com/api/v4/projects/fizzizist%2Fangry-duiker-2>
- <https://gitlab.com/fizzizist/angry-duiker-2/-/raw/master/Cargo.toml>
- <https://gitlab.com/fizzizist/angry-duiker-2/-/raw/master/README.md>

### chordflow — remove

<p>The official repository removed ChordFlow&#x27;s Ratatui TUI. It is now only a Dioxus desktop GUI. The chordflow_tui crate (ratatui 0.29) was dropped from the workspace members by tag v0.4.0. Commit a2a43b68 (&#x27;migrating to cpal&#x27;, 2026-01-02) then deleted its source. Every tag from v0.4.0 to v0.7.0 lists only chordflow_desktop and chordflow_music_theory, and the README calls it &#x27;a desktop app&#x27; using the Dioxus CLI. The guitar-practice description is still accurate, but the listed implementation no longer has a Ratatui/TUI interface.</p>

- <https://raw.githubusercontent.com/timvancann/chordflow/main/Cargo.toml>
- <https://github.com/timvancann/chordflow/commit/a2a43b68>
- <https://raw.githubusercontent.com/timvancann/chordflow/94d35a81/chordflow_tui/Cargo.toml>

### gtm — update

<p>The listed URL github.com/prjctimg/gtm returns HTTP 301 to github.com/craftty-org/gtm. The API reports the canonical name as craftty-org/gtm (an organization, not a fork), and the workspace manifest declares that URL as its repository. The project is still a Ratatui terminal audio player, the name is unchanged and the description is accurate, so only the URL needs updating.</p>

Proposed wording or identity:

<p>https://github.com/craftty-org/gtm</p>

- <https://github.com/prjctimg/gtm>
- <https://raw.githubusercontent.com/craftty-org/gtm/dev/Cargo.toml>
- <https://raw.githubusercontent.com/craftty-org/gtm/dev/gtm/Cargo.toml>

### rs-pug — update

<p>Relevant: it depends on ratatui 0.30 and is a terminal music player built on mpv and yt-dlp. However, the entry&#x27;s lead claim, &quot;Neovim-inspired&quot;, has no support in the current README, docs-usage.md or GitHub description. Grepping them for vim/neovim finds nothing. The current docs present it as a terminal player that streams from YouTube, SoundCloud and Sonum, plays local files, has a real-time FFT spectrum visualizer and is extensible with Lua plugins. &quot;Asynchronous&quot; (it uses tokio) and &quot;reactive audio visualizer&quot; are still supported. The suggested wording drops the unsupported claim and names the documented core features.</p>

Review note: hold wording change for judgment. The reported absence of Neovim inspiration from current documentation does not by itself disprove historical inspiration. The proposed feature description may be useful, but this is not a confirmed false claim.

Proposed wording or identity:

<p>A terminal music player for YouTube, SoundCloud and local files, with Lua plugins and a real-time audio visualizer.</p>

- <https://raw.githubusercontent.com/JustRoccat/rs-pug/main/Cargo.toml>
- <https://github.com/JustRoccat/rs-pug>
- <https://raw.githubusercontent.com/JustRoccat/rs-pug/main/docs-usage.md>

### enimtui — keep; snapshot incomplete or changed

<p>A Codeberg ratatui minesweeper game; the README matches the description.</p>

- <https://codeberg.org/tranzystorekk/enimtui/raw/branch/main/Cargo.toml>
- <https://codeberg.org/tranzystorekk/enimtui>

### mlbt — update

<p>The project is still a ratatui TUI with Gameday, scores, standings and stats. However, it uses MLB&#x27;s Stats API (statsapi.mlb.com), not a &#x27;Statcast API&#x27;. The README and the GitHub description both say &#x27;MLB Stats API&#x27;, so the API name in the entry is factually wrong.</p>

Proposed wording or identity:

<p>A TUI for the MLB Stats API. Watch a live game using Gameday, or check scores, standings, and stats.</p>

- <https://raw.githubusercontent.com/mlb-rs/mlbt/main/Cargo.toml>
- <https://github.com/mlb-rs/mlbt/blob/main/README.md>
- <https://raw.githubusercontent.com/mlb-rs/mlbt/main/api/src/client.rs>

### ssHattrick — update

<p>Still a ratatui multiplayer game played over SSH, but it is a hockey game, not a &#x27;Hattrick football-management game&#x27;. The crate manifests describe it as &#x27;Hockey in your terminal over SSH&#x27;. The README&#x27;s &#x27;Hattrick&#x27; link goes to the Atari 7800 game Hat Trick (a hockey game), not the online football manager hattrick.org.</p>

Review note: game-description mismatch independently confirmed. The current official package manifest explicitly describes hockey over SSH and depends on Ratatui. The catalog calls it a football-management game, so that description should be corrected.

Proposed wording or identity:

<p>A multiplayer terminal hockey game inspired by the Atari 7800 Hat Trick, playable over SSH.</p>

- <https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick/Cargo.toml>
- <https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick-core/Cargo.toml>
- <https://github.com/ricott1/sshattrick/blob/main/README.md>

### Thardians — keep; snapshot incomplete or changed

<p>GitLab project thustle/thardians-rs is a Space Invaders game built with Ratatui; description accurate.</p>

- <https://gitlab.com/api/v4/projects/thustle%2Fthardians-rs>
- <https://gitlab.com/thustle/thardians-rs/-/raw/master/Cargo.toml>

## Optional suggestions resolved as keep

- **ratatui-image**: Independent README and manifest review confirms Sixel and Unicode half-block rendering. The existing statement does not claim those are the only protocols. Adding Kitty and iTerm2 is optional.
- **tui-cards**: Independent README and manifest review confirms a Ratatui playing-card widget. Playing cards satisfy the existing generic claim about displaying cards; naming them more precisely is optional.
- **rainfrog**: Independent README review confirms Postgres as a tier-one supported database; the manifest confirms Ratatui. The current entry does not claim Postgres is its only database.
- **binsider**: Independent README and manifest review confirms a Ratatui tool for analyzing ELF binaries. ELF files are binary files, so the existing generic claim is supported. Explicitly naming ELF is optional precision.
- **otree**: Independent README and manifest review confirms JSON, YAML and TOML input in a Ratatui tree viewer. Additional XML support does not invalidate this non-exclusive list.
- **tabiew**: Independent README and manifest review confirms CSV viewing and querying in a Ratatui app. The original claim remains true; mentioning additional tabular formats is optional.
- **fzf-make**: Independent README and manifest review confirms make-target execution with a fuzzy finder and preview window, using Ratatui. The original entry never said only make; broader runner wording is optional.
- **termscp**: Independent README and manifest review confirms the listed SCP, SFTP, FTP, S3 and SMB capabilities and the tuirealm/Ratatui implementation. The original list is not exclusive; additional protocols are an optional expansion.

## Method and limitations

The input catalog is pinned by README SHA-256 `d922da1de3161ed7e617aa7c1a111f09ea09d90073a6d3819439b18bb869ebb1`. The production workflow source was `05a5a41a4916bc47ecb3c5e867f40ed8e21f95b5`. A three-stage bootstrap adapter uses the production research prompt, Opus 5.5 at medium effort, exact entry/schema checks, and the production baseline rules. It also investigates entries whose automatic snapshots failed, without approving those snapshots. All research outputs and transcripts are retained in the evaluation workspace.

The first two batches used the original production prompt verbatim. Batches 03–17 added concise supported-keep write-ups. Batches 18–30 also clarified that additional capabilities do not invalidate a non-exclusive description. All prompt variants are retained; research requirements were not reduced. Only the three previously reviewed entries were excluded; all other entries were reviewed in catalog order.

GitHub source tracking watches the fields documented in README.md, not every source file. Some non-GitHub crate repositories are not supported by the current snapshot collector. Failure to retrieve a source is not evidence that the project is dead. Source material and model conclusions still require maintainer judgment.

A fixed 12-entry source spot-check supported ten keep recommendations and one original description that had received an optional expansion suggestion; one check was partial and remains held. This sample does not establish whole-catalog accuracy.

Selected independent checks and optional-versus-factual distinctions are recorded in `initial-review-findings.json`. This is not an exhaustive independent audit of every keep decision.

## Focused prompt regression

The clarified production prompt was tested on ten entries, without exposing expected labels to Opus: seven optional-expansion cases and three genuine-change controls. All ten matched the expected decisions: seven keeps and three updates. This is a targeted regression check, not a whole-catalog accuracy estimate.

The separate check took 94.27 seconds and used $0.7132 recorded usage equivalent. Its decisions, receipt and prompt fingerprint are retained in `initial-review-verification.json`.

## Fresh comparison after review

A new, model-free source comparison scanned all 586 entries against the completed baseline. It skipped **542 unchanged entries (92.5%)**, selected 37 for potential research (32 without approved baseline records and 5 with changed watched evidence), and held 7 fetch failures. **No models ran.**

The five source changes were `Mitos`, `Ario`, `faro`, `linutil`, `kimün`. This is an immediate repeat comparison, not a prediction of monthly costs. Entries can change while a full initial pass is in progress; their saved reviews remain dated evidence, and the next run detects the difference. Detailed routing results are retained in `initial-review-verification.json`.
