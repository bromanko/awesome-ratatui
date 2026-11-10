"""Research selected entries in bounded native-UM agent sessions."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import ci

BATCH_SIZE = 20


def run_batch(packet):
    root = Path('.um/freshness').resolve()
    with tempfile.TemporaryDirectory(prefix='freshness-research-') as folder:
        temp = Path(folder)
        request = temp/'research.json'
        request.write_text(json.dumps(packet))
        # Each batch retains the native UM agent harness and schema validation.
        # The enclosing workflow owns selection and the combined final report.
        result = subprocess.run(['um', 'workflow', 'run', '--source-root', str(root),
            '--execution-root', str(Path.cwd()), '--run-dir', str(temp/'run'),
            '--input-text-file', 'research', str(request), '--json',
            str(root/'research-batch.yaml')], text=True, capture_output=True,
            timeout=1800, check=True, env=dict(os.environ))
        run = json.loads(result.stdout)
        if run.get('outcome') != 'succeeded':
            raise ValueError('Research batch did not succeed')
        exported = run['result']['exports']['assessment']
        if exported.get('state') != 'available' or exported.get('kind') != 'json':
            raise ValueError('Research batch has no validated assessment')
        path = (Path(run['resultDirectory'])/exported['path']).resolve()
        if not path.is_relative_to(temp.resolve()):
            raise ValueError('Research export escaped the batch directory')
        assessment = json.loads(path.read_text())
        receipts = []
        for transcript in (temp/'run').rglob('transcript.jsonl'):
            rows = [json.loads(line) for line in transcript.read_text().splitlines()]
            receipt = next((r for r in reversed(rows) if r.get('type') == 'cost-state'), None)
            if receipt:
                receipts.append({k: receipt.get(k) for k in ['totalCostUSD', 'modelUsage', 'hasUnknownModelCost']})
        return assessment, dict(entryIds=[e['id'] for e in packet['entries']], usage=receipts)


def investigate(packet, runner=None):
    runner = runner or run_batch
    entries = packet['entries']
    if len({entry['id'] for entry in entries}) != len(entries):
        raise ValueError('Duplicate selected entry')
    assessment, receipts = dict(results=[]), []
    for offset in range(0, len(entries), BATCH_SIZE):
        batch = dict(packet, entries=entries[offset:offset+BATCH_SIZE])
        print(f'Research batch {offset//BATCH_SIZE+1}: {len(batch["entries"])} entries', flush=True)
        result, receipt = runner(batch)
        ci.validate(batch, result)
        assessment['results'].extend(result['results'])
        receipts.append(receipt)
    ci.validate(packet, assessment)
    return assessment, dict(batchSize=BATCH_SIZE, researched=len(entries), batches=receipts)
