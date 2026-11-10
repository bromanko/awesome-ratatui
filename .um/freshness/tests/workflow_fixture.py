"""Exercise the real conditional UM graph with synthetic agent/network/check results."""
from pathlib import Path
import re
import sys
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import ci
import stages
import catalog
import research


def generate():
    root=Path('.um/freshness')
    text=(root/'workflow.yaml').read_text()
    text=re.sub(r'environmentPassthrough:.*?(?=steps:)', '', text, flags=re.S)
    for name,input_name,ref,output,schema,command in [
        ('investigateEntries','catalog','outputs.prepareCatalog.catalog','assessment','assessment','agentAssessment'),
        ('reviewHistory','history','outputs.collectHistory.history','review','history','agentReview')]:
        original=re.search(r'^  '+name+r':\n.*?(?=^  [a-zA-Z]+:|^exports:)',text,flags=re.S|re.M)[0]
        condition=re.split(r'    (?:agent|inputs):', original.split('    condition:',1)[1],maxsplit=1)[0]
        replacement=f'''  {name}:
    kind: cmd
    condition:{condition}    inputs:
      {input_name}:
        ref: {ref}
    command:
      argv: [python3, .um/freshness/tests/workflow_fixture.py, {command}]
    outputs:
      {output}:
        kind: json
        from: path
        path: .um/freshness/work/fixture-{output}.json
        schema: schemas/{schema}.json
'''
        if name=='investigateEntries':
            replacement += '''      usage:
        kind: text
        from: path
        path: .um/freshness/work/research-model-receipt.json
'''
        if name=='reviewHistory':
            replacement += '''      usage:
        kind: text
        from: path
        path: .um/freshness/work/history-model-receipt.json
'''
        text=re.sub(r'^  '+name+r':\n.*?(?=^  [a-zA-Z]+:|^exports:)',lambda _:replacement,text,flags=re.S|re.M)
    text=text.replace('.um/freshness/scripts/stages.py','.um/freshness/tests/workflow_fixture.py')
    mode=sys.argv[2] if len(sys.argv)>2 else 'correction'
    text=text.replace('workflow_fixture.py, prepare]',f'workflow_fixture.py, prepare, {mode}]')
    (root/'workflow-test.yaml').write_text(text)


class FixtureValidator:
    def __init__(self,*args): pass
    def close(self): pass
    def validate(self,proposal,entry):
        return dict(passed=True,reason='Synthetic validation passed; real tools are tested separately.')


def run(stage):
    if stage=='agentAssessment':
        data=stages.obj('catalog')
        def runner(batch):
            assert len(batch['entries']) <= research.BATCH_SIZE
            rows=[dict(id=e['id'],action='keep',reason='Synthetic control.',
                       evidence=[dict(url='https://example.com',observation='Synthetic evidence, not live research.')],
                       limitations=[], blockers=[], newName=None,newUrl=None,newDescription=None) for e in batch['entries']]
            if data.get('fixtureMode') == 'correction' and rows[0]['id'] == data['entries'][0]['id']:
                rows[0].update(action='update',newDescription=data['entries'][0]['description']+' Synthetic fixture.')
            return dict(results=rows), dict(entryIds=[r['id'] for r in rows],usage=[])
        assessment, receipt = research.investigate(catalog.research_packet(data), runner=runner)
        stages.save('fixture-assessment.json', assessment)
        stages.save('research-model-receipt.json', receipt)
    elif stage=='agentReview':
        packet=stages.obj('history')
        stages.save('history-model-receipt.json', {})
        if not packet['candidates']:
            with patch.object(stages.subprocess, 'run', side_effect=AssertionError('Empty history must not start a model')):
                stages.main('reviewHistory')
        stages.save('fixture-review.json',dict(reviews=[dict(id=c['id'],status='clear',reason='Synthetic history; no duplicate.',references=[]) for c in packet['candidates']]))
    else:
        def collect(data,assessment):
            return dict(catalogSha=data['catalogSha'],candidates=[dict(id=r['id'],complete=True,errors=[],queries=['Synthetic query'],records=[])
                for r in assessment['results'] if r['action']!='keep'])
        original_packet=ci.packet
        mode=sys.argv[2] if len(sys.argv)>2 else 'correction'
        def packet(repo):
            data=original_packet(repo)
            data['fixtureMode']=mode
            return data
        snapshot=lambda entry:dict(complete=True,fingerprint='fixture',source={'kind':'fixture'})
        baseline=catalog.empty()
        if stage=='prepare' and mode=='unchanged':
            data=original_packet(Path.cwd())
            for entry in data['entries']:
                baseline['entries'][catalog.key(entry)]=dict(claim=catalog.claim(entry,data['contributionRules']),
                    snapshot=snapshot(entry),reviewedAt='fixture',assessment={'action':'keep'})
        original=ci.write_report
        def render(*args,**kwargs):
            kwargs['demo']=True
            return original(*args,**kwargs)
        with patch.object(ci,'packet',packet), patch.object(catalog,'snapshot',snapshot), patch.object(catalog,'load',return_value=baseline), patch.object(stages.history,'collect',collect), patch.object(ci,'freshness',return_value='unchanged'), patch.object(stages.checks,'Validator',FixtureValidator), patch.object(ci,'write_report',render):
            stages.main(stage)


if __name__=='__main__':
    if sys.argv[1]=='generate': generate()
    else: run(sys.argv[1])
