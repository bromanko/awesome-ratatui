import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import research


def packet(count):
    return dict(repository='example/catalog', catalogSha='a'*40, contributionRules='Rules',
                entries=[dict(id=str(i), name=f'Tool {i}') for i in range(count)])


def result(batch):
    return dict(results=[dict(id=e['id'],action='keep',reason='Supported.',
        evidence=[dict(url='https://example.com',observation='Supported.')],
        limitations=[],blockers=[],newName=None,newUrl=None,newDescription=None) for e in batch['entries']])


class ResearchBatchTests(unittest.TestCase):
    def test_all_selected_entries_are_covered_in_bounded_batches(self):
        data=packet(47); original=copy.deepcopy(data); sizes=[]
        def runner(batch):
            sizes.append(len(batch['entries']))
            self.assertEqual(batch['contributionRules'], 'Rules')
            return result(batch), {'entryIds':[e['id'] for e in batch['entries']]}
        assessment, receipt=research.investigate(data, runner)
        self.assertEqual(sizes,[20,20,7])
        self.assertEqual([r['id'] for r in assessment['results']], [str(i) for i in range(47)])
        self.assertEqual(receipt['researched'],47)
        self.assertEqual(len(receipt['batches']),3)
        self.assertEqual(data,original)

    def test_no_selected_entries_make_no_model_calls(self):
        def runner(_): self.fail('Unexpected model call')
        self.assertEqual(research.investigate(packet(0),runner)[0], {'results':[]})

    def test_duplicate_selection_rejected_before_model_call(self):
        data=packet(2);data['entries'][1]['id']='0'
        def runner(_): self.fail('Unexpected model call')
        with self.assertRaises(ValueError):research.investigate(data,runner)

    def test_missing_or_cross_batch_results_fail(self):
        for invalid in ['missing','duplicate','foreign']:
            with self.subTest(invalid=invalid):
                def runner(batch):
                    r=result(batch)
                    if invalid=='missing':r['results'].pop()
                    elif invalid=='duplicate':r['results'][1]=r['results'][0]
                    else:r['results'][0]['id']='another-batch'
                    return r,{}
                with self.assertRaises(ValueError):research.investigate(packet(21),runner)

    def test_later_batch_failure_does_not_return_partial_review(self):
        calls=[]
        def runner(batch):
            calls.append(batch)
            if len(calls)==2:raise RuntimeError('Model failed')
            return result(batch),{}
        with self.assertRaises(RuntimeError):research.investigate(packet(41),runner)
        self.assertEqual(len(calls),2)
