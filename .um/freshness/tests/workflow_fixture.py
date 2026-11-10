"""Exercise the real seven-node UM graph with synthetic agent/network/check results."""
from pathlib import Path
import re
import sys
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import ci
import stages


def generate():
    root=Path('.um/freshness')
    text=(root/'workflow.yaml').read_text()
    text=re.sub(r'environmentPassthrough:.*?(?=steps:)', '', text, flags=re.S)
    for name,input_name,ref,output,schema,command in [
        ('investigateEntries','catalog','outputs.prepareCatalog.catalog','assessment','assessment','agentAssessment'),
        ('reviewHistory','history','outputs.collectHistory.history','review','history','agentReview')]:
        replacement=f'''  {name}:
    kind: cmd
    inputs:
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
        text=re.sub(r'^  '+name+r':\n.*?(?=^  [a-zA-Z]+:|^exports:)',lambda _:replacement,text,flags=re.S|re.M)
    text=text.replace('.um/freshness/scripts/stages.py','.um/freshness/tests/workflow_fixture.py')
    (root/'workflow-test.yaml').write_text(text)


class FixtureValidator:
    def __init__(self,*args): pass
    def close(self): pass
    def validate(self,proposal,entry):
        return dict(passed=True,reason='Synthetic validation passed; real tools are tested separately.')


def run(stage):
    if stage=='agentAssessment':
        data=stages.obj('catalog')
        rows=[dict(id=e['id'],action='keep',reason='Synthetic control.',
                   evidence=[dict(url='https://example.com',observation='Synthetic evidence, not live research.')],
                   limitations=[],newUrl=None,newDescription=None) for e in data['entries']]
        rows[0].update(action='update',newDescription=data['entries'][0]['description']+' Synthetic fixture.')
        stages.save('fixture-assessment.json',dict(results=rows))
    elif stage=='agentReview':
        packet=stages.obj('history')
        stages.save('fixture-review.json',dict(reviews=[dict(id=c['id'],status='clear',reason='Synthetic history; no duplicate.',references=[]) for c in packet['candidates']]))
    else:
        def collect(data,assessment):
            return dict(catalogSha=data['catalogSha'],candidates=[dict(id=r['id'],complete=True,errors=[],queries=['Synthetic query'],records=[])
                for r in assessment['results'] if r['action']!='keep'])
        original=ci.write_report
        def render(*args,**kwargs):
            kwargs['demo']=True
            return original(*args,**kwargs)
        with patch.object(stages.history,'collect',collect), patch.object(ci,'freshness',return_value='unchanged'), patch.object(stages.checks,'Validator',FixtureValidator), patch.object(ci,'write_report',render):
            stages.main(stage)


if __name__=='__main__':
    if sys.argv[1]=='generate': generate()
    else: run(sys.argv[1])
