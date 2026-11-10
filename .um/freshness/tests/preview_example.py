"""Render clearly labeled fictional examples without a model call or network access."""
import hashlib
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ci


def example():
    readme = ('# Example catalog\n'
              '- [Sample Notes](https://example.com/notes) - A terminal notebook.\n'
              '- [Sample Tasks](https://example.com/tasks) - A terminal task manager.\n')
    data = dict(repository=ci.UPSTREAM, catalogSha='0'*40, readme=readme,
                readmeHash=hashlib.sha256(readme.encode()).hexdigest(),
                entries=ci.entries(readme), slice=0, sliceCount=1)
    rows = [dict(id='2', action='update', reason='Fictional example: official documentation lists a new project URL.',
                 evidence=[dict(url='https://example.com/notes', observation='Synthetic evidence of a move; no source was fetched.')],
                 limitations=[], newUrl='https://example.com/terminal-notes', newDescription=None),
            dict(id='3', action='keep', reason='Fictional example: the description still fits.',
                 evidence=[dict(url='https://example.com/tasks', observation='Synthetic control; no source was fetched.')],
                 limitations=[], newUrl=None, newDescription=None)]
    return data, dict(results=rows)


if __name__ == '__main__':
    data, raw = example()
    # Show ready, duplicate-held and validation-held outcomes side by side.
    raw['results'][1].update(action='update',newUrl='https://example.com/new-tasks')
    data['readme'] += '- [Sample Clock](https://example.com/clock) - A terminal clock.\n'
    data['entries'] = ci.entries(data['readme'])
    data['readmeHash'] = hashlib.sha256(data['readme'].encode()).hexdigest()
    raw['results'].append(dict(id='4',action='update',reason='Fictional example: suggested new clock homepage.',
        evidence=[dict(url='https://example.com/clock',observation='Synthetic evidence; no source fetched.')],
        limitations=[],newUrl='https://example.com/new-clock',newDescription=None))
    duplicate='https://github.com/example/catalog/pull/123'
    candidates=[dict(id=str(i),complete=True,errors=[],records=[],
        queries=['Fictional example: project name, old URL, proposed URL']) for i in (2,3,4)]
    candidates[1]['records']=[dict(html_url=duplicate,title='Fictional existing correction')]
    reviews=[dict(id=str(i),status='clear',reason='Synthetic search: no existing correction.',references=[]) for i in (2,3,4)]
    reviews[1].update(status='duplicate',reason='Fictional open PR already proposes this same URL correction.',references=[duplicate])
    class ExampleValidator:
        def validate(self, proposal, entry):
            if proposal['id']=='4':
                return dict(passed=False,reason='Simulated: proposed destination link failed; edit held.',
                            links=dict(introduced=['https://example.com/new-clock'],preexisting=[]))
            return dict(passed=True, reason='Simulated: formatting, spelling, and destination passed; no real checks ran.',
                        links=dict(introduced=[], preexisting=['https://example.com/unrelated-outage']))
    proposals, note = ci.previews(data, raw, 'unchanged')
    evaluated = ci.evaluate_proposals(data,proposals,dict(candidates=candidates),dict(reviews=reviews),
                                     ExampleValidator(),lambda data:'unchanged')
    ci.write_report(data,raw,'unchanged',Path(sys.argv[1]),demo=True,
                    prepared=(proposals,note),evaluations=evaluated)
