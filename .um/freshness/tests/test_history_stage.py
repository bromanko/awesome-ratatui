import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import stages


class HistoryStageTests(unittest.TestCase):
    def test_no_candidates_never_starts_model(self):
        with patch.object(stages,'obj',return_value=dict(candidates=[])), patch.object(stages,'save') as save, patch.object(stages.subprocess,'run') as run:
            stages.main('reviewHistory')
            run.assert_not_called()
            save.assert_any_call('review.json',dict(reviews=[]))

    def test_candidates_use_opus_and_native_schema_dialect(self):
        response=dict(structured_output=dict(reviews=[]),total_cost_usd=0.01)
        with patch.object(stages,'obj',return_value=dict(candidates=[{'id':'1'}])), patch.object(stages,'save') as save, patch.object(stages.subprocess,'run',return_value=SimpleNamespace(stdout=json.dumps(response))) as run:
            stages.main('reviewHistory')
            args=run.call_args.args[0]
            self.assertEqual(args[args.index('--model')+1],'claude-opus-5-5')
            self.assertNotIn('$schema',json.loads(args[args.index('--json-schema')+1]))
            self.assertEqual(args[args.index('--tools')+1],'')
            save.assert_any_call('review.json',dict(reviews=[]))

    def test_model_error_is_not_a_clear_history_review(self):
        with patch.object(stages,'obj',return_value=dict(candidates=[{'id':'1'}])), patch.object(stages,'save'), patch.object(stages.subprocess,'run',return_value=SimpleNamespace(stdout='{"is_error":true}')):
            with self.assertRaises(ValueError):stages.main('reviewHistory')


class FinalFreshnessTests(unittest.TestCase):
    def test_catalog_drift_holds_both_baseline_and_corrections(self):
        import tempfile
        data=dict(baseline={'version':1,'entries':{}}, scannedEntries=[],unchangedEntries=[],entries=[],pendingEntries=[])
        bundle=dict(catalog=data,assessment={},status='unchanged',proposals=[],note='',evaluations={'1':dict(ready=True,note='Ready')},logs={})
        def render(data,assessment,status,output,**kwargs):
            output.mkdir(parents=True,exist_ok=True)
            (output/'report.md').write_text('Fixture')
        with tempfile.TemporaryDirectory() as folder, patch.object(stages,'WORK',Path(folder)), patch.object(stages,'obj',return_value=bundle), patch.object(stages.catalog,'advance',return_value=({'version':1,'entries':{'new':{}}},dict(resolved=['Tool'],pending=[]))), patch.object(stages.ci,'freshness',return_value='changed'), patch.object(stages.ci,'write_report',side_effect=render):
            stages.main('renderPreview')
            self.assertFalse(bundle['evaluations']['1']['ready'])
            self.assertEqual(json.loads((Path(folder)/'preview/baseline.json').read_text()),data['baseline'])
