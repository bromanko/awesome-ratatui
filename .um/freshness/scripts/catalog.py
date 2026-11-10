"""Model-free source snapshots and a versioned, reviewable catalog baseline."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import ci
import history

BASELINE = Path('.um/freshness/baseline.json')
VERSION = 1
MANIFESTS = {'cargo.toml', 'package.json', 'pyproject.toml', 'go.mod', 'gleam.toml',
             'mix.exs', 'requirements.txt', 'setup.py', 'setup.cfg', 'deno.json', 'deno.jsonc'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def key(entry):
    # Line numbers change when other entries are inserted. Duplicate URLs in different
    # sections are independent catalog claims.
    return digest([entry['url'], entry['section']])


def claim(entry, rules):
    return digest([entry['name'], entry['url'], entry['description'], entry['section'], rules])


def get_url(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'awesome-ratatui-freshness/1'})
    with urllib.request.urlopen(request, timeout=25) as response:
        body = response.read(2 * 1024 * 1024 + 1)
        if len(body) > 2 * 1024 * 1024:
            raise ValueError('Source exceeds 2 MiB; snapshot incomplete')
        return response.geturl(), body


def github_snapshot(repo):
    metadata = history.api('repos/' + repo)
    canonical = metadata['full_name']
    branch = metadata['default_branch']
    tree = history.api(f'repos/{canonical}/git/trees/{urllib.parse.quote(branch, safe="")}', recursive=1)
    if tree.get('truncated') or not isinstance(tree.get('tree'), list):
        raise ValueError('Repository tree unavailable or truncated')
    files = {}
    for item in tree['tree']:
        path = item['path']
        name = path.rsplit('/', 1)[-1].lower()
        if item['type'] == 'blob' and (name in MANIFESTS or name.startswith('readme') or path.lower().startswith('docs/') and name.endswith('.md')):
            files[path] = item['sha']
    if not files:
        raise ValueError('No README, documentation, or package manifests found')
    return dict(kind='github', repository=canonical, archived=metadata['archived'],
                description=metadata.get('description'), defaultBranch=branch, files=files)


def snapshot(entry):
    """No model, no project code execution. Incomplete fetches never become baselines."""
    url = entry['url']
    parts = urllib.parse.urlsplit(url)
    try:
        if parts.hostname == 'github.com':
            match = re.match(r'^/([^/]+)/([^/]+)', parts.path)
            if not match:
                raise ValueError('Not a GitHub repository URL')
            source = github_snapshot('/'.join(match.groups()).removesuffix('.git'))
        elif parts.hostname == 'crates.io' and parts.path.startswith('/crates/'):
            crate = parts.path.split('/')[2]
            _, body = get_url('https://crates.io/api/v1/crates/' + urllib.parse.quote(crate, safe=''))
            metadata = json.loads(body)['crate']
            source = {k: metadata.get(k) for k in ['name', 'description', 'repository', 'max_version']}
            source['kind'] = 'crate'
            match = re.match(r'^https://github.com/([^/]+/[^/#]+)', source.get('repository') or '')
            if not match:
                raise ValueError('Crate has no supported repository for source evidence')
            source['source'] = github_snapshot(match[1].removesuffix('.git'))
        else:
            final_url, body = get_url(url)
            source = dict(kind='page', url=final_url, bodySha256=hashlib.sha256(body).hexdigest())
        return dict(complete=True, fingerprint=digest(source), source=source)
    except Exception as exc:
        # Do not include headers or environment variables in persisted diagnostics.
        return dict(complete=False, error=f'{type(exc).__name__}: source snapshot unavailable')


def empty():
    return dict(version=VERSION, entries={})


def load(path=BASELINE):
    if not path.exists():
        return empty()
    data = json.loads(path.read_text())
    if data.get('version') != VERSION or not isinstance(data.get('entries'), dict):
        raise ValueError('Unsupported or malformed baseline; do not silently discard reviews')
    for row in data['entries'].values():
        if not isinstance(row, dict) or not all(k in row for k in ['claim', 'snapshot', 'reviewedAt', 'assessment']):
            raise ValueError('Malformed baseline entry')
        if row['assessment'].get('action') != 'keep' or not row['snapshot'].get('complete'):
            raise ValueError('Baseline contains an unresolved review')
    return data


def prepare(data, baseline, fetch=None):
    if fetch is None:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=4) as pool:
            observations = list(pool.map(snapshot, data['entries']))
    else:
        observations = [fetch(entry) for entry in data['entries']]
    selected, unchanged, pending, snapshots = [], [], [], {}
    for entry, current in zip(data['entries'], observations):
        identity = key(entry)
        if identity in snapshots:
            raise ValueError('Duplicate catalog URL in the same section')
        snapshots[identity] = current
        previous = baseline['entries'].get(identity)
        reason = ('fetch-incomplete' if not current['complete'] else
                  'not-reviewed' if not previous else
                  'catalog-changed' if previous['claim'] != claim(entry, data['contributionRules']) else
                  'source-changed' if previous['snapshot']['fingerprint'] != current['fingerprint'] else 'unchanged')
        item = dict(entry, changeReason=reason)
        if reason == 'unchanged':
            unchanged.append(item)
        elif reason == 'fetch-incomplete':
            pending.append(item)
        else:
            selected.append(item)
    data = dict(data, entries=selected, scannedEntries=data['entries'], snapshots=snapshots,
                baseline=baseline, unchangedEntries=unchanged, pendingEntries=pending)
    return data


def research_packet(data):
    return {k: data[k] for k in ['repository', 'catalogSha', 'contributionRules']} | {
        'entries': [dict(e, currentSnapshot=data['snapshots'][key(e)],
                         previousReview=data['baseline']['entries'].get(key(e))) for e in data['entries']]}


def advance(data, assessment, fetch=None):
    """Only verified keeps advance. Corrections and uncertainty remain pending.

    Re-fetch reviewed evidence to avoid acknowledging a change made during research.
    Existing unrelated baseline records are preserved when other entries are reviewed.
    """
    fetch = fetch or snapshot
    ci.validate(data, assessment)
    result = json.loads(json.dumps(data['baseline']))
    resolved, pending = [], [e['name'] for e in data['pendingEntries']]
    entries = {e['id']: e for e in data['entries']}
    for row in assessment['results']:
        entry = entries[row['id']]
        current = data['snapshots'][key(entry)]
        if row['action'] != 'keep' or row['blockers'] or not current['complete']:
            pending.append(entry['name'])
            continue
        after = fetch(entry)
        if not after['complete'] or after['fingerprint'] != current['fingerprint']:
            pending.append(entry['name'])
            continue
        result['entries'][key(entry)] = dict(name=entry['name'], url=entry['url'], section=entry['section'],
            claim=claim(entry, data['contributionRules']), snapshot=current,
            reviewedAt=datetime.now(timezone.utc).isoformat(), assessment=row)
        resolved.append(entry['name'])
    return result, dict(resolved=resolved, pending=pending)


def inventory(repo, output):
    """Build an evidence inventory without calling a model or approving entries."""
    from concurrent.futures import ThreadPoolExecutor
    data = ci.packet(repo)
    with ThreadPoolExecutor(max_workers=4) as pool:
        snapshots = list(pool.map(snapshot, data['entries']))
    result = dict(version=VERSION, catalogSha=data['catalogSha'],
                  observedAt=datetime.now(timezone.utc).isoformat(), reviewed=False,
                  entries=[dict(name=e['name'], url=e['url'], section=e['section'],
                                claim=claim(e, data['contributionRules']), snapshot=s)
                           for e,s in zip(data['entries'], snapshots)])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(entries=len(snapshots), complete=sum(s['complete'] for s in snapshots),
                          pending=sum(not s['complete'] for s in snapshots), modelCalls=0)))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('.um/freshness/work/inventory.json'))
    args = parser.parse_args()
    inventory(Path.cwd(), args.output)
