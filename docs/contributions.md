# Contributions

| Thay đổi | Bằng chứng |
| --- | --- |
| Ba shape và helper xử lý quote/refund | lab8/shapes/{workflow,single,orchestrator,common}.py; 248 student test pass trên cả bốn shape. |
| Test bổ sung | tests/test_student_edge_cases.py: claim không tồn tại, quote đổi khi retry, giới hạn bước ReAct; 7 test pass. |
| Benchmark và crash | reports/benchmark.json: 280 trial; reports/crash.json: 20/20. |
| Ablation và phân tích | lab8/research_ablation.py, reports/ablation_ticket_delay.json; architecture, decision record và research card. |
| Bonus B3 | bonus/swarm_verified.py; 8 claim đối kháng có nhãn tay; reports/bonus_verifier.json (330 trial); 10 test bonus pass; docs/bonus_report.md. |
