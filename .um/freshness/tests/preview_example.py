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
    candidate = dict(id='2', complete=True, errors=[], records=[],
                     queries=['Fictional example: project name, old URL, proposed URL'])
    class ExampleValidator:
        def validate(self, proposal, entry):
            return dict(passed=True, reason='Simulated: formatting, spelling, and destination passed; no real checks ran.',
                        links=dict(introduced=[], preexisting=['https://example.com/unrelated-outage']))
    ci.write_report(data, raw, 'unchanged', Path(sys.argv[1]), demo=True,
                    history_packet=dict(candidates=[candidate]),
                    history_review=dict(reviews=[dict(id='2',status='clear',reason='Synthetic search: no existing correction.',references=[])]),
                    validator=ExampleValidator())
