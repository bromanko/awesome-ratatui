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
        data = ci.packet(Path.cwd(),int(value('slice')))
        if len(json.dumps(data).encode()) > 512 * 1024:
            raise ValueError('Catalog packet exceeds 512 KiB')
        save('catalog.json',data)
    elif stage == 'collectHistory':
        data, assessment = obj('catalog'), obj('assessment')
        ci.validate(data,assessment)
        collected = history.collect(data,assessment)
        save('history.json',collected)
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
             review=reviewed, status=status, proposals=proposals, note=note))
    elif stage == 'validateCorrections':
        bundle = obj('corrections')
        log_dir = WORK/'checks'
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
    elif stage == 'renderPreview':
        bundle = obj('validated')
        output = WORK/'preview'
        if output.exists(): shutil.rmtree(output)
        ci.write_report(bundle['catalog'],bundle['assessment'],bundle['status'],output,
                        prepared=(bundle['proposals'],bundle['note']),evaluations=bundle['evaluations'])
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
