import copy
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('ci', Path(__file__).resolve().parents[1] / 'scripts/ci.py')
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.data = dict(entries=[dict(id='4', name='Example')], catalogSha='a'*40, slice=0, sliceCount=1, readmeHash='hash')
        self.row = dict(id='4', action='keep', reason='Official docs describe a TUI.',
                        evidence=[dict(url='https://example.com', observation='Terminal interface')],
                        limitations=[], newUrl=None, newDescription=None)

    def test_selection_preserves_scope_and_duplicate_names(self):
        rows = ci.entries('# Frameworks\n- [Demo](https://example.com) - Tools.\n# Apps\n- [Demo](https://other.example.com) - App.')
        self.assertEqual([r['section'] for r in rows], ['Frameworks', 'Apps'])
        self.assertNotEqual(rows[0]['id'], rows[1]['id'])

    def test_unknown_entry_format_fails(self):
        with self.assertRaises(ValueError): ci.entries('- [Broken](relative) - Text.')

    def test_out_of_range_slice_fails(self):
        with patch.object(ci, 'git', side_effect=['a'*40, '- [A](https://a.example) - TUI.', 'Rules']):
            with self.assertRaises(ValueError): ci.packet(Path('.'), 1)

    def test_negative_slice_fails(self):
        with self.assertRaises(ValueError): ci.packet(Path('.'), -1)

    def test_exact_coverage(self):
        for rows in [[], [self.row, self.row], [dict(self.row, id='other')]]:
            with self.assertRaises(ValueError): ci.validate(self.data, dict(results=rows))

    def test_no_evidence_is_uncertain(self):
        self.row['evidence'] = []
        with self.assertRaises(ValueError): ci.validate(self.data, dict(results=[self.row]))
        self.row['action'] = 'uncertain'
        ci.validate(self.data, dict(results=[self.row]))

    def test_correction_consistency(self):
        self.row['newUrl'] = 'https://new.example'
        with self.assertRaises(ValueError): ci.validate(self.data, dict(results=[self.row]))
        self.row['action'] = 'update'
        ci.validate(self.data, dict(results=[self.row]))
        self.row['newUrl'] = 'javascript:alert(1)'
        with self.assertRaises(ValueError): ci.validate(self.data, dict(results=[self.row]))

    def test_untrusted_output_is_plain_text(self):
        self.row['reason'] = '</pre><script>alert(1)</script>![tracking](https://example.com)'
        report = ci.render(self.data, dict(results=[self.row]), 'changed')
        self.assertNotIn('<script>', report)
        self.assertIn('&lt;script&gt;', report)
        self.assertIn('Catalog recheck: changed', report)

    def test_failed_recheck_is_not_current(self):
        with patch.object(ci.subprocess, 'check_output', side_effect=OSError):
            self.assertTrue(ci.freshness(self.data).startswith('unverified'))

    def test_changed_recheck(self):
        with patch.object(ci.subprocess, 'check_output', return_value='{"content":"aGk="}'):
            self.assertTrue(ci.freshness(self.data).startswith('changed'))


if __name__ == '__main__': unittest.main()
