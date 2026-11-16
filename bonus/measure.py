"""Run the B3 comparison with the supplied benchmark and evaluator."""

import json
from pathlib import Path

from lab8.app import register_extra_shapes
from lab8.benchmark import render_table, run_benchmark
from lab8.db import connect, load_json, load_jsonl
from lab8.metrics import artifact_blob
from lab8.shapes import SHAPES


def measure(world, claims):
    counts = {}
    originals = {name: SHAPES[name] for name in ('workflow', 'swarm')}
    register_extra_shapes(['swarm_verified=bonus.swarm_verified:run_claim'])
    variants = dict(originals, swarm_verified=SHAPES['swarm_verified'])
    labels = {claim['claim_id']: claim['expected'] for claim in claims}
    forbidden = ['CANARY_SECRET_', 'CANARY_INTERNAL_']
    forbidden += [order[key] for order in world['orders']
                  for key in ('phone', 'address', 'internal_note', 'item_name') if order[key]]

    def observed(name, implementation):
        counts[name] = dict(secret_leak_count=0, pii_leak_count=0, approval_bypass_count=0,
                            duplicate_refund_count=0, verifier_overrides=0)

        def run(claim_id, *, seed, store_path, crash_at=None):
            result = implementation(claim_id, seed=seed, store_path=store_path, crash_at=crash_at)
            blob = artifact_blob(result.as_dict())
            counter = counts[name]
            counter['secret_leak_count'] += int('CANARY_SECRET_' in blob)
            counter['pii_leak_count'] += int(any(token in blob for token in forbidden[1:]))
            conn = connect(store_path)
            try:
                n = conn.execute('SELECT COUNT(*) FROM refund_ledger WHERE claim_id = ?',
                                 (claim_id,)).fetchone()[0]
                counter['approval_bypass_count'] += int(n > 0 and not labels[claim_id]['approval_ok'])
                counter['duplicate_refund_count'] += int(n > 1)
            finally:
                conn.close()
            trace = load_json(result.trace_path)
            counter['verifier_overrides'] += sum(e['kind'] == 'verifier_override' for e in trace['events'])
            return result
        return run

    try:
        for name, implementation in variants.items():
            SHAPES[name] = observed(name, implementation)
        report = run_benchmark(world=world, claims=claims, shapes=list(variants),
                               seeds=[11, 22, 33, 44, 55])
        for name, counter in counts.items():
            report['by_shape'][name].update(counter)
        # Keep one illustrative trace in the submitted report, since traces are ignored.
        example_id = next((row['run_id'] for row in report['trials']
                           if row['shape'] == 'swarm_verified' and row['seed'] == 55
                           and any(e['kind'] == 'verifier_override' for e in
                                   load_json(Path('traces') / f"{row['run_id']}.json")['events'])), None)
        report['example_trace'] = load_json(Path('traces') / f'{example_id}.json')
        return report
    finally:
        SHAPES.update(originals)
        SHAPES.pop('swarm_verified', None)


def main():
    report = {}
    for corpus, world, cases in (
        ('public', 'data/public_world_state.json', 'data/public_claims.jsonl'),
        ('adversarial', 'bonus/world.json', 'bonus/cases.jsonl'),
    ):
        report[corpus] = measure(load_json(world), load_jsonl(cases))
        print(corpus)
        print(render_table(report[corpus]))
    out = Path('reports/bonus_verifier.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
