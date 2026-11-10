# Update ssHattrick entry

The project is still relevant: the `sshattrick` binary crate depends on ratatui 0.30, and the repo is active and not archived. Its canonical identity is unchanged (ricott1/sshattrick, HTTP 200, no redirect). The entry's description is factually wrong, though. The README says the game is a clone of Hattrick and links to the Atari 7800 game page, which RetroGames.cz titles 'Hat Trick'. The crate describes itself as 'Hockey in your terminal over SSH.' So it is a hockey arcade game, not the Hattrick football-management game. The multiplayer and SSH claims are still accurate.

Evidence:
https://raw.githubusercontent.com/ricott1/sshattrick/main/README.md — README: 'ssHattrick is a multiplayer game that you can play over SSH. It is a clone of the popular game [Hattrick](https://www.retrogames.cz/play_1368-Atari7800.php).' Play via `ssh frittura.org` or self-host the server.
https://www.retrogames.cz/play_1368-Atari7800.php — The linked reference game page title is 'Hat Trick (Atari 7800) - online game', an arcade ice hockey game, not the football-management browser game.
https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick/Cargo.toml — Package sshattrick 0.2.1, description 'Hockey in your terminal over SSH.', keywords include ratatui/ssh/multiplayer; depends on ratatui 0.30.0 (unstable-backend-writer), crossterm 0.29, frittura-ssh-core.
https://raw.githubusercontent.com/ricott1/sshattrick/main/Cargo.toml — Root is a workspace with members crates/sshattrick-core and crates/sshattrick; root has no dependencies itself.
https://raw.githubusercontent.com/ricott1/sshattrick/main/crates/sshattrick-core/Cargo.toml — sshattrick-core: 'Pure game logic and asset rendering for sshattrick - hockey in your terminal.'; ratatui is a dev-dependency.
https://api.github.com/repos/ricott1/sshattrick — full_name ricott1/sshattrick, archived false, default_branch main, pushed_at 2026-05-30, homepage https://crates.io/crates/sshattrick. GitHub description 'Play Hattrick in your terminal over SSH'.
https://crates.io/api/v1/crates/sshattrick — Crate sshattrick, newest version 0.2.1, description 'Hockey in your terminal over SSH.', repository is the GitHub repo.

Informational caveats:
The game was not run, and the public SSH server (frittura.org) was not tested. The README itself warns that the server is often down.
The GitHub repo description still says only 'Play Hattrick', so the hockey genre comes from the README link and the crate metadata.

Based on catalog revision cfbce4c754e2e1d59fa1ce82fcdae650955f72b7.
Proposed by an automated freshness review. A maintainer must verify the evidence and edit.
Validation and discussion checks are recorded below.

Review status: Ready for maintainer review
Prior discussion: related: The only match is merged PR #31 (https://github.com/ratatui/awesome-ratatui/pull/31). In that PR the author, ricott1, first added the ssHattrick entry. Its description was 'Play Hattrick in your terminal over SSH.' Maintainer orhun approved it (https://github.com/ratatui/awesome-ratatui/pull/31#pullrequestreview-1899554597) and commented 'No freaking way!' (https://github.com/ratatui/awesome-ratatui/pull/31#issuecomment-1962532900). That PR created the original entry. It did not make the proposed correction, and it does not say the game is football management or hockey. Nothing in it objects to calling the game a hockey game. The packet has no open PR that competes with this description fix, so the record is useful background but not a duplicate, rejection or obsolete change. Four searches were run: 'ssHattrick' and the repo URL, each in ratatui/awesome-ratatui and bromanko/awesome-ratatui. The search is marked complete. One caveat: the GitHub repo description still says only 'Play Hattrick', so the hockey label comes from the README link and the crate metadata.
Validation: Checks passed; existing unrelated link failures are listed separately.
