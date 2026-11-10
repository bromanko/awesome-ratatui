> **Real review · November 10, 2026.** Executed locally using the Claude subscription; this Actions job displays the saved result. Selected the known ssHattrick finding and two adjacent entries. Runtime: 2m 42s; recorded usage equivalent: $0.2405. No correction was submitted.

# Catalog review

**1 ready for review · 0 held**

3 checked · 2 unchanged · 1 researched · 0 source checks unavailable

<h2>ssHattrick — Ready for maintainer review</h2>

```diff
--- a/README.md
+++ b/README.md
@@ -703,7 +703,7 @@
 - [rust-sadari-cli](https://github.com/24seconds/rust-sadari-cli) - Rust sadari game based on terminal! (Ghost leg or Amidakuji in another words).
 - [sharad-ratatui](https://github.com/ProHaller/sharad_ratatui) - A text-based Shadowrun role-playing game.
 - [Snake](https://github.com/kriskw1999/ratatui-snake) - Simple terminal based snake game.
-- [ssHattrick](https://github.com/ricott1/sshattrick) - A multiplayer terminal version of the Hattrick football-management game, playable over SSH.
+- [ssHattrick](https://github.com/ricott1/sshattrick) - A multiplayer terminal clone of the Atari 7800 hockey game Hat Trick, playable over SSH.
 - [sued-rs](https://github.com/Danilo-Guedes/sued-rs) - A horror-themed recreation of SueD, the 2000s Brazilian prank oracle.
 - [sxtetris](https://github.com/shixinhuang99/sxtetris) - A terminal Tetris game.
 - [tage](https://github.com/jacopograndi/tage) - Turn based strategy game with multiplayer, empires and warfare.
```

<details>
<summary>Evidence and checks</summary>

<p>The project is still relevant: the `sshattrick` binary crate depends on ratatui 0.30, and the repo is active and not archived. Its canonical identity is unchanged (ricott1/sshattrick, HTTP 200, no redirect). The entry&#x27;s description is factually wrong, though. The README says the game is a clone of Hattrick and links to the Atari 7800 game page, which RetroGames.cz titles &#x27;Hat Trick&#x27;. The crate describes itself as &#x27;Hockey in your terminal over SSH.&#x27; So it is a hockey arcade game, not the Hattrick football-management game. The multiplayer and SSH claims are still accurate.</p>

<p>https://raw.githubusercontent.com/ricott1/sshattrick/main/README.md — README: &#x27;ssHattrick is a multiplayer game that you can play over SSH. It is a clone of the popular game [Hattrick](https://www.retrogames.cz/play_1368-Atari7800.php).&#x27; Play via `ssh frittura.org` or self-host the server.</p>

<p>https://www.retrogames.cz/play_1368-Atari7800.php — The linked reference game page title is &#x27;Hat Trick (Atari 7800) - online game&#x27;, an arcade ice hockey game, not the football-management browser game.</p>

<p>https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick/Cargo.toml — Package sshattrick 0.2.1, description &#x27;Hockey in your terminal over SSH.&#x27;, keywords include ratatui/ssh/multiplayer; depends on ratatui 0.30.0 (unstable-backend-writer), crossterm 0.29, frittura-ssh-core.</p>

<p>https://raw.githubusercontent.com/ricott1/sshattrick/main/Cargo.toml — Root is a workspace with members crates/sshattrick-core and crates/sshattrick; root has no dependencies itself.</p>

<p>https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick-core/Cargo.toml — sshattrick-core: &#x27;Pure game logic and asset rendering for sshattrick - hockey in your terminal.&#x27;; ratatui is a dev-dependency.</p>

<p>https://api.github.com/repos/ricott1/sshattrick — full_name ricott1/sshattrick, archived false, default_branch main, pushed_at 2026-05-30, homepage https://crates.io/crates/sshattrick. GitHub description &#x27;Play Hattrick in your terminal over SSH&#x27;.</p>

<p>https://crates.io/api/v1/crates/sshattrick — Crate sshattrick, newest version 0.2.1, description &#x27;Hockey in your terminal over SSH.&#x27;, repository is the GitHub repo.</p>

<p>Caveats: The game was not run, and the public SSH server (frittura.org) was not tested. The README itself warns that the server is often down.; The GitHub repo description still says only &#x27;Play Hattrick&#x27;, so the hockey genre comes from the README link and the crate metadata.</p>

<p>related: The only match is merged PR #31 (https://github.com/ratatui/awesome-ratatui/pull/31). In that PR the author, ricott1, first added the ssHattrick entry. Its description was &#x27;Play Hattrick in your terminal over SSH.&#x27; Maintainer orhun approved it (https://github.com/ratatui/awesome-ratatui/pull/31#pullrequestreview-1899554597) and commented &#x27;No freaking way!&#x27; (https://github.com/ratatui/awesome-ratatui/pull/31#issuecomment-1962532900). That PR created the original entry. It did not make the proposed correction, and it does not say the game is football management or hockey. Nothing in it objects to calling the game a hockey game. The packet has no open PR that competes with this description fix, so the record is useful background but not a duplicate, rejection or obsolete change. Four searches were run: &#x27;ssHattrick&#x27; and the repo URL, each in ratatui/awesome-ratatui and bromanko/awesome-ratatui. The search is marked complete. One caveat: the GitHub repo description still says only &#x27;Play Hattrick&#x27;, so the hockey label comes from the README link and the crate metadata. Checks passed; existing unrelated link failures are listed separately.</p>

</details>

<details>
<summary>Saved review baseline</summary>

0 new completed reviews · 1 pending.

The baseline was unchanged. This retained preview contains no baseline update.

</details>

<details>
<summary>Full research and run details</summary>

# Freshness research

Advisory only; every suggested change requires maintainer review.
No list edits, PRs, comments, or reviews were submitted.

Catalog revision: `cfbce4c754e2e1d59fa1ce82fcdae650955f72b7`
Slice: 185 of 196 (zero-based)
Catalog recheck: unchanged

Sources below are agent-reported observations, not independent verification.

## Entry 706

<pre>ssHattrick

The project is still relevant: the `sshattrick` binary crate depends on ratatui 0.30, and the repo is active and not archived. Its canonical identity is unchanged (ricott1/sshattrick, HTTP 200, no redirect). The entry&#x27;s description is factually wrong, though. The README says the game is a clone of Hattrick and links to the Atari 7800 game page, which RetroGames.cz titles &#x27;Hat Trick&#x27;. The crate describes itself as &#x27;Hockey in your terminal over SSH.&#x27; So it is a hockey arcade game, not the Hattrick football-management game. The multiplayer and SSH claims are still accurate.

https://raw.githubusercontent.com/ricott1/sshattrick/main/README.md
README: &#x27;ssHattrick is a multiplayer game that you can play over SSH. It is a clone of the popular game [Hattrick](https://www.retrogames.cz/play_1368-Atari7800.php).&#x27; Play via `ssh frittura.org` or self-host the server.
https://www.retrogames.cz/play_1368-Atari7800.php
The linked reference game page title is &#x27;Hat Trick (Atari 7800) - online game&#x27;, an arcade ice hockey game, not the football-management browser game.
https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick/Cargo.toml
Package sshattrick 0.2.1, description &#x27;Hockey in your terminal over SSH.&#x27;, keywords include ratatui/ssh/multiplayer; depends on ratatui 0.30.0 (unstable-backend-writer), crossterm 0.29, frittura-ssh-core.
https://raw.githubusercontent.com/ricott1/sshattrick/main/Cargo.toml
Root is a workspace with members crates/sshattrick-core and crates/sshattrick; root has no dependencies itself.
https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick-core/Cargo.toml
sshattrick-core: &#x27;Pure game logic and asset rendering for sshattrick - hockey in your terminal.&#x27;; ratatui is a dev-dependency.
https://api.github.com/repos/ricott1/sshattrick
full_name ricott1/sshattrick, archived false, default_branch main, pushed_at 2026-05-30, homepage https://crates.io/crates/sshattrick. GitHub description &#x27;Play Hattrick in your terminal over SSH&#x27;.
https://crates.io/api/v1/crates/sshattrick
Crate sshattrick, newest version 0.2.1, description &#x27;Hockey in your terminal over SSH.&#x27;, repository is the GitHub repo.

Blocking uncertainties:
None reported.

Informational caveats:
The game was not run, and the public SSH server (frittura.org) was not tested. The README itself warns that the server is often down.
The GitHub repo description still says only &#x27;Play Hattrick&#x27;, so the hockey genre comes from the README link and the crate metadata.

Recommendation: update
Proposed name: None
Proposed URL: https://github.com/ricott1/sshattrick
Proposed description: A multiplayer terminal clone of the Atari 7800 hockey game Hat Trick, playable over SSH.</pre>


</details>

Proposals only; no catalog edits or PRs submitted. Full records and checked patches are in the run artifacts.
