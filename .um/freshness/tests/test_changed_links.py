"""Changed inline destinations need positive link-check evidence, including exclusions."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import ci
import checks

class ChangedLinkTests(unittest.TestCase):
    def test_excluded_inline_link_holds_even_when_primary_link_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            before='# Tools\n- [Tool](https://example.com) - Original.\n'
            (root/'README.md').write_text(before)
            for command in [['git','init','-q'],['git','add','README.md'],['git','-c','user.name=Test','-c','user.email=test@example.com','-c','commit.gpgsign=false','commit','-qm','Fixture']]:
                subprocess.run(command,cwd=root,check=True)
            sha=ci.git(root,'rev-parse','HEAD').strip()
            data=dict(catalogSha=sha,readme=before,readmeHash=hashlib.sha256(before.encode()).hexdigest(),entries=ci.entries(before))
            row=dict(id='2',action='update',reason='Verified documentation.',evidence=[dict(url='https://example.com',observation='Docs linked.')],limitations=[],blockers=[],newName=None,newUrl=None,newDescription='Updated [documentation](https://docs.example).')
            proposal=ci.previews(data,dict(results=[row]),'unchanged')[0][0]
            def results(excluded):
                return dict(links=dict(exitCode=0,stdout=json.dumps(dict(total=2,success_map={'README.md':[dict(url='https://example.com')]},excluded_map={'README.md':[dict(url='https://docs.example')]} if excluded else {})),stderr=''),lint=dict(exitCode=0),spelling=dict(exitCode=0))
            validator=checks.Validator(root,sha,before,root/'out')
            try:
                with patch.object(validator,'check',side_effect=[results(False),results(True)]):
                    result=validator.validate(proposal,data['entries'][0])
                self.assertFalse(result['passed'])
                self.assertEqual(result['links']['unverified'],['https://docs.example/'])
            finally:
                validator.close()

    def test_all_inline_destinations_in_changed_row_are_selected(self):
        before='# Tools\n- [Tool](https://example.com) - Original.\n'
        after=before.replace('Original.','[Docs](https://docs.example/path) and <https://api.example> or https://bare.example.')
        self.assertEqual(set(checks.changed_urls(before,after)),{'https://example.com','https://docs.example/path','https://api.example','https://bare.example'})

    def test_changed_row_matching_another_section_still_requires_success(self):
        before='# First\n- [Tool](https://old.example) - A tool.\n# Second\n- [Tool](https://new.example) - A tool.\n'
        after=before.replace('https://old.example','https://new.example')
        relevant=checks.changed_urls(before,after)
        self.assertEqual(relevant,['https://new.example'])
        result=checks.compare_links(dict(errors=[]),dict(errors=[],excluded=['https://new.example'],successful=[]),relevant)
        self.assertFalse(result['passed'])
        self.assertEqual(result['unverified'],['https://new.example/'])
