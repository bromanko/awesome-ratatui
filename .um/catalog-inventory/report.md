# Full catalog review inventory

**24 proposed changes · 2 uncertain entries · 13 snapshot issues**

Saved initial review of **586 entries**; **547 completed review records** retained for recurring runs.

These are research recommendations, not 24 validated patches. Prior-discussion checks and patch validation have not been completed for the full inventory. No catalog edits are applied by this report.

## Proposed changes

| Entry | Recommendation |
| --- | --- |
| [xnano](https://github.com/hsaeed3/xnano) | Update |
| [tui-additions](https://crates.io/crates/tui-additions) | Update |
| [tui-box-text](https://crates.io/crates/tui-box-text) | Update |
| [opaline](https://crates.io/crates/opaline) | Update |
| [gitu](https://github.com/altsem/gitu) | Remove |
| [OpenBitFun](https://github.com/GCWing/OpenBitFun) | Update |
| [Forge](https://github.com/NorviaLabs/forge) | Remove |
| [lumen](https://github.com/blackopsrepl/lumen) | Remove |
| [pixtuoid](https://github.com/IvanWng97/pixtuoid) | Update |
| [SynapsCLI](https://github.com/HaseebKhalid1507/SynapsCLI) | Update |
| [adsb_deku/radar](https://github.com/wcampbell0x2a/adsb_deku#radar-tui) | Update |
| [orbit-tui](https://github.com/ziuus/orbit-tui) | Update |
| [kftui](https://github.com/hcavarsan/kftray/blob/main/README.md#kftui) | Update |
| [dfdisk](https://github.com/tylerstyle/dfdisk) | Update |
| [pacman-utils](https://github.com/ankur3-101106/pacman-utils) | Update |
| [passepartui](https://github.com/kardwen/passepartui) | Update |
| [sc-cli](https://github.com/lnds/sc-cli) | Update |
| [glues](https://github.com/gluesql/glues) | Update |
| [leetrs](https://github.com/shadowmkj/leetrs) | Update |
| [chordflow](https://github.com/timvancann/chordflow) | Remove |
| [gtm](https://github.com/prjctimg/gtm) | Update |
| [rs-pug](https://github.com/JustRoccat/rs-pug) | Update |
| [mlbt](https://github.com/mlb-rs/mlbt) | Update |
| [ssHattrick](https://github.com/ricott1/sshattrick) | Update |

### xnano — update

```diff
-- [xnano](https://github.com/hsaeed3/xnano) - A declarative terminal framework for Python built on ratatui & ratzilla.
+- [xnano](https://github.com/hsaeed3/xnano) - A terminal framework for Python built on Ratatui.
```

xnano is still a Python terminal framework built on Ratatui. The README says 'built on ratatui', shows the Built With Ratatui badge, and exposes all of ratatui's widgets in xnano.widgets. The workspace crates depend on ratatui 0.30, ratatui-core and PyO3 bindings. However, the claim 'built on … ratzilla' is unsupported: no mention of ratzilla appears in the root Cargo.toml, any of the 6 workspace member manifests, the pyproject files, the README, the docs index, or the v1 web docs. The legacy v1 branch's xnano-core/Cargo.toml uses ratatui and tachyonfx, not ratzilla. Browser support is now through Pyodide/WebAssembly with an in-memory canvas. The word 'declarative' described the legacy v1 ('incredibly declarative TUI framework'). The current main-branch v2 is described as 'a terminal you put things on', with imperative-style writes that stay live. The suggested wording drops the unsupported claims.

<details>
<summary>Evidence and limitations</summary>

- 'An extremely nano terminal experience for Python, built on ratatui.' Layout and drawing run in Rust on ratatui. All of ratatui's widgets are in xnano.widgets. WebAssembly is supported via Pyodide. No mention of ratzilla. [Source](https://raw.githubusercontent.com/hsaeed3/xnano/main/README.md)
- Workspace members are xnano-terminal-cells/state/runtime/core/audio/image. Workspace dependencies include ratatui 0.30 and ratatui-core 0.1. No ratzilla. [Source](https://raw.githubusercontent.com/hsaeed3/xnano/main/Cargo.toml)
- The xnano terminal runtime depends on ratatui, ratatui-core and termprofile[ratatui]. No ratzilla, and none in the other member manifests checked. [Source](https://raw.githubusercontent.com/hsaeed3/xnano/main/crates/xnano-terminal-runtime/Cargo.toml)
- Says v1 is no longer part of the current library and main is completely v2. v1 source lives on the v1 branch; last v1 release is 1.2.3. [Source](https://raw.githubusercontent.com/hsaeed3/xnano/main/docs/v1/index.md)
- v1: 'A simple python tui framework built on top of ratatui and tachyonfx'; 'incredibly declarative TUI framework'. No ratzilla. [Source](https://raw.githubusercontent.com/hsaeed3/xnano/v1/README.md)
- The v1 core depends on ratatui 0.30, ratatui-core 0.1 and tachyonfx 0.25. No ratzilla. [Source](https://raw.githubusercontent.com/hsaeed3/xnano/v1/xnano-core/Cargo.toml)
- The v1 Web host runs an offscreen runtime and streams cell frames to the browser. It says there is no separate HTML paint backend and does not mention ratzilla. [Source](https://raw.githubusercontent.com/hsaeed3/xnano/main/docs/v1/core-concepts/web.md)
- **Limitation:** Git history was not searched exhaustively. A GitHub commit search for 'ratzilla' returned 0 results, but an earlier revision may have used Ratzilla.
- **Limitation:** Did not run the software.
- **Limitation:** Did not assess the legacy v1 branch's maintenance status. It exists, and the docs point users to release 1.2.3.

</details>

### tui-additions — update

```diff
-- [tui-additions](https://crates.io/crates/tui-additions) - Additions to the rust tui crate.
+- [tui-additions](https://crates.io/crates/tui-additions) - A declarative framework and extra widgets for Ratatui.
```

The project is still relevant, but 'the rust tui crate' now usually means the archived tui-rs crate, which this project no longer uses. Current releases depend only on ratatui 0.30 and provide a declarative framework module and a widgets module (grid, textfield, textlist). The suggested wording describes what the crate actually provides.

<details>
<summary>Evidence and limitations</summary>

- 0.4.4; the framework and widgets features both pull in ratatui 0.30 (optional dep); no tui dependency. [Source](https://raw.githubusercontent.com/Siriusmart/tui-additions/master/Cargo.toml)
- Modules: widgets ('structs that impl ratatui::widget::Widget') and framework ('A declarative TUI framework'). [Source](https://raw.githubusercontent.com/Siriusmart/tui-additions/master/src/lib.rs)
- Widget sources: grid.rs, textfield.rs, textlist.rs. [Source](https://api.github.com/repos/Siriusmart/tui-additions/contents/src/widgets)
- **Limitation:** The upstream README and crate description still say 'Additions to the Rust TUI crate'; the proposed wording comes from the source modules.

</details>

### tui-box-text — update

```diff
-- [tui-box-text](https://crates.io/crates/tui-box-text) - Displays text surrounded by a box.
+- [tui-box-text](https://crates.io/crates/tui-box-text) - Displays text using box-drawing characters.
```

The description is factually wrong. The crate does not draw text surrounded by a box. It draws large characters made from box-drawing characters (BoxChar::new('A')).

<details>
<summary>Evidence and limitations</summary>

- 0.3.5; 'A Ratatui widget for displaying text using the box drawing characters'. [Source](https://raw.githubusercontent.com/ratatui/tui-widgets/main/tui-box-text/Cargo.toml)
- 'A Ratatui widget to draw delightfully boxy text with line-drawing characters'; usage renders BoxChar::new('A'). [Source](https://raw.githubusercontent.com/ratatui/tui-widgets/main/tui-box-text/README.md)

</details>

### opaline — update

```diff
-- [opaline](https://crates.io/crates/opaline) - Token-based theme engine for Ratatui with gradients, 20 builtin themes, user theme discovery, and a reusable theme selector widget.
+- [opaline](https://crates.io/crates/opaline) - Token-based theme engine for Ratatui with gradients, builtin themes, user theme discovery, and a reusable theme selector widget.
```

opaline is still relevant: ratatui is a default feature, and the ThemeSelector widget uses ratatui. The entry's '20 builtin themes' is wrong, though. The current README says opaline ships 39 builtin themes. Per the guidance to avoid volatile counts, the suggested wording drops the number. All other claims are confirmed: token-based engine, gradients, discovery of user themes in ~/.config, and a ThemeSelector widget.

<details>
<summary>Evidence and limitations</summary>

- The README states '39 builtin themes', 'Multi-Stop Gradients', 'Deep Ratatui Integration', 'ThemeSelector Widget — drop-in theme picker with live preview' and 'Theme Discovery — scan ~/.config/ for user themes'. It also lists egui, iced, crossterm, syntect and CSS adapters. [Source](https://raw.githubusercontent.com/hyperb1iss/opaline/main/README.md)
- Default features are builtin-themes, gradients and ratatui (ratatui-core). The optional 'widgets' feature depends on ratatui 0.30, and 'discovery' is an optional feature. [Source](https://raw.githubusercontent.com/hyperb1iss/opaline/main/Cargo.toml)
- The latest version is 0.4.2 (2026-09-02). The crate description is 'A token-based theme engine for Rust applications'. [Source](https://crates.io/api/v1/crates/opaline)
- **Limitation:** The theme count may change again, which is why the suggested wording leaves it out.

</details>

### gitu — remove

```diff
-- [gitu](https://github.com/altsem/gitu) - A TUI Git client inspired by Magit.
```

Gitu is still a Magit-inspired terminal Git client, but official sources show it no longer uses Ratatui. The 0.44.0 changelog (2026-10-28) says 'Remove Ratatui dep. Rendering is now simpler, no double-buffering and diffing.' The current master Cargo.toml and Cargo.lock contain no ratatui or tui crate. Rendering now goes through a custom crossterm backend in src/term.rs. Earlier releases (e.g. v0.43.0) did use Ratatui. This is affirmative evidence that the listed implementation no longer uses Ratatui, so I recommend removal for maintainer review.

<details>
<summary>Evidence and limitations</summary>

- Under [0.44.0] - 2026-10-28, Features: 'Port over config from Ratatui' and 'Remove Ratatui dep. Rendering is now simpler, no double-buffering and diffing.' [Source](https://raw.githubusercontent.com/altsem/gitu/master/CHANGELOG.md)
- gitu 0.44.0 [dependencies] list crossterm 0.28.1 but no ratatui. Dev-dependencies don't include it either. The downloaded master Cargo.lock has no ratatui or tui package. [Source](https://raw.githubusercontent.com/altsem/gitu/master/Cargo.toml)
- The previous release, v0.43.0, depended on ratatui 0.29.0 (serde feature). It was a Ratatui project until 0.43.x. [Source](https://raw.githubusercontent.com/altsem/gitu/v0.43.0/Cargo.toml)
- Defines TermBackend::Crossterm, which uses crossterm commands directly (Print, SetColors, MoveTo). No Ratatui Terminal or Backend is used. [Source](https://github.com/altsem/gitu/blob/master/src/term.rs)
- **Limitation:** The README still describes 'A terminal user interface for Git. Inspired by Magit', so the description itself remains accurate. Only the Ratatui relevance has changed.
- **Limitation:** Versions up to 0.43.x used Ratatui. Whether the list keeps projects that formerly used Ratatui is a maintainer policy choice.
- **Limitation:** Only the source and changelog were inspected. The software was not run.

</details>

### OpenBitFun — update

```diff
-- [OpenBitFun](https://github.com/GCWing/OpenBitFun) - An open-source desktop workspace for general-purpose AI agents.
+- [OpenBitFun](https://github.com/openBitFun/OpenBitFun) - An open-source desktop workspace for general-purpose AI agents.
```

https://github.com/GCWing/OpenBitFun redirects to https://github.com/openBitFun/OpenBitFun, and the packet snapshot also names openBitFun/OpenBitFun. It is still relevant: the workspace CLI app (`openbitfun`) has an interactive TUI built with Ratatui. The name and description are still accurate. Only the URL should change.

<details>
<summary>Evidence and limitations</summary>

- An HTTP request follows one redirect to https://github.com/openBitFun/OpenBitFun, which returns 200. [Source](https://github.com/GCWing/OpenBitFun)
- The CLI member crate depends on ratatui through the workspace. The root Cargo.toml pins ratatui 0.29. [Source](https://raw.githubusercontent.com/openBitFun/OpenBitFun/main/src/apps/cli/Cargo.toml)
- "OpenBitFun CLI provides an interactive terminal UI". Running `openbitfun` opens the interactive TUI. [Source](https://raw.githubusercontent.com/openBitFun/OpenBitFun/main/src/apps/cli/README.md)
- Describes OpenBitFun as an open-source agent workspace with a desktop app. The desktop app and the CLI share core execution capabilities. [Source](https://raw.githubusercontent.com/openBitFun/OpenBitFun/main/README.md)
- **Limitation:** The README still links to GCWing/OpenBitFun for mobile releases. Those links work through the redirect.

</details>

### Forge — remove

```diff
-- [Forge](https://github.com/NorviaLabs/forge) - An AI coding agent that unifies an agent, code editor, and shell in a single keyboard-driven terminal workspace.
```

Forge's default branch has dropped its Ratatui TUI and is now a Tauri desktop app. Commit 3b1ce51 (2026-11-10) is titled "refactor: drop the TUI; the workspace builds the desktop app". On main, the workspace has no forge-tui member and no ratatui dependency, and crates/forge-tui/Cargo.toml returns 404. The README now says "Run, supervise, and resume AI coding work across your projects in one desktop app", and the `forge` CLI only opens that app or runs one headless benchmark prompt. Tags v0.1.0-beta.1 through beta.11 had the Ratatui forge-tui crate. So the listed "keyboard-driven terminal workspace" no longer describes the project at the listed URL.

<details>
<summary>Evidence and limitations</summary>

- Commit titled "refactor: drop the TUI; the workspace builds the desktop app", dated 2026-11-10, the latest commit touching crates/forge-tui. [Source](https://github.com/NorviaLabs/forge/commit/3b1ce5155d3916c1161cd7b00e107de9e7c397e1)
- Workspace members on main have no forge-tui. A comment calls the Tauri app forge-desktop "the product". There is no ratatui or crossterm dependency. No member crate's Cargo.toml mentions ratatui; forge-connect's mentions "TUI" only in a comment. [Source](https://raw.githubusercontent.com/NorviaLabs/forge/main/Cargo.toml)
- "Forge is an open-source desktop coding environment". `forge` opens the desktop app. The crate list names forge-desktop (Tauri) and no TUI crate. [Source](https://raw.githubusercontent.com/NorviaLabs/forge/main/README.md)
- The latest release tag still lists the crates/forge-tui member and ratatui =0.30.2. [Source](https://raw.githubusercontent.com/NorviaLabs/forge/v0.1.0-beta.11/Cargo.toml)
- The desktop UI uses Svelte, Tauri and xterm.js, not Ratatui. [Source](https://raw.githubusercontent.com/NorviaLabs/forge/main/crates/forge-desktop/ui/package.json)
- **Limitation:** The latest published release, v0.1.0-beta.11, still ships the Ratatui TUI. The removal is on main, landed on review day, and has not been released yet.
- **Limitation:** The repository has no changelog file to confirm whether the TUI will stay supported in released versions.

</details>

### lumen — remove

```diff
-- [lumen](https://github.com/blackopsrepl/lumen) - Runs a ratatui app as an agent session and gives a human a live cell-grid view of it.
```

The listed claim, "runs a ratatui app as an agent session ... live cell-grid view", no longer holds on the default branch. Up to v0.13.7, Lumen was a Rust workspace with a `lumen-ratatui` crate that streamed Ratatui buffer cells. In v0.14.0 (2026-10-04) it became a C++/Qt Wayland compositor. Current main has no Cargo.toml and no lumen-ratatui crate. The README, repo description and changelog now describe only Qt and Quickshell sessions.

<details>
<summary>Evidence and limitations</summary>

- "Lumen hosts Qt applications for agents ... It is the compositor: every session is a nested Wayland client". No mention of ratatui, terminal sessions or cell grids. [Source](https://raw.githubusercontent.com/blackopsrepl/lumen/main/README.md)
- 0.14.0 (2026-10-04): "compositor: C++ Wayland compositor with windowless output". 0.15.0 adds Quickshell panels. No later entry restores terminal or Ratatui sessions. [Source](https://raw.githubusercontent.com/blackopsrepl/lumen/main/CHANGELOG.md)
- The legacy README documents "Ratatui sessions run a Lumen-native app" that links the `lumen-ratatui` crate, with ratatui's buffer diff as the transport. This is the behaviour the catalog entry describes. [Source](https://raw.githubusercontent.com/blackopsrepl/lumen/v0.13.6/README.md)
- Exists at tag v0.13.7 (HTTP 200). The same path and the root Cargo.toml return 404 on main, where CMakeLists.txt exists instead. [Source](https://raw.githubusercontent.com/blackopsrepl/lumen/v0.13.7/crates/lumen-ratatui/Cargo.toml)
- Resolves without redirect. Repo description: "Single-binary session service: Qt and Quickshell sessions for agents with a live, controllable annotation loop for humans". [Source](https://github.com/blackopsrepl/lumen)
- **Limitation:** The changelog does not state in so many words that Ratatui support was dropped. The conclusion comes from the rewrite, the missing manifests and the Qt-only docs on main.
- **Limitation:** Tags v0.13.x still contain the Ratatui implementation. Their maintenance status is unknown, and the feat/docker-runtime branch README describes Chromium sessions, not Ratatui. Neither is a documented current offering.

</details>

### pixtuoid — update

```diff
-- [pixtuoid](https://github.com/IvanWng97/pixtuoid) - Live pixel-art office for AI coding agents.
+- [pixtuoid](https://github.com/pixtuoid/pixtuoid) - Live pixel-art office for AI coding agents.
```

https://github.com/IvanWng97/pixtuoid redirects to https://github.com/pixtuoid/pixtuoid, which is also the repository in the packet snapshot and in the README's own links. The project and name are unchanged and still Ratatui-based. Only the URL needs updating.

<details>
<summary>Evidence and limitations</summary>

- HTTP redirect resolves to https://github.com/pixtuoid/pixtuoid (200). [Source](https://github.com/IvanWng97/pixtuoid)
- The binary crate pixtuoid uses ratatui from the workspace. The root workspace pins ratatui 0.30. [Source](https://raw.githubusercontent.com/pixtuoid/pixtuoid/main/crates/pixtuoid/Cargo.toml)
- "Your AI coding agents, visualized as pixel-art coworkers in a terminal office." Badges and links all point to pixtuoid/pixtuoid. [Source](https://raw.githubusercontent.com/pixtuoid/pixtuoid/main/README.md)

</details>

### SynapsCLI — update

```diff
-- [SynapsCLI](https://github.com/HaseebKhalid1507/SynapsCLI) - Lightning fast terminal native agent harness with tools, extensions and subagents. 15MB, 2ms boot.
+- [SynapsCLI](https://github.com/HaseebKhalid1507/SynapsCLI) - Lightning-fast terminal-native AI agent runtime with tools, extensions, and parallel subagents.
```

The project is still relevant: the synaps-tui workspace member and the root package depend on ratatui 0.30. But "15MB, 2ms boot" contradicts the current official docs. The README says "one ~32 MB binary". BENCHMARKS.md reports about 7 ms warm start to first frame and about 41 ms cold start (synaps 0.11.0, 2026-10-26). The proposed description drops these volatile numbers.

<details>
<summary>Evidence and limitations</summary>

- synaps-tui: "Terminal UI layer — ratatui, crossterm, syntect, tachyonfx"; ratatui = "0.30". [Source](https://raw.githubusercontent.com/HaseebKhalid1507/SynapsCLI/main/crates/agent-tui/Cargo.toml)
- "Run a crew of AI agents in your terminal, on any model, from one ~32 MB binary." Lists named parallel subagents, extensions in any language, MCP, and built-in tools. There is no 15 MB or 2 ms claim. [Source](https://raw.githubusercontent.com/HaseebKhalid1507/SynapsCLI/main/README.md)
- "Warm start ~7 ms to first frame (attach to the running daemon)"; "Cold start ~41 ms". [Source](https://raw.githubusercontent.com/HaseebKhalid1507/SynapsCLI/main/BENCHMARKS.md)
- **Limitation:** Did not run the software. The numbers come from the project's own benchmarks on one machine.

</details>

### adsb_deku/radar — update

```diff
-- [adsb_deku/radar](https://github.com/wcampbell0x2a/adsb_deku#radar-tui) - A terminal radar for displaying aircraft positions from Automatic Dependent Surveillance–Broadcast (ADS-B) data.
+- [adsb_deku/radar](https://github.com/rsadsb/adsb_deku#radar-tui) - A terminal radar for displaying aircraft positions from Automatic Dependent Surveillance–Broadcast (ADS-B) data.
```

Listed URL github.com/wcampbell0x2a/adsb_deku returns 301 to github.com/rsadsb/adsb_deku, and the GitHub API reports the canonical full_name as rsadsb/adsb_deku. The radar TUI still exists and still uses ratatui, and the description is accurate. Only the URL needs updating; keep the #radar-tui anchor, which still matches the README heading "radar tui".

<details>
<summary>Evidence and limitations</summary>

- HTTP 301 → https://github.com/rsadsb/adsb_deku; API full_name rsadsb/adsb_deku, not archived, default branch master. [Source](https://github.com/wcampbell0x2a/adsb_deku)
- Workspace member rsadsb_apps 0.8.0 defines the `radar` binary and depends on ratatui 0.28.1 and crossterm 0.27. [Source](https://github.com/rsadsb/adsb_deku/blob/master/apps/Cargo.toml)
- "#### radar tui" section: ADS-B client for the terminal that plots aircraft positions; "uses ratatui for generating the display". [Source](https://github.com/rsadsb/adsb_deku/blob/master/README.md)

</details>

### orbit-tui — update

```diff
-- [orbit-tui](https://github.com/ziuus/orbit-tui) - Keyboard-driven terminal system dashboard (~3MB, 0.5% CPU) with CPU, memory, disk, network, GPU, processes, and audio visualizer.
+- [orbit-tui](https://github.com/ziuus/orbit-tui) - Keyboard-driven terminal system dashboard with CPU, memory, disk, network, GPU and process monitoring, an audio visualizer, and WASM plugins.
```

ziuus/orbit-tui is still relevant: it is a Ratatui keyboard-driven terminal dashboard. The description's volatile numbers are not supported by the current README. I found no ~3MB binary claim anywhere in the README. The README gives idle CPU as "roughly 0.5% of a core at idle" and says "four modes", while the GitHub description says "six modes". The project also now covers a WASM plugin system and workspace/agent pages. The suggested wording keeps the supported features and drops the numbers, as the guidelines prefer.

<details>
<summary>Evidence and limitations</summary>

- The package is orbit-tui 0.11.17 (binary orbit). It depends on ratatui 0.29, ratatui-image and crossterm. [Source](https://raw.githubusercontent.com/ziuus/orbit-tui/main/Cargo.toml)
- The README calls Orbit a "terminal OS and developer dashboard ... one pane, four modes". It says "roughly 0.5% of a core at idle". It documents a Monitor page (processes with filter, sort, tree and kill), GPU support (NVIDIA, AMD, Intel), an audio visualizer using cava, and WASM plugins. No 3MB size claim appears. [Source](https://raw.githubusercontent.com/ziuus/orbit-tui/main/README.md)
- The GitHub API description reads "One pane, six modes ... ~3MB binary, 0.5% CPU", which conflicts with the README's "four modes". [Source](https://github.com/ziuus/orbit-tui)
- **Limitation:** I did not measure binary size or CPU use.

</details>

### kftui — update

```diff
-- [kftui](https://github.com/hcavarsan/kftray/blob/main/README.md#kftui) - A TUI to manage multiple kubectl port-forward commands, with support for UDP and Kubernetes proxy.
+- [kftui](https://github.com/hcavarsan/kftray/tree/main/crates/kftui) - A TUI to manage multiple kubectl port-forward commands, with support for UDP and Kubernetes proxy.
```

The tool is still relevant: kftui (crates/kftui) uses Ratatui and manages Kubernetes port-forwards, including UDP and forwarding through a cluster proxy. However, the listed anchor README.md#kftui is stale. The root README no longer has a 'kftui' heading (current headings: About, Features, Get started, Contributing, License, …), so the link goes to the top of the README. The kftui crate has its own README in the monorepo, and that directory URL returns 200. The description is still accurate.

<details>
<summary>Evidence and limitations</summary>

- The root README has no '#kftui' section. It says 'kftray and kftui manage Kubernetes port forwards' and lists 'Forward TCP and UDP traffic to services or pods, or reach other hosts through a cluster proxy.' [Source](https://raw.githubusercontent.com/hcavarsan/kftray/main/README.md)
- Returns HTTP 200. crates/kftui/README.md opens with '# kftui — kftui manages Kubernetes port forwards from the terminal.' [Source](https://github.com/hcavarsan/kftray/tree/main/crates/kftui)
- The package kftui uses workspace ratatui (0.30.2 at the root), crossterm, ratatui-explorer, and tui-logger. [Source](https://raw.githubusercontent.com/hcavarsan/kftray/main/crates/kftui/Cargo.toml)
- **Limitation:** Other valid destinations are https://crates.io/crates/kftui or https://kftray.app/docs/interfaces/terminal. The contribution guide suggests crates.io links for libraries, but kftui is an application.

</details>

### dfdisk — update

```diff
-- [dfdisk](https://github.com/tylerstyle/dfdisk) - Modern forensic disk imaging, damaged media rescue and evidence management.
+- [dfdisk](https://github.com/tylerstyle/dfdisk) - Forensic disk imaging, damaged media rescue, verification and image conversion.
```

dfdisk is still a Ratatui forensic imaging tool, and 'forensic disk imaging' and 'damaged media rescue' (via GNU ddrescue) are documented. 'Evidence management' is not documented as a capability. The tool records required case number, evidence number, and examiner metadata in acquisition reports, but it does not manage evidence. The official manifest description now says '…damaged media rescue and conversion CLI/TUI tool', and the README documents image verification and RAW↔E01 conversion. A durable rewording follows the project's own manifest.

<details>
<summary>Evidence and limitations</summary>

- Description: 'Modern forensic disk imaging, damaged media rescue and conversion CLI/TUI tool'. The manifest lists ratatui 0.30 and crossterm 0.29. [Source](https://raw.githubusercontent.com/tylerstyle/dfdisk/main/Cargo.toml)
- The README says 'dfdisk makes forensic images of disks on Linux… E01 or RAW, checks the copy… writes a report' and has sections on Damaged drives (ddrescue) and 'Checking and converting images later'. Case and evidence numbers are only acquisition metadata. No evidence-management feature is described. [Source](https://raw.githubusercontent.com/tylerstyle/dfdisk/main/README.md)
- **Limitation:** One could read 'evidence management' loosely as covering the required case and evidence metadata, reports, and remembered profile values. This is a wording-precision fix, not a relevance concern.

</details>

### pacman-utils — update

```diff
-- [pacman-utils](https://github.com/ankur3-101106/pacman-utils) - A keyboard-driven Arch Linux system manager with pacman, AUR, and reflector tools.
+- [archman](https://github.com/ankur3-101106/pacman-utils) - A keyboard-driven Arch Linux system manager with pacman, AUR, and reflector tools.
```

The project is now branded "archman": that is the README title, the Cargo package name and the logo. The repository slug is still pacman-utils, and https://github.com/ankur3-101106/pacman-utils returns 200 with no redirect, so the URL stays the same. The description is still accurate: it is a keyboard-driven Ratatui Arch system manager running pacman, AUR helpers (yay/paru) and reflector. Suggest renaming the entry to archman.

<details>
<summary>Evidence and limitations</summary>

- name = "archman"; description "Interactive Arch Linux system manager with a ratatui interface"; ratatui = "0.29". [Source](https://raw.githubusercontent.com/ankur3-101106/pacman-utils/main/Cargo.toml)
- Heading "# archman", "Interactive Arch Linux System Manager & TUI Dashboard", "A fast, keyboard-driven terminal dashboard". The embedded runner runs "Pacman, AUR helpers (yay/paru), and reflector". [Source](https://raw.githubusercontent.com/ankur3-101106/pacman-utils/main/README.md)
- Returns HTTP 200 at the same URL with no redirect. The repository has not been renamed. [Source](https://github.com/ankur3-101106/pacman-utils)
- **Limitation:** The GitHub repo description in the packet still reads "All available pacman options combined into one interactive script". Only the README and crate use the new name.
- **Limitation:** The README also describes mirror management for 12 distributions. That is extra scope and does not need to go in the description.

</details>

### passepartui — update

```diff
-- [passepartui](https://github.com/kardwen/passepartui) - A TUI for managing the pass password store.
+- [passepartui](https://github.com/kardwen/passepartui) - A TUI for browsing and copying passwords from the pass password store.
```

Project is a ratatui TUI for pass and remains relevant, but README explicitly says no password-store manipulation (adding/deleting) is implemented; it supports navigation, search/filter, and viewing/copying passwords and OTPs. "Managing" overstates this; a neutral wording matching the upstream tagline is more accurate.

<details>
<summary>Evidence and limitations</summary>

- "Currently, no functionality for manipulating the password store (e.g. adding or deleting a password) is implemented. For those operations use pass directly"; features: navigation, search/filter, viewing and copying passwords/OTPs. [Source](https://raw.githubusercontent.com/kardwen/passepartui/main/README.md)
- description "A TUI for pass"; ratatui 0.29.0. [Source](https://raw.githubusercontent.com/kardwen/passepartui/main/Cargo.toml)
- **Limitation:** Project describes itself as alpha; last push 2025-05-07, so write support could be added later.

</details>

### sc-cli — update

```diff
-- [sc-cli](https://github.com/lnds/sc-cli) - A TUI for Shortcut (formerly know as Clubhouse) a project management tool for teams.
+- [sc-cli](https://github.com/lnds/sc-cli) - A TUI for Shortcut (formerly known as Clubhouse), a project management tool for teams.
```

lnds/sc-cli remains a ratatui CLI+TUI client for Shortcut stories, but the entry has a spelling error ("formerly know as" → "known") and missing punctuation; contribution rules require checking spelling/grammar. Clubhouse→Shortcut rename is real but README doesn't mention it; the parenthetical is retained.

<details>
<summary>Evidence and limitations</summary>

- description "CLI and TUI client for Shortcut stories"; ratatui 0.29, tui-textarea, crossterm. [Source](https://raw.githubusercontent.com/lnds/sc-cli/main/Cargo.toml)
- "Shortcut CLI & TUI"; Built With Ratatui badge; manages Shortcut stories via API. [Source](https://raw.githubusercontent.com/lnds/sc-cli/main/README.md)
- **Limitation:** Change is editorial only.

</details>

### glues — update

```diff
-- [glues](https://github.com/gluesql/glues) - A sync-enabled TUI note-taking app with Git, CSV, and JSON support.
+- [glues](https://github.com/gluesql/glues) - A Vim-inspired, privacy-first TUI note-taking app with Git sync and multiple storage backends.
```

Glues is still a relevant ratatui note-taking TUI, but the entry's 'Git, CSV, and JSON support' is out of date. The README up to v0.7.0 listed a 'CSV or JSON' storage option. From v0.8.0 the README instead documents Instant, Local (file-per-note), redb, Git, MongoDB and Proxy backends, and no longer mentions CSV or JSON. The TUI still enables GlueSQL CsvStorage, but only for its own configuration (tui/src/config.rs). The suggested wording drops the unsupported CSV/JSON claim and avoids listing volatile backends.

<details>
<summary>Evidence and limitations</summary>

- glues-tui depends on ratatui 0.30.0 with crossterm, tui-input and tui-big-text. [Source](https://raw.githubusercontent.com/gluesql/glues/main/tui/Cargo.toml)
- 'Vim-inspired, privacy-first TUI note-taking app with multiple storage options'. The listed options are Instant, Local, redb, Git, MongoDB and Proxy. Git storage syncs automatically with a remote. CSV and JSON appear nowhere. [Source](https://raw.githubusercontent.com/gluesql/glues/main/README.md)
- The v0.7.0 README still had a '**CSV or JSON**' storage section ('CSV saves data in comma-separated format, while JSON uses JSONL'). [Source](https://raw.githubusercontent.com/gluesql/glues/v0.7.0/README.md)
- The v0.8.0 README no longer mentions CSV or JSON storage. [Source](https://raw.githubusercontent.com/gluesql/glues/v0.8.0/README.md)
- get_glue() returns Glue<CsvStorage> 'for configuration', so CSV is used internally for config, not as a user note backend. [Source](https://raw.githubusercontent.com/gluesql/glues/main/tui/src/config.rs)
- **Limitation:** The v0.8.0 release notes do not explicitly announce removing CSV/JSON. The conclusion comes from the README change between the v0.7.0 and v0.8.0 tags plus the current docs.
- **Limitation:** The software was not run.

</details>

### leetrs — update

```diff
-- [leetrs](https://github.com/shadowmkj/leetrs) - A TUI for browsing, testing, and submitting LeetCode problems directly from your terminal.
+- [leetrs](https://github.com/shadowmkj/leetrs) - A CLI and TUI for browsing, testing, and submitting LeetCode problems from your terminal.
```

Relevant: canonical repo shadowmkj/leetrs ships a Ratatui TUI, and the identity is correct. The entry's wording is inaccurate, though. It calls leetrs 'A TUI for browsing, testing, and submitting', but the official docs limit the TUI to searching, filtering and picking problems. Testing and submitting are separate CLI subcommands ('leetrs test' and 'leetrs submit') that act on solution files edited in Neovim. Suggested rewording describes it as a CLI and TUI.

<details>
<summary>Evidence and limitations</summary>

- API full_name matches; not archived. Description: 'Rust-powered CLI and engine ... solving LeetCode problems from the terminal'. [Source](https://github.com/shadowmkj/leetrs)
- Workspace members: '.', crates/cookie-extract and xtask. The root crate depends on ratatui 0.30.0, crossterm and tui-input. [Source](https://raw.githubusercontent.com/shadowmkj/leetrs/main/Cargo.toml)
- 'A blazing-fast, Rust-powered CLI engine and TUI for solving LeetCode problems natively in Neovim.' Workflow: Browse & Search in the TUI, then Fetch, Edit in Neovim, and Test & Submit. [Source](https://raw.githubusercontent.com/shadowmkj/leetrs/main/README.md)
- 'Launches the interactive Ratatui terminal browser for searching, filtering, and picking LeetCode problems.' Enter triggers 'leetrs pick'. No test or submit actions are listed. [Source](https://raw.githubusercontent.com/shadowmkj/leetrs/main/docs/docs/cli-reference/tui.md)
- 'leetrs test <FILE>' and 'leetrs submit' are standalone CLI commands. [Source](https://raw.githubusercontent.com/shadowmkj/leetrs/main/docs/docs/cli-reference/test-and-submit.md)
- **Limitation:** Did not run the software. A hidden TUI keybinding for test/submit cannot be ruled out, but none appears in the TUI docs. The README's keybinding section was only partly checked.

</details>

### chordflow — remove

```diff
-- [chordflow](https://github.com/timvancann/chordflow) - A tool for practicing improvisation and mastering the guitar neck.
```

The official repository removed ChordFlow's Ratatui TUI. It is now only a Dioxus desktop GUI. The chordflow_tui crate (ratatui 0.29) was dropped from the workspace members by tag v0.4.0. Commit a2a43b68 ('migrating to cpal', 2026-01-02) then deleted its source. Every tag from v0.4.0 to v0.7.0 lists only chordflow_desktop and chordflow_music_theory, and the README calls it 'a desktop app' using the Dioxus CLI. The guitar-practice description is still accurate, but the listed implementation no longer has a Ratatui/TUI interface.

<details>
<summary>Evidence and limitations</summary>

- Workspace members are only chordflow_desktop and chordflow_music_theory. [Source](https://raw.githubusercontent.com/timvancann/chordflow/main/Cargo.toml)
- Commit 'migrating to cpal' removed chordflow_tui/Cargo.toml, main.rs, ui.rs and keymap.rs. [Source](https://github.com/timvancann/chordflow/commit/a2a43b68)
- The pre-removal chordflow_tui crate depended on ratatui 0.29.0 and crossterm. [Source](https://raw.githubusercontent.com/timvancann/chordflow/94d35a81/chordflow_tui/Cargo.toml)
- Current UI depends on dioxus 0.7.2 (desktop/web/mobile). No ratatui. [Source](https://raw.githubusercontent.com/timvancann/chordflow/main/chordflow_desktop/Cargo.toml)
- README: 'ChordFlow is a desktop app'. Usage requires the Dioxus CLI. The roadmap marks 'Use Dioxus to create a GUI native app' done. Latest release v0.7.0 (2026-08-27). [Source](https://github.com/timvancann/chordflow)
- **Limitation:** Old tags (e.g. 0.3.3) still list chordflow_tui as a workspace member. No maintenance or support status for those legacy TUI tags was found, and none is inferred from their existence.
- **Limitation:** A crates.io lookup for chordflow_tui returned no crate data.

</details>

### gtm — update

```diff
-- [gtm](https://github.com/prjctimg/gtm) - Feature rich audio player built for terminal enthusiasts.
+- [gtm](https://github.com/craftty-org/gtm) - Feature rich audio player built for terminal enthusiasts.
```

The listed URL github.com/prjctimg/gtm returns HTTP 301 to github.com/craftty-org/gtm. The API reports the canonical name as craftty-org/gtm (an organization, not a fork), and the workspace manifest declares that URL as its repository. The project is still a Ratatui terminal audio player, the name is unchanged and the description is accurate, so only the URL needs updating.

<details>
<summary>Evidence and limitations</summary>

- HTTP 301 with Location: https://github.com/craftty-org/gtm. [Source](https://github.com/prjctimg/gtm)
- Workspace members gtm and gtmd. repository = "https://github.com/craftty-org/gtm". Version 0.2.97. [Source](https://raw.githubusercontent.com/craftty-org/gtm/dev/Cargo.toml)
- The gtm client crate depends on ratatui 0.30, tui-big-text and ratatui-image. [Source](https://raw.githubusercontent.com/craftty-org/gtm/dev/gtm/Cargo.toml)
- README: 'The missing (terminal) audio player' with background playback, YouTube/Spotify, radio and podcasts. Repo description: 'cross platform, feature rich and hackable terminal audio player'. Default branch dev; pushed 2026-11-09. [Source](https://github.com/craftty-org/gtm)

</details>

### rs-pug — update

```diff
-- [rs-pug](https://github.com/JustRoccat/rs-pug) - A Neovim-inspired asynchronous music player with a reactive audio visualizer.
+- [rs-pug](https://github.com/JustRoccat/rs-pug) - A terminal music player for YouTube, SoundCloud and local files, with Lua plugins and a real-time audio visualizer.
```

Relevant: it depends on ratatui 0.30 and is a terminal music player built on mpv and yt-dlp. However, the entry's lead claim, "Neovim-inspired", has no support in the current README, docs-usage.md or GitHub description. Grepping them for vim/neovim finds nothing. The current docs present it as a terminal player that streams from YouTube, SoundCloud and Sonum, plays local files, has a real-time FFT spectrum visualizer and is extensible with Lua plugins. "Asynchronous" (it uses tokio) and "reactive audio visualizer" are still supported. The suggested wording drops the unsupported claim and names the documented core features.

<details>
<summary>Evidence and limitations</summary>

- The description is "Blazing fast tui music player". It depends on ratatui 0.30, ratatui-image and tokio. [Source](https://raw.githubusercontent.com/JustRoccat/rs-pug/main/Cargo.toml)
- The README describes "a terminal music player built in Rust on top of mpv, yt-dlp, and ratatui". It streams from YouTube, SoundCloud and Sonum, plays local files, has a real-time FFT spectrum visualizer and supports Lua plugins. It never mentions Neovim or Vim. [Source](https://github.com/JustRoccat/rs-pug)
- The usage guide documents number-key tabs and a ':' command palette. It does not describe the app as Neovim-inspired. [Source](https://raw.githubusercontent.com/JustRoccat/rs-pug/main/docs-usage.md)
- **Limitation:** Nothing officially contradicts the Neovim claim; it is simply unsupported. A ':' command palette exists, and an earlier README may have used that wording.

</details>

### mlbt — update

```diff
-- [mlbt](https://github.com/mlb-rs/mlbt) - A tui for the MLB Statcast API. Watch a live game using Gameday, or check scores, standings, and stats.
+- [mlbt](https://github.com/mlb-rs/mlbt) - A TUI for the MLB Stats API. Watch a live game using Gameday, or check scores, standings, and stats.
```

The project is still a ratatui TUI with Gameday, scores, standings and stats. However, it uses MLB's Stats API (statsapi.mlb.com), not a 'Statcast API'. The README and the GitHub description both say 'MLB Stats API', so the API name in the entry is factually wrong.

<details>
<summary>Evidence and limitations</summary>

- Declares tui = { package = "ratatui", version = "0.30.2" } and tui-logger. [Source](https://raw.githubusercontent.com/mlb-rs/mlbt/main/Cargo.toml)
- README: 'Gameday, scores, stats, standings, teams, and player profiles. Powered by MLB's Stats API'. The word Statcast does not appear anywhere in the README. [Source](https://github.com/mlb-rs/mlbt/blob/main/README.md)
- BASE_URL is https://statsapi.mlb.com/api/. [Source](https://raw.githubusercontent.com/mlb-rs/mlbt/main/api/src/client.rs)
- **Limitation:** The app may show some Statcast-derived metrics (e.g. exit velocity) that come through the Stats API. The correction is only about the API's name.

</details>

### ssHattrick — update

```diff
-- [ssHattrick](https://github.com/ricott1/sshattrick) - A multiplayer terminal version of the Hattrick football-management game, playable over SSH.
+- [ssHattrick](https://github.com/ricott1/sshattrick) - A multiplayer terminal hockey game inspired by the Atari 7800 Hat Trick, playable over SSH.
```

Still a ratatui multiplayer game played over SSH, but it is a hockey game, not a 'Hattrick football-management game'. The crate manifests describe it as 'Hockey in your terminal over SSH'. The README's 'Hattrick' link goes to the Atari 7800 game Hat Trick (a hockey game), not the online football manager hattrick.org.

<details>
<summary>Evidence and limitations</summary>

- description = "Hockey in your terminal over SSH." Depends on ratatui 0.30. [Source](https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick/Cargo.toml)
- description: 'Pure game logic and asset rendering for sshattrick - hockey in your terminal'. Keywords include game, hockey, tui. [Source](https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick-core/Cargo.toml)
- 'multiplayer game that you can play over SSH. It is a clone of the popular game Hattrick'. The link goes to retrogames.cz play_1368-Atari7800. [Source](https://github.com/ricott1/sshattrick/blob/main/README.md)
- Page title: 'Hat Trick (Atari 7800) - online game'. [Source](https://www.retrogames.cz/play_1368-Atari7800.php)

</details>

## Needs more evidence (2)

### [dekit](https://github.com/pvolok/dekit)

mprocs was renamed to dekit, now a 'Process manager for dev and prod'. The listed description is the legacy mprocs tagline, so it is outdated. Relevance is also unresolved. Ratatui no longer appears in the current src/Cargo.toml or Cargo.lock. Tags v0.8.0/v0.8.3 still listed ratatui, v0.9.0 does not, and the changelog for 0.9.0 says terminal internals were rewritten. The console UI now imports the in-house crate::term module. The only ratatui-ecosystem dependency left is tui-input 0.15 with default-features = false. There is no official statement about Ratatui, and the TUI still exists. Maintainer should decide whether tui-input alone is enough for the list before any description update.

- Did not exhaustively search every source file for vendored ratatui code; conclusion rests on manifests, lockfile and sampled imports.
- The legacy mprocs crate on crates.io (max 0.9.6, which itself lacks a ratatui dependency) was not otherwise evaluated.

<details>
<summary>Supporting evidence</summary>

- Package 'dekit' 0.10.3, 'Process manager for dev and prod', keywords include 'tui' and 'mprocs'. No ratatui dependency; tui-input 0.15.0 with default-features = false. [Source](https://raw.githubusercontent.com/pvolok/dekit/HEAD/src/Cargo.toml)
- The lockfile contains crossterm, termwiz and tui-input packages but no ratatui package. [Source](https://raw.githubusercontent.com/pvolok/dekit/HEAD/Cargo.lock)
- Console UI imports crate::term::{Grid, Rgb, grid::Rect, style::Style}, an in-house renderer rather than ratatui. [Source](https://raw.githubusercontent.com/pvolok/dekit/HEAD/src/console/ui_tasks.rs)
- The v0.8.3 manifest still referenced ratatui; the v0.9.0 manifest has no ratatui reference (v0.7.3 had tui = ratatui 0.26.2). [Source](https://raw.githubusercontent.com/pvolok/dekit/v0.8.3/src/Cargo.toml)
- 0.9.0 (2026-03-19): 'A lot of terminal/pty related internals were rewritten'. A later entry: 'The terminal emulator and renderer were rewritten'. [Source](https://raw.githubusercontent.com/pvolok/dekit/HEAD/CHANGELOG.md)
- 'mprocs has been renamed to dekit'; legacy CLI available as 'dekit mprocs …'. The listed description is the old mprocs tagline. https://github.com/pvolok/mprocs redirects to pvolok/dekit. [Source](https://raw.githubusercontent.com/pvolok/dekit/HEAD/README-mprocs.md)

</details>

### [pumas](https://github.com/graelo/pumas)

The latest published release (0.5.0, on crates.io and tagged v0.5.0) depends on Ratatui with termion. The default branch `main` no longer lists ratatui and instead uses iocraft (0.9), a different, non-Ratatui TUI library. The project is still a terminal power-usage monitor for Apple Silicon, and the description stays accurate. Unresolved: whether the next release will ship without Ratatui. Until then, the currently installable version is Ratatui-based.

- I did not find the specific commit or changelog entry for the ratatui-to-iocraft migration (the GitHub API was rate-limited).

<details>
<summary>Supporting evidence</summary>

- main (still version 0.5.0) has a "# ui" section listing iocraft = "0.9" and smol. There is no ratatui or termion dependency. [Source](https://raw.githubusercontent.com/graelo/pumas/main/Cargo.toml)
- The v0.5.0 tag lists ratatui 0.30 (termion feature) and termion 4. [Source](https://raw.githubusercontent.com/graelo/pumas/v0.5.0/Cargo.toml)
- Published crate 0.5.0 (2026-04-14, the newest) depends on ratatui and termion. [Source](https://crates.io/api/v1/crates/pumas/0.5.0/dependencies)
- Recent main commits include "chore(deps): bump iocraft to 0.9". The repo is active (latest commit 2026-11-02). [Source](https://github.com/graelo/pumas/commits/main.atom)
- "A nvtop-inspired command line tool for Apple Silicon Macs", a Rust reimplementation of asitop. It requires sudo for powermetrics. The README does not mention which UI library it uses. [Source](https://raw.githubusercontent.com/graelo/pumas/main/README.md)

</details>


## Snapshot issues — no change recommended (13)

### [ratatui-comfy-tabs](https://crates.io/crates/ratatui-comfy-tabs)

The packet snapshot was unavailable, but crates.io and GitLab were readable. ratatui-comfy-tabs 0.5.12 (GitLab comfyhome/crates/ratatui-comfy-tabs, active as of 2026-07-04) depends on ratatui-core and is described as an advanced, highly customizable tab-bar navigation widget for Ratatui. The listing's description matches.

- The GitLab API returned no 'archived' field for this project (null), so archive status was not confirmed through the API.
- Did not run the software.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- 'An advanced tab-bar navigation widget for Ratatui. Highly customizable, with built-in multi-position rendering logic.' Version 0.5.12, repository gitlab.com/comfyhome/crates/ratatui-comfy-tabs. [Source](https://crates.io/api/v1/crates/ratatui-comfy-tabs)
- Depends on ratatui-core 0.1.2; ratatui 0.30.2 (crossterm) for dev and examples. [Source](https://gitlab.com/comfyhome/crates/ratatui-comfy-tabs/-/raw/main/Cargo.toml)
- 'Lightweight, customizable tab navigation for Ratatui' with horizontal and vertical layouts. Also mirrored at github.com/comfy-home/misc-RatatuiComfyTabs. [Source](https://gitlab.com/comfyhome/crates/ratatui-comfy-tabs/-/raw/main/README.md)

</details>

### [ratatui-comfy-toaster](https://crates.io/crates/ratatui-comfy-toaster)

The packet snapshot was unavailable, but crates.io and GitLab were readable. ratatui-comfy-toaster 0.6.2 (GitLab comfyhome/crates/ratatui-comfy-toaster, active as of 2026-07-18) depends on ratatui 0.30. Its README calls it 'An advanced toast notification engine for Ratatui terminal UI applications' and an enhanced fork of ratatui-toaster. The listing matches.

- The GitLab API returned no 'archived' field for this project (null), so archive status was not confirmed through the API.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- 'An advanced toast engine for ratatui. Timed toast notifications | Sticky toasts ... | Presets'. Version 0.6.2. [Source](https://crates.io/api/v1/crates/ratatui-comfy-toaster)
- Depends on ratatui 0.30 (unstable-widget-ref). Attribution: based on ratatui-toaster v0.1.2. [Source](https://gitlab.com/comfyhome/crates/ratatui-comfy-toaster/-/raw/main/Cargo.toml)
- 'An advanced toast notification engine for Ratatui terminal UI applications... an enhanced fork of ratatui-toaster.' [Source](https://gitlab.com/comfyhome/crates/ratatui-comfy-toaster/-/raw/main/README.md)

</details>

### [tui-dialog](https://crates.io/crates/tui-dialog)

The packet snapshot failed because the source is on Codeberg, not GitHub. I read Codeberg directly: the crate is a single-line text-entry dialog widget for Ratatui, matching the description.

- The README says the widget only works with the crossterm backend.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- max_version 0.5.0 (2026-01-17), not yanked; repository https://codeberg.org/kdwarn/tui-dialog. [Source](https://crates.io/api/v1/crates/tui-dialog)
- Depends on ratatui 0.30.0, ratatui-core and crossterm; 'A widget for entering a single line of text in a dialog for Ratatui.' [Source](https://codeberg.org/kdwarn/tui-dialog/raw/branch/main/Cargo.toml)
- Repo kdwarn/tui-dialog, archived=false, default branch main. [Source](https://codeberg.org/api/v1/repos/kdwarn/tui-dialog)

</details>

### [tui-nodes](https://crates.io/crates/tui-nodes)

The packet snapshot failed because the source is on SourceHut. I read SourceHut directly: the crate is a node-graph visualization widget that now depends on ratatui 0.30, matching the description.

- The upstream README and manifest still mention tui-rs; the catalog description does not, so it needs no change.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- max_version 0.10.0 (2026-01-07), not yanked; repository https://git.sr.ht/~jaxter184/tui-nodes. [Source](https://crates.io/api/v1/crates/tui-nodes)
- Depends on ratatui 0.30.0; description 'Node graph visualization for tui-rs' (the manifest wording predates the move to ratatui). [Source](https://git.sr.ht/~jaxter184/tui-nodes/blob/HEAD/Cargo.toml)
- Repository page returns HTTP 200. [Source](https://git.sr.ht/~jaxter184/tui-nodes)

</details>

### [color-to-tui](https://crates.io/crates/color-to-tui)

The packet snapshot was unavailable, so this was checked directly. crates.io confirms that color-to-tui depends on ratatui and that its description matches the entry. The primary repository at git.uttarayan.me returned HTTP 502, which needs a recheck and is not evidence the project is dead. The GitHub mirror shows the crate parses hex and indexed colors into ratatui Color, with serde helpers.

- The primary repository host could not be read, so its current contents were checked only through the GitHub mirror and the crates.io/docs.rs metadata.
- The last release was in 2023 and the version requirement is ratatui '0.*'. Compatibility with current ratatui versions was not tested.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- Latest version 0.3.0 (2023-04-03), not yanked. The repository and homepage are https://git.uttarayan.me/uttarayan/color-to-tui. Version 0.3.0 depends on ratatui '0.*', serde and serde_json. [Source](https://crates.io/api/v1/crates/color-to-tui)
- The docs.rs description reads 'Parse colors and convert them to ratatui::style::Colors', matching the entry. [Source](https://docs.rs/crate/color-to-tui/latest)
- GitHub mirror, not archived, last push 2023-09-26. Its README describes parsing HEX colors to ratatui Rgb colors (e.g. '#C3F111' -> Color::Rgb) and indexed values (e.g. '142' -> Color::Indexed). [Source](https://github.com/uttarayan21/color-to-tui)
- Returned HTTP 502 Bad Gateway when checked. This needs a recheck. [Source](https://git.uttarayan.me/uttarayan/color-to-tui)

</details>

### [ratatui-input-manager](https://crates.io/crates/ratatui-input-manager)

The crate is live (v0.4.0). Its keymap attribute macro declares input handlers, and its crossterm, termion and termwiz features match the entry. The README does not use the phrase 'Elm style', but nothing contradicts it.

- The package snapshot was incomplete, so I used the crates.io API and the README instead. The 'Elm style' wording is unsupported by current docs; a maintainer could simplify it, but it is not a confirmed error.
- The crate also includes keybinding help widgets, which the entry does not mention.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- Version 0.4.0. Features: crossterm, termion, termwiz, widgets (default crossterm + widgets). Description: 'declarative approach to handling inputs in ratatui'. The repository field is null on crates.io. [Source](https://crates.io/api/v1/crates/ratatui-input-manager)
- The README shows a #[keymap(backend = "crossterm")] macro on impl App with #[keybind] methods, dispatched through app.handle(event). It also ships Help and HelpBar widgets. Source repo garryod/ratatui-input-manager (linked from the README badge) is not archived. [Source](https://raw.githubusercontent.com/garryod/ratatui-input-manager/HEAD/README.md)
- docs.rs 0.4.0 builds. Optional dependencies: crossterm, termion, termwiz, ratatui-core and ratatui-widgets. [Source](https://docs.rs/ratatui-input-manager/latest/ratatui_input_manager/)

</details>

### [JocalSend](https://git.kittencollective.com/nebkor/joecalsend)

Forgejo repo is live; the crate jocalsend is a Ratatui TUI implementing the LocalSend protocol. Description is accurate.

- The repo slug (joecalsend) differs from the display/crate name (jocalsend/JocalSend). This is consistent with official metadata, not an error.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- Package jocalsend is described as "A TUI for LocalSend". It depends on ratatui 0.29 and ratatui-explorer, and its repository field points to this URL. [Source](https://git.kittencollective.com/nebkor/joecalsend/raw/branch/main/Cargo.toml)
- Returns HTTP 200 with no redirect. The README says JocalSend "uses Ratatui to provide an interactive terminal-based" LocalSend client that can send and receive files and text. [Source](https://git.kittencollective.com/nebkor/joecalsend)

</details>

### [pgtui](https://codeberg.org/kdwarn/pgtui)

A Ratatui PostgreSQL TUI client that opens your terminal editor for inserts and updates.


The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- Package pgtui depends on ratatui = "0.30" and tui-dialog. [Source](https://codeberg.org/kdwarn/pgtui/raw/branch/main/Cargo.toml)
- "pgtui is a Postgres TUI client that handles basic CRUD operations, utilizing your terminal editor for inserts and updates." [Source](https://codeberg.org/kdwarn/pgtui/raw/branch/main/README.md)

</details>

### [taskfinder](https://crates.io/crates/taskfinder)

Packet snapshot was unavailable, but crates.io metadata was read directly: taskfinder 2.19.0 is a ratatui TUI extracting tasks from plain text files with editor hook, matching the entry; crates.io link is consistent with contribution guidance.

- Codeberg source repository was not read directly; verification relies on crates.io metadata.

The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- description "A terminal user interface that extracts and displays tasks from plain text files, hooking into your default terminal-based editor for editing."; max_version 2.19.0, updated 2026-11-09; repository https://codeberg.org/kdwarn/taskfinder. [Source](https://crates.io/api/v1/crates/taskfinder)
- Depends on ratatui ^0.30.0 and crossterm ^0.29.0. [Source](https://crates.io/api/v1/crates/taskfinder/2.19.0/dependencies)

</details>

### [isw](https://gitlab.com/thom-cameron/isw)

GitLab project resolves at its canonical path and uses Ratatui. The README describes a TUI stopwatch with intervals and gives a pomodoro example, which matches the entry.


The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- path_with_namespace is thom-cameron/isw. Description: 'a simple terminal stopwatch application'. last_activity_at is 2026-10-23. [Source](https://gitlab.com/api/v4/projects/thom-cameron%2Fisw)
- Depends on ratatui 0.29.0 and crossterm 0.29.0. [Source](https://gitlab.com/thom-cameron/isw/-/raw/main/Cargo.toml)
- Features include 'a basic stopwatch in a nice tui' with intervals. A '### pomodoro' section shows a 25/5 pomodoro setup. [Source](https://gitlab.com/thom-cameron/isw/-/raw/main/readme.md)

</details>

### [angry-duiker](https://gitlab.com/fizzizist/angry-duiker-2)

angry-duiker is a Ratatui TUI music player that streams from DLNA media servers. This matches the listed description.


The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- Canonical path fizzizist/angry-duiker-2. Description: 'A TUI DLNA music player written in Rust.' Default branch master; last activity 2026-04-03. [Source](https://gitlab.com/api/v4/projects/fizzizist%2Fangry-duiker-2)
- Dependencies: ratatui 0.29, ratatui-image, tui-textarea, and rupnp (UPnP/DLNA). [Source](https://gitlab.com/fizzizist/angry-duiker-2/-/raw/master/Cargo.toml)
- 'A TUI DLNA music player. Allows you to stream your music from any DLNA server on your network such as Plex or MiniDLNA.' [Source](https://gitlab.com/fizzizist/angry-duiker-2/-/raw/master/README.md)

</details>

### [enimtui](https://codeberg.org/tranzystorekk/enimtui)

A Codeberg ratatui minesweeper game; the README matches the description.


The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- ratatui 0.30 with crossterm and layout-cache features. [Source](https://codeberg.org/tranzystorekk/enimtui/raw/branch/main/Cargo.toml)
- README: 'another attempt to create a delightfully simple minesweeper game, this time in your terminal'. Codeberg API: archived=false, updated 2025-12. [Source](https://codeberg.org/tranzystorekk/enimtui)

</details>

### [Thardians](https://gitlab.com/thustle/thardians-rs)

GitLab project thustle/thardians-rs is a Space Invaders game built with Ratatui; description accurate.


The review recommends keeping this entry, but its source snapshot was not complete enough to save it as an unchanged baseline.

<details>
<summary>Supporting evidence</summary>

- Official metadata: path thustle/thardians-rs, description 'A Space Invaders game for the terminal using Ratatui.', topics include ratatui, last activity 2026-08-02. [Source](https://gitlab.com/api/v4/projects/thustle%2Fthardians-rs)
- Depends on ratatui = "0.30.0"; README: 'A space invaders game you can play in the terminal, using the Ratatui terminal UI.' [Source](https://gitlab.com/thustle/thardians-rs/-/raw/master/Cargo.toml)

</details>
