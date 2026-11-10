import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.entry = dict(id='12', name='Tool', url='https://github.com/example/tool',
                          description='A tool.', section='Tools', line='unused')
        self.data = dict(entries=[self.entry], contributionRules='rules', repository='test', catalogSha='sha')
        self.source = dict(complete=True, fingerprint='same', source={'files': {'README.md':'blob'}})
        self.review = dict(results=[dict(id='12', action='keep', reason='Verified.', evidence=[dict(url=self.entry['url'], observation='Read official docs.')],
                                        blockers=[], limitations=[], newName=None, newUrl=None, newDescription=None)])
        self.fetch = lambda _: copy.deepcopy(self.source)

    def baseline(self):
        packet=catalog.prepare(self.data,catalog.empty(),self.fetch)
        return catalog.advance(packet,self.review,self.fetch)[0]

    def test_initial_inventory_does_not_mark_reviewed(self):
        data=catalog.prepare(self.data,catalog.empty(),self.fetch)
        self.assertEqual(data['entries'][0]['changeReason'],'not-reviewed')
        self.assertEqual(data['baseline']['entries'],{})

    def test_completed_review_skips_unchanged(self):
        data=catalog.prepare(self.data,self.baseline(),self.fetch)
        self.assertEqual(data['entries'],[])
        self.assertEqual(len(data['unchangedEntries']),1)

    def test_line_number_change_does_not_trigger_research(self):
        baseline=self.baseline()
        self.entry['id']='99'
        self.assertEqual(catalog.prepare(self.data,baseline,self.fetch)['entries'],[])

    def test_catalog_description_and_rules_changes_trigger(self):
        for field in ['description','contributionRules']:
            baseline=self.baseline()
            target=self.data if field=='contributionRules' else self.entry
            old=target[field];target[field]='changed'
            self.assertEqual(catalog.prepare(self.data,baseline,self.fetch)['entries'][0]['changeReason'],'catalog-changed')
            target[field]=old

    def test_source_change_triggers(self):
        baseline=self.baseline()
        self.source['fingerprint']='changed'
        self.assertEqual(catalog.prepare(self.data,baseline,self.fetch)['entries'][0]['changeReason'],'source-changed')

    def test_failure_is_pending_and_does_not_overwrite_baseline(self):
        baseline=self.baseline()
        data=catalog.prepare(self.data,baseline,lambda _:dict(complete=False,error='rate limit'))
        self.assertEqual(data['entries'],[])
        result,progress=catalog.advance(data,dict(results=[]),self.fetch)
        self.assertEqual(result,baseline)
        self.assertEqual(progress['pending'],['Tool'])

    def test_uncertain_correction_and_blocked_keep_never_advance(self):
        for action,blockers in [('uncertain',[]),('update',[]),('keep',['missing evidence'])]:
            row=copy.deepcopy(self.review)
            row['results'][0].update(action=action,blockers=blockers,newDescription='New description.' if action=='update' else None)
            data=catalog.prepare(self.data,catalog.empty(),self.fetch)
            result,progress=catalog.advance(data,row,self.fetch)
            self.assertEqual(result['entries'],{})
            self.assertEqual(progress['pending'],['Tool'])

    def test_source_changed_during_research_stays_pending(self):
        data=catalog.prepare(self.data,catalog.empty(),self.fetch)
        result,progress=catalog.advance(data,self.review,lambda _:dict(complete=True,fingerprint='different'))
        self.assertFalse(result['entries'])
        self.assertEqual(progress['pending'],['Tool'])

    def test_unrelated_completed_reviews_survive_other_entry_updates(self):
        baseline=self.baseline()
        other=copy.deepcopy(self.data)
        other['entries'][0]['url']='https://github.com/example/other'
        data=catalog.prepare(other,baseline,self.fetch)
        result,_=catalog.advance(data,self.review,self.fetch)
        self.assertEqual(len(result['entries']),2)

    def test_focused_packet_omits_full_catalog_and_other_reviews(self):
        data=catalog.prepare(self.data,catalog.empty(),self.fetch)
        self.assertNotIn('baseline',catalog.research_packet(data))
        self.assertNotIn('readme',catalog.research_packet(data))

    def test_tree_covers_workspace_manifests_but_ignores_unrelated_code(self):
        meta=dict(full_name='example/tool',default_branch='main',archived=False,description='Tool')
        tree=dict(truncated=False,tree=[dict(path=p,type='blob',sha=p) for p in ['README.md','crates/ui/Cargo.toml','docs/usage.md','src/main.rs']])
        with patch.object(catalog.history,'api',side_effect=[meta,tree]):
            source=catalog.github_snapshot('example/tool')
        self.assertEqual(set(source['files']),{'README.md','crates/ui/Cargo.toml','docs/usage.md'})

    def test_truncated_tree_is_not_a_complete_snapshot(self):
        meta=dict(full_name='example/tool',default_branch='main',archived=False)
        with patch.object(catalog.history,'api',side_effect=[meta,dict(truncated=True,tree=[])]):
            self.assertFalse(catalog.snapshot(self.entry)['complete'])


if __name__ == '__main__': unittest.main()
