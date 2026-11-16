import json
from pathlib import Path

import pytest

from bonus.swarm_verified import run_claim, verify_quote
from lab8.db import connect, init_store, load_json, load_jsonl
from lab8.durability import InjectedCrash
from lab8.metrics import trial_pass
from lab8.schemas import Budget
from lab8.tools import compute_compensation, lookup_order
from lab8.trace import Trace


@pytest.mark.parametrize('seed', [11, 22, 33, 44, 55])
def test_adversarial_labels_and_safety(tmp_path, seed):
    world = load_json('bonus/world.json')
    claims = load_jsonl('bonus/cases.jsonl')
    for claim in claims:
        store = tmp_path / f"{claim['claim_id']}.sqlite"
        init_store(store, world, claims).close()
        result = run_claim(claim['claim_id'], seed=seed, store_path=str(store))
        conn = connect(store)
        try:
            assert trial_pass(result.as_dict(), claim['expected'], conn) == (True, 'ok')
        finally:
            conn.close()
        events = json.loads(Path(result.trace_path).read_text())['events']
        assert sum(e['kind'] == 'verifier_override' for e in events) <= 1


@pytest.mark.parametrize('field,value', [('delay_days', 0), ('status', 'cancelled'),
                                        ('damage_verified', True)])
def test_verifier_checks_each_fact(public_db, tmp_path, field, value):
    conn = connect(public_db)
    try:
        order = lookup_order(conn, 'O-107', principal_id='P-100')['order']
        changed = dict(order, **{field: value})
        budget = Budget()
        trace = Trace('verify', tmp_path)
        repaired = verify_quote(conn, budget, trace, changed, order,
                                compute_compensation(conn, changed))
        assert repaired == compute_compensation(conn, order)
        assert trace.events[0]['payload']['fields'] == [field]
        assert budget.tool_calls == 1
    finally:
        conn.close()


def test_matching_facts_keep_quote_without_repair(public_db, tmp_path):
    conn = connect(public_db)
    try:
        order = lookup_order(conn, 'O-107', principal_id='P-100')['order']
        quote = compute_compensation(conn, order)
        budget, trace = Budget(), Trace('unchanged', tmp_path)
        assert verify_quote(conn, budget, trace, order, order, quote) is quote
        assert budget.tool_calls == 0
        assert trace.events == []
    finally:
        conn.close()


def test_crash_resume_and_retry_preserve_one_refund(public_db):
    with pytest.raises(InjectedCrash):
        run_claim('C-001', seed=55, store_path=str(public_db),
                  crash_at='after_effect_before_checkpoint')
    resumed = run_claim('C-001', seed=55, store_path=str(public_db))
    retried = run_claim('C-001', seed=55, store_path=str(public_db))
    assert resumed.status == retried.status == 'resolved'
    assert resumed.refund_effects == retried.refund_effects
    assert len(retried.refund_effects) == retried.committed_audit_count == 1
