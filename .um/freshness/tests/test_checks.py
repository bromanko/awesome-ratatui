import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import checks
import history


class DiscussionTests(unittest.TestCase):
    def setUp(self):
        self.candidate = dict(id='2',complete=True,errors=[],records=[dict(html_url='https://github.com/ratatui/awesome-ratatui/pull/1')])
        self.review = dict(id='2',status='clear',reason='No same change.',references=[])

    def test_duplicate_rejected_obsolete_and_unknown_hold(self):
        for status in ['duplicate','rejected','obsolete','incomplete','invalid']:
            self.review.update(status=status,references=['https://github.com/ratatui/awesome-ratatui/pull/1'])
            self.assertFalse(history.gate(self.candidate,self.review)[0])

    def test_incomplete_search_cannot_be_cleared_by_model(self):
        self.candidate['complete'] = False
        self.assertFalse(history.gate(self.candidate,self.review)[0])

    def test_related_requires_a_collected_reference(self):
        self.review.update(status='related',references=['https://invented.example'])
        self.assertFalse(history.gate(self.candidate,self.review)[0])
        self.review['references']=['https://github.com/ratatui/awesome-ratatui/pull/1']
        self.assertTrue(history.gate(self.candidate,self.review)[0])

    def test_missing_review_is_held(self):
        self.assertFalse(history.gate(self.candidate,None)[0])

    def test_search_outage_recorded(self):
        data=dict(catalogSha='a'*40,entries=[dict(id='1',name='Example',url='https://old.example')])
        raw=dict(results=[dict(id='1',action='update',limitations=[], blockers=[], newName=None,newUrl='https://new.example')])
        with patch.dict(history.os.environ, {'GITHUB_REPOSITORY':'bromanko/awesome-ratatui'}), patch.object(history,'api',side_effect=OSError):
            result=history.collect(data,raw)['candidates'][0]
        self.assertFalse(result['complete'])
        self.assertEqual(len(result['queries']),6)
        self.assertTrue(any('repo:ratatui/awesome-ratatui' in q for q in result['queries']))
        self.assertTrue(any('repo:bromanko/awesome-ratatui' in q for q in result['queries']))

    def test_truncated_search_is_not_clear(self):
        data=dict(catalogSha='a'*40,entries=[dict(id='1',name='Example',url='https://old.example')])
        raw=dict(results=[dict(id='1',action='remove',limitations=[], blockers=[], newName=None,newUrl=None)])
        with patch.object(history,'api',return_value=dict(total_count=31,incomplete_results=False,items=[])):
            self.assertFalse(history.collect(data,raw)['candidates'][0]['complete'])


class ValidationTests(unittest.TestCase):
    def test_preexisting_unrelated_failure_does_not_block(self):
        before=dict(errors=['https://unrelated.example'])
        after=dict(errors=['https://unrelated.example'],excluded=[],successful=['https://changed.example'])
        result=checks.compare_links(before,after,['https://changed.example'])
        self.assertTrue(result['passed'])
        self.assertEqual(result['preexisting'],['https://unrelated.example/'])

    def test_new_failure_and_affected_old_failure_block(self):
        after=dict(errors=['https://changed.example'],excluded=[])
        self.assertFalse(checks.compare_links(dict(errors=[]),after,[])['passed'])
        self.assertFalse(checks.compare_links(dict(errors=after['errors']),after,after['errors'])['passed'])

    def test_ignored_destination_is_not_a_pass(self):
        self.assertFalse(checks.compare_links(dict(errors=[]),dict(errors=[],excluded=['https://changed.example']),['https://changed.example'])['passed'])

    def test_timeout_is_incomplete(self):
        with self.assertRaises(ValueError): checks.links(dict(exitCode=-1,stdout=''),Path('/tmp'))

    def test_file_paths_normalized_across_checkouts(self):
        result=dict(exitCode=2,stdout=json.dumps(dict(total=1,errors=1,error_map={'README.md':[dict(url='file:///tmp/base/missing.md')]})))
        self.assertEqual(checks.links(result,Path('/tmp/base'))['errors'],['file://CATALOG/missing.md'])


if __name__ == '__main__': unittest.main()
