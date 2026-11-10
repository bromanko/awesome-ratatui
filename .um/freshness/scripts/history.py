"""Bounded read-only collection and consistency checks for prior discussions."""
import json
import os
from pathlib import Path
import subprocess
import re

REPOSITORIES = ['ratatui/awesome-ratatui']


def api(path, **fields):
    command = ['gh', 'api', '--method', 'GET', path]
    for key, value in fields.items():
        command += ['-f', f'{key}={value}']
    env = dict(os.environ)
    if env.get('FRESHNESS_GITHUB_TOKEN'):
        env['GH_TOKEN'] = env['FRESHNESS_GITHUB_TOKEN']
    return json.loads(subprocess.check_output(command, env=env, text=True, stderr=subprocess.PIPE, timeout=30))


def listing(path):
    # Detect truncation rather than declaring a partial history complete.
    rows = api(path, per_page=100)
    if not isinstance(rows, list) or len(rows) >= 100:
        raise ValueError('History detail list too large or malformed')
    return rows


def record(repo, item):
    number = item['number']
    issue = api(f'repos/{repo}/issues/{number}')
    result = {k: issue.get(k) for k in ['number', 'html_url', 'title', 'body', 'state', 'state_reason', 'user']}
    result['comments'] = listing(f'repos/{repo}/issues/{number}/comments')
    if 'pull_request' in item:
        pr = api(f'repos/{repo}/pulls/{number}')
        result['pullRequest'] = {k: pr.get(k) for k in ['merged_at', 'state', 'head', 'base']}
        result['files'] = listing(f'repos/{repo}/pulls/{number}/files')
        result['reviews'] = listing(f'repos/{repo}/pulls/{number}/reviews')
        result['reviewComments'] = listing(f'repos/{repo}/pulls/{number}/comments')
        if any(f.get('status') != 'removed' and 'patch' not in f for f in result['files']):
            raise ValueError('PR diff unavailable or truncated')
    # Do not pass unnecessary account metadata to the model.
    def compact(value):
        if isinstance(value, list): return [compact(v) for v in value]
        if isinstance(value, dict):
            return {k: compact(v) for k, v in value.items() if k in {
                'number','html_url','title','body','state','state_reason','user','login',
                'author_association','created_at','updated_at','comments','pullRequest',
                'merged_at','files','filename','status','patch','reviews','reviewComments'}}
        return value
    return compact(result)


def collect(data, raw):
    repos = list(REPOSITORIES)
    fork = os.environ.get('FRESHNESS_REPOSITORY', os.environ.get('GITHUB_REPOSITORY', ''))
    if re.fullmatch(r'[A-Za-z0-9_.-]+/awesome-ratatui', fork) and fork not in repos:
        repos.append(fork)
    selected = {e['id']: e for e in data['entries']}
    candidates = []
    for row in raw['results']:
        if row['action'] not in {'update','replace','remove'} or row['limitations']:
            continue
        entry = selected[row['id']]
        candidate = dict(id=row['id'], entry=entry, proposal=row, queries=[], records=[], complete=True, errors=[])
        matches = {}
        for repo in repos:
            for term in dict.fromkeys([entry['name'], entry['url']] + ([row['newUrl']] if row['newUrl'] else [])):
                query = f'repo:{repo} "{term.replace(chr(34), " ")}" in:title,body,comments'
                candidate['queries'].append(query)
                try:
                    response = api('search/issues', q=query, per_page=30)
                    if response.get('incomplete_results') or response['total_count'] > 30:
                        raise ValueError('Search incomplete or more than 30 matches')
                    for item in response['items']:
                        matches[(repo,item['number'])] = item
                except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
                    candidate['complete'] = False
                    candidate['errors'].append(f'Search unavailable/incomplete: {query} ({type(error).__name__})')
        if len(matches) > 10:
            candidate['complete'] = False
            candidate['errors'].append('More than 10 matching discussions; manual review needed.')
        for (repo, _), item in list(matches.items())[:10]:
            try:
                detail = record(repo, item)
                if len(json.dumps(detail).encode()) > 48000:
                    raise ValueError('Discussion exceeds evidence limit')
                candidate['records'].append(detail)
            except (ValueError, KeyError, OSError, subprocess.SubprocessError):
                candidate['complete'] = False
                candidate['errors'].append(f"Could not read complete discussion: {item['html_url']}")
        candidates.append(candidate)
    packet = dict(catalogSha=data['catalogSha'], candidates=candidates)
    if len(json.dumps(packet).encode()) > 400000:
        for candidate in candidates:
            candidate.update(complete=False, records=[], errors=['Combined history exceeds evidence limit.'])
    return packet


def gate(candidate, review):
    if not candidate['complete']:
        return False, 'History search incomplete: ' + '; '.join(candidate['errors'])
    if not review or review.get('id') != candidate['id']:
        return False, 'History assessment unavailable.'
    urls = set()
    def visit(value):
        if isinstance(value, dict):
            if 'html_url' in value: urls.add(value['html_url'])
            for v in value.values(): visit(v)
        elif isinstance(value, list):
            for v in value: visit(v)
    visit(candidate['records'])
    status = review.get('status')
    refs = review.get('references', [])
    if status not in {'clear','related','duplicate','rejected','obsolete','incomplete'}:
        return False, 'Invalid history assessment.'
    if any(ref not in urls for ref in refs) or (status in {'related','duplicate','rejected','obsolete'} and not refs):
        return False, 'History assessment lacks matching collected references.'
    return status in {'clear','related'}, status + ': ' + review.get('reason','')
