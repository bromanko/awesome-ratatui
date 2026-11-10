#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
npm ci --ignore-scripts --no-audit --no-fund
printf '%s\n' "$PWD/node_modules/.bin" >> "$GITHUB_PATH"
tool_dir="$RUNNER_TEMP/freshness-tools"
mkdir -p "$tool_dir"
cd "$tool_dir"
curl -fsSL https://github.com/crate-ci/typos/releases/download/v1.51.1/typos-v1.51.1-x86_64-unknown-linux-musl.tar.gz -o typos.tar.gz
curl -fsSL https://github.com/lycheeverse/lychee/releases/download/lychee-v0.24.2/lychee-x86_64-unknown-linux-gnu.tar.gz -o lychee.tar.gz
printf '%s\n' '93c301fd4120ff076e2cc2a6d6a61cab4a4bdb81899287c0938b452e56d1f454  typos.tar.gz' '1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a  lychee.tar.gz' | sha256sum -c -
tar -xzf typos.tar.gz
tar -xzf lychee.tar.gz
install -m 755 lychee-x86_64-unknown-linux-gnu/lychee "$tool_dir/lychee"
"$tool_dir/typos" --version
"$tool_dir/lychee" --version
printf '%s\n' "$tool_dir" >> "$GITHUB_PATH"
