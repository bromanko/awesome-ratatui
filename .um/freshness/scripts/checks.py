"""Validate one-entry patches in disposable copies using the upstream check tools."""
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile


def run(command, cwd, env, timeout=180):
    try:
        result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout)
        return dict(exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr)
    except (OSError, subprocess.TimeoutExpired) as error:
        return dict(exitCode=-1, stdout='', stderr=type(error).__name__ + ': ' + str(error))


def links(result, root):
    if result['exitCode'] not in {0,2}:
        raise ValueError('Link checker did not complete')
    data = json.loads(result['stdout'])
    if data.get('total', 0) == 0 or data.get('unknown', 0):
        raise ValueError('Empty/incomplete link check')
    def urls(key):
        return {row['url'].replace(root.as_uri(), 'file://CATALOG')
                for rows in data.get(key, {}).values() for row in rows}
    errors = urls('error_map') | urls('timeout_map')
    if (data.get('errors',0) or data.get('timeouts',0)) and not errors:
        raise ValueError('Missing link failure details')
    return dict(errors=sorted(errors), excluded=sorted(urls('excluded_map')),
                successful=sorted(urls('success_map')), total=data['total'])


def compare_links(before, after, relevant):
    inherited = set(before['errors']) & set(after['errors'])
    introduced = set(after['errors']) - set(before['errors'])
    affected = set(relevant) & (set(after['errors']) | set(after['excluded']))
    return dict(passed=not (introduced or affected), introduced=sorted(introduced),
                preexisting=sorted(inherited), affected=sorted(affected))


class Validator:
    def __init__(self, repo, sha, readme, output):
        self.repo, self.sha, self.readme, self.output = repo.resolve(), sha, readme, output
        self.temp = tempfile.TemporaryDirectory(prefix='freshness-checks-')
        self.root = Path(self.temp.name)
        self.env = {k: os.environ[k] for k in ('PATH','LANG','SSL_CERT_FILE','NIX_SSL_CERT_FILE') if k in os.environ}
        self.env.update(HOME=str(self.root), GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
        if os.environ.get('GH_TOKEN'):
            self.env['github_token'] = os.environ['GH_TOKEN']
            self.env['GITHUB_TOKEN'] = os.environ['GH_TOKEN']
        self.archive = subprocess.check_output(['git','-C',str(self.repo),'archive',sha])
        self.before = None

    def close(self):
        self.temp.cleanup()

    def checkout(self, name):
        folder = self.root / name
        folder.mkdir()
        with tarfile.open(fileobj=io.BytesIO(self.archive)) as archive:
            archive.extractall(folder, filter='data')
        if (folder/'README.md').read_text() != self.readme:
            raise ValueError('Validation snapshot does not match research packet')
        for command in [['git','init','-q','--initial-branch=main'],
                        ['git','config','remote.origin.url','https://github.com/ratatui/awesome-ratatui.git'],
                        ['git','config','branch.main.remote','origin']]:
            if run(command,folder,self.env)['exitCode'] != 0: raise ValueError('Cannot initialize validation checkout')
        return folder

    def check(self, folder, label):
        commands = {'lint':['awesome-lint','README.md'], 'spelling':['typos','--config','typos.toml','README.md'],
                    'links':['lychee','--no-progress','--format','json','--max-retries','0',
                             '--max-concurrency','10','--timeout','10','README.md']}
        results = {key:run(cmd,folder,self.env) for key,cmd in commands.items()}
        log = self.output / 'validation'
        log.mkdir(parents=True,exist_ok=True)
        (log/(label+'.json')).write_text(json.dumps(results,indent=2)+'\n')
        return results

    def validate(self, proposal, entry):
        if self.before is None:
            self.base = self.checkout('baseline')
            self.before = self.check(self.base,'baseline')
        folder = self.checkout('entry-'+proposal['id'])
        patch = self.root / ('entry-'+proposal['id']+'.patch')
        patch.write_text(proposal['patch'])
        for command in [['git','apply','--check',str(patch)],['git','apply',str(patch)]]:
            result = run(command,folder,self.env)
            if result['exitCode'] != 0:
                return dict(passed=False, reason='Patch does not apply to the pinned catalog.', patch=result)
        # Verify only the exact intended README change occurred.
        changed = (folder/'README.md').read_text()
        import ci
        expected = ''.join(__import__('difflib').unified_diff(self.readme.splitlines(True),changed.splitlines(True),
                           fromfile='a/README.md',tofile='b/README.md'))
        if expected != proposal['patch']:
            return dict(passed=False,reason='Applied change differs from proposed patch.')
        after = self.check(folder,'entry-'+proposal['id'])
        result = dict(passed=False, baseline={k:v['exitCode'] for k,v in self.before.items()},
                      patched={k:v['exitCode'] for k,v in after.items()})
        try:
            before_links = links(self.before['links'],self.base)
            after_links = links(after['links'],folder)
            relevant = [e['url'] for e in ci.entries(changed) if e['name'] == entry['name']]
            result['links'] = compare_links(before_links,after_links,relevant)
            result['passed'] = all(after[k]['exitCode']==0 for k in ('lint','spelling')) and result['links']['passed']
            result['reason'] = ('Checks passed; existing unrelated link failures are listed separately.' if result['passed']
                                else 'Proposed edit failed checks; held for maintainer review. See validation logs.')
        except (ValueError,KeyError,TypeError):
            result['reason'] = 'Link validation incomplete; held for maintainer review.'
        return result
