#!/usr/bin/env python3
"""UM command stages. Every handoff is read from UM_STEP_INPUTS."""
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile
import ci
import history
import checks
import catalog
import subprocess
import research

WORK = Path('.um/freshness/work')


def value(name):
    return (Path(os.environ['UM_STEP_INPUTS']) / 'values' / name).read_text()


def obj(name):
    return json.loads(value(name))


def save(name, data):
    WORK.mkdir(parents=True,exist_ok=True)
    (WORK/name).write_text(json.dumps(data,indent=2)+'\n')


def main(stage):
    if stage == 'prepare':
        if WORK.exists(): shutil.rmtree(WORK)
        data = ci.packet(Path.cwd())
        data = catalog.prepare(data, catalog.load())
        save('decision.json', dict(needsResearch=bool(data['entries'])))
        save('research.json', catalog.research_packet(data))
        if len(json.dumps(data).encode()) > 16 * 1024 * 1024:
            raise ValueError('Catalog packet exceeds 16 MiB')
        save('catalog.json',data)
    elif stage == 'investigateEntries':
        assessment, receipt = research.investigate(obj('research'))
        save('assessment.json', assessment)
        save('research-model-receipt.json', receipt)
    elif stage == 'collectHistory':
        data, assessment = obj('catalog'), obj('assessment')
        ci.validate(data,assessment)
        collected = history.collect(data,assessment)
        save('history.json',collected)
    elif stage == 'reviewHistory':
        collected = obj('history')
        save('history-model-receipt.json', {})
        # An empty review returns without starting Claude. UM 0.72.1 cannot bind an
        # optional skipped output, so this stage always produces the typed review.
        if not collected['candidates']:
            reviewed = dict(reviews=[])
        else:
            root = Path('.um/freshness')
            schema = json.loads((root/'schemas/history.json').read_text())
            schema.pop('$schema', None)  # Claude's schema validator uses its own dialect.
            command = ['claude', '-p', '--model', 'claude-opus-5-5', '--effort', 'medium',
                       '--output-format', 'json', '--json-schema', json.dumps(schema),
                       '--system-prompt', (root/'prompts/history.md').read_text(),
                       '--tools', '', '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
                       '--setting-sources', '', '--no-session-persistence']
            result = subprocess.run(command, input=json.dumps(collected), capture_output=True,
                                    text=True, timeout=600, check=True)
            response = json.loads(result.stdout)
            if response.get('is_error') or not isinstance(response.get('structured_output'), dict):
                raise ValueError('History model did not return a successful structured review')
            reviewed = response['structured_output']
            save('history-model-receipt.json', {k:response.get(k) for k in
                 ['modelUsage','total_cost_usd','duration_ms','num_turns']})
        save('review.json', reviewed)
    elif stage == 'buildCorrections':
        data, assessment, collected, reviewed = (obj(n) for n in ('catalog','assessment','history','review'))
        if collected['catalogSha'] != data['catalogSha']:
            raise ValueError('History and catalog identities differ')
        expected = {c['id'] for c in collected['candidates']}
        actual = [c['id'] for c in reviewed['reviews']]
        if len(actual) != len(set(actual)) or set(actual) != expected:
            raise ValueError('History review does not cover candidates exactly once')
        status = ci.freshness(data)
        proposals, note = ci.previews(data,assessment,status)
        save('corrections.json',dict(catalog=data, assessment=assessment, history=collected,
             review=reviewed, status=status, proposals=proposals, note=note, historyUsage=obj('historyUsage'), researchUsage=obj('researchUsage')))
    elif stage == 'validateCorrections':
        bundle = obj('corrections')
        log_dir = WORK/'checks'
        bundle['evaluations'] = {}
        if bundle['proposals']:
            validator = checks.Validator(Path.cwd(),bundle['catalog']['catalogSha'],bundle['catalog']['readme'],log_dir)
            try:
                bundle['evaluations'] = ci.evaluate_proposals(bundle['catalog'],bundle['proposals'],
                    bundle['history'],bundle['review'],validator,ci.freshness)
            finally:
                validator.close()
        # Validation logs travel with the declared output, not as an implicit handoff.
        bundle['logs'] = {p.relative_to(log_dir).as_posix():p.read_text()
                          for p in log_dir.rglob('*.json')} if log_dir.exists() else {}
        save('validated.json',bundle)
    elif stage in {'renderPreview', 'renderUnchanged'}:
        if stage == 'renderPreview':
            bundle = obj('validated')
        else:
            data = obj('catalog')
            assessment = dict(results=[])
            bundle = dict(catalog=data, assessment=assessment, status=ci.freshness(data),
                          proposals=[], note='No correction candidates.', evaluations={}, logs={})
        output = WORK/'preview'
        if output.exists(): shutil.rmtree(output)
        baseline, progress = catalog.advance(bundle['catalog'], bundle['assessment'])
        if progress['resolved']:
            bundle['status'] = ci.freshness(bundle['catalog'])
        if bundle['status'] != 'unchanged':
            baseline = bundle['catalog']['baseline']
            progress['pending'] += progress['resolved']
            progress['resolved'] = []
            for evaluation in bundle['evaluations'].values():
                evaluation.update(ready=False, note='Catalog freshness changed or could not be verified before export.')
        ci.write_report(bundle['catalog'],bundle['assessment'],bundle['status'],output,
                        prepared=(bundle['proposals'],bundle['note']),evaluations=bundle['evaluations'],progress=progress)
        (output/'baseline.json').write_text(json.dumps(baseline, indent=2)+'\n')
        if bundle.get('researchUsage'):
            (output/'research-model-receipt.json').write_text(json.dumps(bundle['researchUsage'], indent=2)+'\n')
        if bundle.get('historyUsage'):
            (output/'history-model-receipt.json').write_text(json.dumps(bundle['historyUsage'], indent=2)+'\n')
        for name, content in bundle['logs'].items():
            path = Path(name)
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('Invalid validation log path')
            target = output/path
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(content)
        with zipfile.ZipFile(WORK/'proposals.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(output.rglob('*')):
                if path.is_file(): archive.write(path,path.relative_to(output))
    else:
        raise ValueError('Unknown workflow stage')


if __name__ == '__main__': main(sys.argv[1])
