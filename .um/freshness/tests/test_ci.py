import copy
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "scripts"))
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('ci', Path(__file__).resolve().parents[1] / 'scripts/ci.py')
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        self.data = dict(entries=[dict(id='4', name='Example')], catalogSha='a'*40, readmeHash='hash')
        self.row = dict(id='4', action='keep', reason='Official docs describe a TUI.',
                        evidence=[dict(url='https://example.com', observation='Terminal interface')],
                        limitations=[], blockers=[], newName=None, newUrl=None, newDescription=None)

    def test_selection_preserves_scope_and_duplicate_names(self):
        rows = ci.entries('# Frameworks\n- [Demo](https://example.com) - Tools.\n# Apps\n- [Demo](https://other.example.com) - App.')
        self.assertEqual([r['section'] for r in rows], ['Frameworks', 'Apps'])
        self.assertNotEqual(rows[0]['id'], rows[1]['id'])

    def test_unknown_entry_format_fails(self):
        with self.assertRaises(ValueError): ci.entries('- [Broken](relative) - Text.')

    def test_packet_always_covers_entire_catalog(self):
        readme = '\n'.join(f'- [Tool {i}](https://example.com/{i}) - TUI.' for i in range(47))
        with patch.object(ci, 'git', side_effect=['a'*40, readme, 'Rules']):
            data = ci.packet(Path('.'))
        self.assertEqual(len(data['entries']), 47)
        self.assertEqual(data['entries'][-1]['name'], 'Tool 46')
        self.assertNotIn('slice', data)

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



class PreviewTests(unittest.TestCase):
    def setUp(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from catalog_fixture import example
        self.data, self.raw = example()

    def test_patch_applies_and_preserves_other_entries(self):
        import subprocess
        import tempfile
        proposals, _ = ci.previews(self.data, self.raw, 'unchanged')
        self.assertEqual(len(proposals), 1)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text(self.data['readme'])
            (root / 'change.patch').write_text(proposals[0]['patch'])
            subprocess.run(['git', 'apply', '--check', 'change.patch'], cwd=root, check=True)
            subprocess.run(['git', 'apply', 'change.patch'], cwd=root, check=True)
            self.assertEqual((root / 'README.md').read_text(), self.data['readme'].replace(
                '](https://example.com/notes)', '](https://example.com/terminal-notes)'))

    def test_stale_and_unknown_catalog_withhold_patch(self):
        for status in ['changed', 'unverified']:
            self.assertEqual(ci.previews(self.data, self.raw, status)[0], [])

    def test_blockers_withhold_patch(self):
        self.raw['results'][0]['blockers'] = ['Destination ownership unclear.']
        self.assertEqual(ci.previews(self.data, self.raw, 'unchanged')[0], [])

    def test_keep_produces_no_patch(self):
        row = self.raw['results'][0]
        row.update(action='keep', newUrl=None)
        self.assertEqual(ci.previews(self.data, self.raw, 'unchanged')[0], [])

    def test_mismatched_line_and_hash_rejected(self):
        self.data['entries'][0]['line'] = 'wrong'
        with self.assertRaises(ValueError): ci.previews(self.data, self.raw, 'unchanged')
        self.data['readmeHash'] = 'wrong'
        with self.assertRaises(ValueError): ci.previews(self.data, self.raw, 'unchanged')

    def test_multiline_description_rejected(self):
        self.raw['results'][0]['newDescription'] = 'Text.\n- Injected entry'
        with self.assertRaises(ValueError): ci.previews(self.data, self.raw, 'unchanged')

    def test_removal_changes_one_entry(self):
        self.raw['results'][0].update(action='remove', newUrl=None)
        proposals, _ = ci.previews(self.data, self.raw, 'unchanged')
        self.assertIn('-' + self.data['entries'][0]['line'], proposals[0]['patch'])
        self.assertNotIn('-' + self.data['entries'][1]['line'], proposals[0]['patch'])

    def test_held_preview_never_exports_patch_and_clears_old_patch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output/'entry-2.patch').write_text('old stale proposal')
            ci.write_report(self.data,self.raw,'unchanged',output,demo=True)
            self.assertFalse((output/'entry-2.patch').exists())
            report = (output/'report.md').read_text()
            self.assertIn('Held', report)
            self.assertIn('<summary>Show held diff</summary>', report)
            self.assertIn('History check not performed.', report)

    def test_ready_preview_exports_checked_patch(self):
        import tempfile
        class Validator:
            def validate(self, proposal, entry):
                return dict(passed=True,reason='Fixture passed')
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)
            proposals, note = ci.previews(self.data,self.raw,'unchanged')
            evaluated = ci.evaluate_proposals(self.data,proposals,
                dict(candidates=[dict(id='2',complete=True,errors=[],records=[],queries=[])]),
                dict(reviews=[dict(id='2',status='clear',reason='Fixture',references=[])]),
                Validator(),lambda data:'unchanged')
            ci.write_report(self.data,self.raw,'unchanged',output,demo=True,
                            prepared=(proposals,note),evaluations=evaluated)
            self.assertTrue((output/'entry-2.patch').exists())
            report = (output/'report.md').read_text()
            self.assertIn('Ready for maintainer review', report)
            self.assertLess(report.index('```diff'), report.index('<summary>Evidence and checks'))
            self.assertNotIn('<summary>Show held diff</summary>', report)
            self.assertTrue((output/'entry-2.checks.json').exists())


if __name__ == '__main__': unittest.main()
