# Contributions

| Thay đổi | Bằng chứng |
| --- | --- |
| Ba shape và helper xử lý quote/refund | src/lab8/shapes/{workflow,single,orchestrator,common}.py; 248 student test pass trên cả bốn shape. |
| Test bổ sung | src/tests/test_student_edge_cases.py: claim không tồn tại, quote đổi khi retry, giới hạn bước ReAct; 7 test pass. |
| Benchmark và crash | src/reports/benchmark.json: 280 trial; src/reports/crash.json: 20/20. |
| Ablation và phân tích | src/lab8/research_ablation.py, src/reports/ablation_ticket_delay.json; architecture, decision record và research card. |
| Bonus B3 | src/bonus/swarm_verified.py; 8 claim đối kháng có nhãn tay; src/reports/bonus_verifier.json (330 trial); 10 test bonus pass; report/team/bonus_report.md. |
