#!/usr/bin/env python3
"""Select a pinned catalog slice and render an advisory report. No GitHub writes."""
import argparse
import base64
import difflib
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess

UPSTREAM = 'ratatui/awesome-ratatui'
ENTRY = re.compile(r'^- \[([^]]+)\]\((https?://[^)]+)\) - (.+)$')


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True)


def entries(readme):
    result, section = [], ''
    for line_number, line in enumerate(readme.splitlines(), 1):
        if line.startswith('#'):
            section = line.lstrip('# ').strip()
        match = ENTRY.fullmatch(line)
        if match:
            name, url, description = match.groups()
            result.append(dict(id=str(line_number), name=name, url=url,
                               description=description, section=section, line=line))
        elif line.startswith('- [') and ' - ' in line:
            raise ValueError(f'Unrecognized catalog entry at line {line_number}')
    if not result:
        raise ValueError('No catalog entries found')
    return result


def packet(repo, index):
    if type(index) is not int or index < 0:
        raise ValueError('Slice must be a nonnegative integer')
    sha = git(repo, 'rev-parse', 'HEAD').strip()
    readme = git(repo, 'show', f'{sha}:README.md')
    rules = git(repo, 'show', f'{sha}:contributing.md')
    catalog = entries(readme)
    selected = catalog[index * 3:(index + 1) * 3]
    if not selected:
        raise ValueError(f'Slice out of range: choose 0–{(len(catalog)-1)//3}')
    return dict(repository=UPSTREAM, catalogSha=sha,
                readmeHash=hashlib.sha256(readme.encode()).hexdigest(),
                slice=index, sliceCount=(len(catalog)+2)//3,
                entries=selected, readme=readme, contributionRules=rules)


def freshness(data):
    try:
        content = json.loads(subprocess.check_output(
            ['gh', 'api', f'repos/{UPSTREAM}/contents/README.md?ref=main'],
            text=True, stderr=subprocess.PIPE, timeout=30))
        current = base64.b64decode(content['content'], validate=False)
        return ('unchanged' if hashlib.sha256(current).hexdigest() == data['readmeHash']
                else 'changed — review against the latest catalog before acting')
    except (subprocess.SubprocessError, KeyError, ValueError, OSError):
        return 'unverified — could not recheck the current catalog'


def validate(data, raw):
    expected = {entry['id'] for entry in data['entries']}
    results = raw.get('results')
    if not isinstance(results, list) or len(results) != len(expected):
        raise ValueError('Assessment must cover every selected entry exactly once')
    seen = set()
    for row in results:
        if row['id'] not in expected or row['id'] in seen:
            raise ValueError('Unexpected or duplicate entry id')
        seen.add(row['id'])
        if row['action'] not in {'keep', 'update', 'replace', 'remove', 'uncertain'}:
            raise ValueError('Invalid action')
        if not isinstance(row['reason'], str) or not row['reason'].strip():
            raise ValueError('Missing reason')
        if not isinstance(row['limitations'], list) or any(not isinstance(x, str) for x in row['limitations']):
            raise ValueError('Invalid limitations')
        if not isinstance(row['evidence'], list):
            raise ValueError('Invalid evidence')
        for source in row['evidence']:
            if not re.fullmatch(r'https?://[^\s]+', source['url']) or not isinstance(source['observation'], str):
                raise ValueError('Invalid evidence source')
        if row['action'] != 'uncertain' and not row['evidence']:
            raise ValueError('A factual conclusion requires evidence')
        for key in ['newUrl', 'newDescription']:
            if row[key] is not None and not isinstance(row[key], str):
                raise ValueError('Invalid proposed correction')
        if row['action'] not in {'update', 'replace'} and any(row[k] is not None for k in ['newUrl', 'newDescription']):
            raise ValueError('Unexpected proposed correction')
        if row['action'] in {'update', 'replace'} and not (row['newUrl'] or row['newDescription']):
            raise ValueError('Missing proposed correction')
        if row['newUrl'] and not re.fullmatch(r'https?://[^\s]+', row['newUrl']):
            raise ValueError('Invalid proposed URL')
    return results


def render(data, raw, status):
    results = validate(data, raw)
    names = {entry['id']: entry['name'] for entry in data['entries']}
    lines = ['# Freshness research', '', 'Advisory only; every suggested change requires maintainer review.',
             'No list edits, PRs, comments, or reviews were submitted.', '',
             f"Catalog revision: `{data['catalogSha']}`",
             f"Slice: {data['slice']} of {data['sliceCount']} (zero-based)",
             'Catalog recheck: ' + status, '',
             'Sources below are agent-reported observations, not independent verification.', '']
    # Treat source/model strings as plain text, preventing injected Markdown/HTML.
    for row in results:
        lines += ['## Entry ' + row['id'], '', '<pre>' + html.escape(
            names[row['id']] + '\n\n' + row['reason'] + '\n\n' +
            '\n'.join(s['url'] + '\n' + s['observation'] for s in row['evidence']) +
            '\n\nUnresolved questions:\n' + ('\n'.join(row['limitations']) or 'None reported.') +
            '\n\nRecommendation: ' + row['action'] +
            '\nProposed URL: ' + (row['newUrl'] or 'None') +
            '\nProposed description: ' + (row['newDescription'] or 'None')) + '</pre>', '']
    return '\n'.join(lines)



def previews(data, raw, status):
    """Build one reviewable proposal per entry; never alter the checkout."""
    results = validate(data, raw)
    if status != 'unchanged':
        return [], 'Preview withheld: catalog freshness could not be confirmed.'
    readme = data['readme']
    if hashlib.sha256(readme.encode()).hexdigest() != data['readmeHash']:
        raise ValueError('Catalog content/hash mismatch')
    selected = {entry['id']: entry for entry in data['entries']}
    proposals = []
    held = 0
    for row in results:
        if row['action'] not in {'update', 'replace', 'remove'}:
            continue
        if row['limitations']:
            held += 1
            continue
        entry = selected[row['id']]
        lines = readme.splitlines(keepends=True)
        offset = int(entry['id']) - 1
        if offset < 0 or offset >= len(lines) or lines[offset].rstrip('\r\n') != entry['line']:
            raise ValueError('Selected entry no longer matches its pinned line')
        if row['action'] == 'remove':
            del lines[offset]
        else:
            url = row['newUrl'] or entry['url']
            description = row['newDescription'] or entry['description']
            if any(c in url for c in '()<>\r\n') or any(c in description for c in '\r\n'):
                raise ValueError('Correction must be a single well-formed Markdown entry')
            if not description.strip() or description != description.strip():
                raise ValueError('Correction description must be nonempty and trimmed')
            ending = '\r\n' if lines[offset].endswith('\r\n') else '\n' if lines[offset].endswith('\n') else ''
            lines[offset] = f"- [{entry['name']}]({url}) - {description}" + ending
        updated = ''.join(lines)
        if updated == readme:
            continue
        diff = ''.join(difflib.unified_diff(readme.splitlines(keepends=True),
                       updated.splitlines(keepends=True), fromfile='a/README.md', tofile='b/README.md'))
        title = f"{row['action'].capitalize()} {entry['name']} entry"
        body = (row['reason'] + '\n\nEvidence:\n' +
                '\n'.join(source['url'] + ' — ' + source['observation'] for source in row['evidence']) +
                f"\n\nBased on catalog revision {data['catalogSha']}.\n"
                'Proposed by an automated freshness review. A maintainer must verify the evidence and edit.\n'
                'This preview has not run the full catalog lint or link checks.\n')
        proposals.append(dict(id=entry['id'], title=title, body=body, patch=diff))
    note = f'{len(proposals)} proposed change(s); {held} held for unresolved questions.'
    return proposals, note


def write_report(data, raw, status, output, demo=False):
    report = render(data, raw, status)
    proposals, note = previews(data, raw, status)
    if demo:
        report = '# Example preview — synthetic test data\n\nNot a live finding or a proposed change to the real catalog.\n\n' + report
    report += '\n\n# Proposed pull requests\n\n' + note + '\n'
    output.mkdir(parents=True, exist_ok=True)
    # Clear previous proposals so retries cannot publish obsolete artifacts.
    for old in output.glob('entry-*.*'):
        old.unlink()
    for proposal in proposals:
        stem = 'entry-' + proposal['id']
        (output / (stem + '.patch')).write_text(proposal['patch'])
        (output / (stem + '.md')).write_text('# ' + proposal['title'] + '\n\n' + proposal['body'])
        report += ('\n## ' + stem + '\n\n<pre>' + html.escape(proposal['title'] + '\n\n' + proposal['body']) + '</pre>\n\n')
        # A fence longer than any run of backticks keeps all patch text literal.
        fence = '`' * max(3, 1 + max([len(x) for x in re.findall(r'`+', proposal['patch'])] or [0]))
        report += fence + 'diff\n' + proposal['patch'] + fence + '\n'
    (output / 'report.md').write_text(report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    pre = subs.add_parser('prepare')
    pre.add_argument('--repo', type=Path, required=True)
    pre.add_argument('--slice', type=int, required=True)
    pre.add_argument('--output', type=Path, required=True)
    post = subs.add_parser('finish')
    post.add_argument('--input-dir', type=Path, required=True)
    post.add_argument('--assessment', type=Path, required=True)
    post.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'prepare':
        data = packet(args.repo, args.slice)
        encoded = json.dumps(data, ensure_ascii=False, indent=2)
        if len(encoded.encode()) > 512 * 1024:
            raise ValueError('Catalog packet exceeds 512 KiB')
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'packet.json').write_text(encoded + '\n')
        print(f"Prepared slice {data['slice']} of {data['sliceCount']} at {data['catalogSha']}")
    else:
        data = json.loads((args.input_dir / 'packet.json').read_text())
        if args.assessment.stat().st_size > 65536:
            raise ValueError('Assessment exceeds 64 KiB')
        raw = json.loads(args.assessment.read_text())
        write_report(data, raw, freshness(data), args.output)


if __name__ == '__main__':
    main()
