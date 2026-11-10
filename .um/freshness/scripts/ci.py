#!/usr/bin/env python3
"""Select a pinned catalog slice and render an advisory report. No GitHub writes."""
import base64
import difflib
import hashlib
import html
import json
import history
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
        content = history.api(f'repos/{UPSTREAM}/contents/README.md', ref='main')
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
        if not isinstance(row.get('blockers'), list) or any(not isinstance(x, str) or not x.strip() for x in row['blockers']):
            raise ValueError('Missing or invalid proposal blockers')
        for key in ['newName', 'newUrl', 'newDescription']:
            if row[key] is not None and not isinstance(row[key], str):
                raise ValueError('Invalid proposed correction')
        if row['action'] not in {'update', 'replace'} and any(row[k] is not None for k in ['newName', 'newUrl', 'newDescription']):
            raise ValueError('Unexpected proposed correction')
        if row['action'] in {'update', 'replace'} and not (row['newName'] or row['newUrl'] or row['newDescription']):
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
            '\n\nBlocking uncertainties:\n' + ('\n'.join(row['blockers']) or 'None reported.') +
            '\n\nInformational caveats:\n' + ('\n'.join(row['limitations']) or 'None reported.') +
            '\n\nRecommendation: ' + row['action'] +
            '\nProposed name: ' + (row['newName'] or 'None') + '\nProposed URL: ' + (row['newUrl'] or 'None') +
            '\nProposed description: ' + (row['newDescription'] or 'None')) + '</pre>', '']
    return '\n'.join(lines)



def patch_text(before, after):
    chunks = difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                 fromfile='a/README.md', tofile='b/README.md')
    return ''.join(line if line.endswith('\n') else line + '\n\\ No newline at end of file\n' for line in chunks)


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
        if row['blockers']:
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
            name = row['newName'] or entry['name']
            if not name.strip() or name != name.strip() or any(c in name for c in '[]()<>\r\n\t'):
                raise ValueError('Invalid entry name')
            url = row['newUrl'] or entry['url']
            description = row['newDescription'] or entry['description']
            if any(c in url for c in '()<>\r\n') or any(c in description for c in '\r\n'):
                raise ValueError('Correction must be a single well-formed Markdown entry')
            if not description.strip() or description != description.strip():
                raise ValueError('Correction description must be nonempty and trimmed')
            ending = '\r\n' if lines[offset].endswith('\r\n') else '\n' if lines[offset].endswith('\n') else ''
            replacement = f"- [{name}]({url}) - {description}" + ending
            if name != entry['name']:
                start, end = offset, offset + 1
                while start > 0 and ENTRY.fullmatch(lines[start-1].rstrip('\r\n')): start -= 1
                while end < len(lines) and ENTRY.fullmatch(lines[end].rstrip('\r\n')): end += 1
                peers = [ENTRY.fullmatch(lines[i].rstrip('\r\n')).group(1) for i in range(start,end) if i != offset]
                if name.casefold() in [n.casefold() for n in peers]:
                    raise ValueError('Rename would duplicate an entry name')
                endings = ['\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else '' for line in lines[start:end]]
                del lines[offset]
                position = next((i for i in range(start,end-1) if ENTRY.fullmatch(lines[i].rstrip('\r\n')).group(1).casefold() > name.casefold()),end-1)
                lines.insert(position,replacement)
                lines[start:end] = [line.rstrip('\r\n') + ending for line, ending in zip(lines[start:end],endings)]
            else:
                lines[offset] = replacement
        updated = ''.join(lines)
        if updated == readme:
            continue
        diff = patch_text(readme,updated)
        title = f"{row['action'].capitalize()} {entry['name']} entry"
        body = (row['reason'] + '\n\nEvidence:\n' +
                '\n'.join(source['url'] + ' — ' + source['observation'] for source in row['evidence']) +
                '\n\nInformational caveats:\n' + ('\n'.join(row['limitations']) or 'None.') +
                f"\n\nBased on catalog revision {data['catalogSha']}.\n"
                'Proposed by an automated freshness review. A maintainer must verify the evidence and edit.\n'
                'Validation and discussion checks are recorded below.\n')
        proposals.append(dict(id=entry['id'], title=title, body=body, patch=diff))
    note = f'{len(proposals)} proposed change(s); {held} held for unresolved questions.'
    return proposals, note


def evaluate_proposals(data, proposals, history_packet, history_review, validator, current_check):
    candidates = {c['id']: c for c in history_packet['candidates']}
    reviews = {c['id']: c for c in history_review['reviews']}
    if len(reviews) != len(history_review['reviews']) or set(reviews) != set(candidates):
        raise ValueError('History assessment must cover every candidate exactly once')
    rows = {e['id']: e for e in data['entries']}
    results = {}
    for proposal in proposals:
        candidate = candidates.get(proposal['id'])
        allowed, note = (history.gate(candidate, reviews.get(proposal['id'])) if candidate
                         else (False, 'History check not performed.'))
        validation = (validator.validate(proposal, rows[proposal['id']]) if allowed
                      else dict(passed=False, reason='Validation not run; history review must pass first.'))
        ready = allowed and validation['passed']
        if ready and current_check(data) != 'unchanged':
            ready = False
            validation.update(passed=False, reason='Catalog changed or could not be rechecked after validation.')
        results[proposal['id']] = dict(ready=ready, note=note, history=candidate,
                                      assessment=reviews.get(proposal['id']), validation=validation)
    return results


def write_report(data, raw, status, output, demo=False, prepared=None, evaluations=None):
    report = render(data, raw, status)
    proposals, note = prepared if prepared is not None else previews(data, raw, status)
    if demo:
        report = '# Example preview — synthetic test data\n\nNot a live finding or a proposed change to the real catalog.\n\n' + report
    report += '\n\n# Proposed pull requests\n\n' + note + '\n'
    output.mkdir(parents=True, exist_ok=True)
    # Clear previous proposals so retries cannot publish obsolete artifacts.
    for old in output.glob('entry-*.*'):
        old.unlink()
    for original in proposals:
        proposal = dict(original)
        result = (evaluations or {}).get(proposal['id'], dict(ready=False, note='History check not performed.',
                       history=None, assessment=None, validation=dict(passed=False,reason='Checks not performed.')))
        ready, history_note = result['ready'], result['note']
        candidate, validation = result['history'], result['validation']
        (output / ('entry-' + proposal['id'] + '.checks.json')).write_text(json.dumps(result,indent=2)+'\n')
        proposal['body'] += ('\nReview status: ' + ('Ready for maintainer review' if ready else 'Held') +
                             '\nPrior discussion: ' + history_note + '\nValidation: ' + validation['reason'] + '\n')
        report += '\n### ' + ('Ready for maintainer review' if ready else 'Held') + '\n'
        report += '<pre>' + html.escape(history_note + '\n' + json.dumps(validation,indent=2)) + '</pre>\n'
        if candidate:
            report += '<pre>' + html.escape('Searches:\n' + '\n'.join(candidate['queries']) +
                        '\nReferences:\n' + '\n'.join((result['assessment'] or {}).get('references',[]))) + '</pre>\n'
        stem = 'entry-' + proposal['id']
        if ready:
            (output / (stem + '.patch')).write_text(proposal['patch'])
        (output / (stem + '.md')).write_text('# ' + proposal['title'] + '\n\n' + proposal['body'])
        report += ('\n## ' + stem + '\n\n<pre>' + html.escape(proposal['title'] + '\n\n' + proposal['body']) + '</pre>\n\n')
        # A fence longer than any run of backticks keeps all patch text literal.
        fence = '`' * max(3, 1 + max([len(x) for x in re.findall(r'`+', proposal['patch'])] or [0]))
        report += fence + 'diff\n' + proposal['patch'] + fence + '\n'
    (output / 'report.md').write_text(report)
