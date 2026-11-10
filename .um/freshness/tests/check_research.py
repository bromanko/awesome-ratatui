"""Verify actual UM batch exports with deterministic commands, without model calls."""
from pathlib import Path
import json
import os
import shutil
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import research

source=Path(__file__).resolve().parents[1]
original=Path.cwd()
with tempfile.TemporaryDirectory(prefix='freshness-batch-contract-') as folder:
    root=Path(folder)/'.um/freshness';root.mkdir(parents=True)
    shutil.copytree(source/'schemas',root/'schemas')
    (root/'fixture.py').write_text('''from pathlib import Path
import json,os
packet=json.loads((Path(os.environ['UM_STEP_INPUTS'])/'values/research').read_text())
rows=[dict(id=e['id'],action='keep',reason='Synthetic contract check.',evidence=[dict(url='https://example.com',observation='Synthetic.')],limitations=[],blockers=[],newName=None,newUrl=None,newDescription=None) for e in packet['entries']]
Path('.um/freshness/assessment.json').write_text(json.dumps(dict(results=rows)))
''')
    (root/'research-batch.yaml').write_text('''schemaVersion: 1
inputs:
  research:
    kind: text
steps:
  assess:
    kind: cmd
    inputs:
      research:
        ref: inputs.research
    command:
      argv: [python3, .um/freshness/fixture.py]
    outputs:
      assessment:
        kind: json
        from: path
        path: .um/freshness/assessment.json
        schema: schemas/assessment.json
exports:
  assessment:
    ref: outputs.assess.assessment
''')
    try:
        os.chdir(folder)
        packet=dict(repository='example/catalog',catalogSha='a'*40,contributionRules='Rules',entries=[dict(id=str(i)) for i in range(41)])
        result,receipt=research.investigate(packet)
        assert [r['id'] for r in result['results']]==[str(i) for i in range(41)]
        assert [len(r['entryIds']) for r in receipt['batches']]==[20,20,1]
        print('Native UM batch exports: 41 entries, three batches, complete coverage, no model calls.')
    finally:os.chdir(original)
