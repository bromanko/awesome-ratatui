"""Regression boundaries revealed by live backtesting; no model calls in CI."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import ci
import checks
import history


class CorrectionRegressions(unittest.TestCase):
    def setUp(self):
        self.text='# Tools\n\n- [Alpha](https://a.example) - First.\n- [Middle](https://m.example) - Middle.\n- [Zulu](https://z.example) - Last.\n\n# Other\n\n- [Other](https://other.example) - Other.\n'
        self.data=dict(catalogSha='a'*40,readme=self.text,readmeHash=hashlib.sha256(self.text.encode()).hexdigest(),entries=[ci.entries(self.text)[2]])
        self.row=dict(id='5',action='update',reason='Official rename.',evidence=[dict(url='https://z.example',observation='Official identity.')],limitations=['Project is alpha; software not executed.'],blockers=[],newName='Beta',newUrl=None,newDescription=None)

    def applied(self):
        proposals,_=ci.previews(self.data,dict(results=[self.row]),'unchanged')
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp);(p/'README.md').write_text(self.data['readme']);(p/'edit.patch').write_text(proposals[0]['patch'])
            subprocess.run(['git','apply','--check','edit.patch'],cwd=p,check=True)
            subprocess.run(['git','apply','edit.patch'],cwd=p,check=True)
            return (p/'README.md').read_text(),proposals

    def test_caveats_allow_rename_and_preserve_other_entries(self):
        text,proposals=self.applied()
        self.assertEqual(text,self.text.replace('- [Zulu](https://z.example) - Last.\n','').replace('- [Middle]', '- [Beta](https://z.example) - Last.\n- [Middle]'))
        self.assertIn('Project is alpha',proposals[0]['body'])

    def test_rename_to_end_and_keep_section_boundary(self):
        self.data['entries']=[ci.entries(self.text)[0]];self.row.update(id='3',newName='zzzz')
        text,_=self.applied()
        self.assertIn('- [Zulu](https://z.example) - Last.\n- [zzzz](https://a.example) - First.\n\n# Other',text)

    def test_no_final_newline_preserved(self):
        self.text=self.text.split('\n\n# Other')[0];self.data.update(readme=self.text,readmeHash=hashlib.sha256(self.text.encode()).hexdigest())
        text,_=self.applied()
        self.assertFalse(text.endswith('\n'))
        self.assertEqual(len(ci.entries(text)),3)

    def test_true_blocker_prevents_preview_and_history(self):
        self.row['blockers']=['Ownership of destination is unknown.']
        self.assertEqual(ci.previews(self.data,dict(results=[self.row]),'unchanged')[0],[])
        with patch.object(history,'api') as api:
            self.assertEqual(history.collect(self.data,dict(results=[self.row]))['candidates'],[])
            api.assert_not_called()

    def test_rename_searches_old_and_new_names_despite_caveats(self):
        with patch.dict(history.os.environ,{'FRESHNESS_REPOSITORY':'ratatui/awesome-ratatui'}), patch.object(history,'api',return_value=dict(total_count=0,items=[])):
            candidate=history.collect(self.data,dict(results=[self.row]))['candidates'][0]
        self.assertTrue(candidate['complete'])
        self.assertTrue(any('"Zulu"' in q for q in candidate['queries']))
        self.assertTrue(any('"Beta"' in q for q in candidate['queries']))

    def test_missing_blocker_field_fails_closed(self):
        del self.row['blockers']
        with self.assertRaises(ValueError):ci.validate(self.data,dict(results=[self.row]))

    def test_duplicate_and_markdown_names_rejected(self):
        for name in ['ALPHA','Bad](https://evil.example)','Bad\nName',' Bad']:
            with self.subTest(name=name):
                self.row['newName']=name
                with self.assertRaises(ValueError):ci.previews(self.data,dict(results=[self.row]),'unchanged')

    def test_keep_cannot_contain_rename(self):
        self.row['action']='keep'
        with self.assertRaises(ValueError):ci.validate(self.data,dict(results=[self.row]))

    def test_absent_destination_success_is_not_a_pass(self):
        self.assertFalse(checks.compare_links(dict(errors=[]),dict(errors=[],excluded=[],successful=[]),['https://z.example'])['passed'])

    def test_catalog_changes_after_validation_hold_patch(self):
        class Validator:
            def validate(self,*args):return dict(passed=True,reason='Passed')
        _,proposals=self.applied()
        result=ci.evaluate_proposals(self.data,proposals,dict(candidates=[dict(id='5',complete=True,records=[],errors=[])]),dict(reviews=[dict(id='5',status='clear',references=[],reason='Clear')]),Validator(),lambda _: 'changed')
        self.assertFalse(result['5']['ready'])

    def test_duplicate_never_calls_validator(self):
        class Validator:
            def validate(self,*args):raise AssertionError('Duplicate must not reach validation')
        _,proposals=self.applied();url='https://github.com/example/repo/pull/1'
        result=ci.evaluate_proposals(self.data,proposals,dict(candidates=[dict(id='5',complete=True,records=[dict(html_url=url)],errors=[])]),dict(reviews=[dict(id='5',status='duplicate',references=[url],reason='Same change')]),Validator(),lambda _: 'unchanged')
        self.assertFalse(result['5']['ready'])


if __name__=='__main__':unittest.main()
