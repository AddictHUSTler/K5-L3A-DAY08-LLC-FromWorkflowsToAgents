# Research card

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 — Failure taxonomy. |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657), NeurIPS 2025; phân tích thực nghiệm các hệ multi-agent. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | MAST phân loại 14 kiểu lỗi thành ba nhóm: thiết kế hệ thống, lệch phối hợp giữa agent và kiểm chứng nhiệm vụ. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Taxonomy rút từ các framework và task trong nghiên cứu; không xác định sẵn nguyên nhân lỗi refund của lab. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Tắt việc lấy delay từ ticket trong swarm sẽ sửa C-002/seed 55: pass tăng từ 69/70 lên 70/70, pass^5 từ 13/14 lên 14/14 và variance về 0. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ MockLLM, prompt/call sites, tools, 14 claim public, world, seed 11/22/33/44/55, giá và evaluator. Chỉ tắt đường ghi đè delay: patch parse_delay_days trả None. Mỗi trial dùng SQLite mới; variant có trace ID riêng. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Phân loại trong lab: lỗi kiểm chứng — chấp nhận delay từ ticket trái order. Đo pass rate, pass^5, seed variance và cost/success bằng benchmark chuẩn. |

## Kết quả ablation

Lệnh chạy trong `src/` sau khi activate môi trường:

```bash
python -m lab8.benchmark --shapes swarm,swarm_order_only --extra-shape swarm_order_only=lab8.research_ablation:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_ticket_delay.json
```

Code: `src/lab8/research_ablation.py`. Patch chỉ có hiệu lực trong variant, giữ nguyên reference. Report: `src/reports/ablation_ticket_delay.json` (140 trial). Run đối chiếu: `R-swarm-C-002-s55` và `R-swarm_order_only-C-002-s55`.

| Metric | Swarm gốc | Tắt ticket delay |
| --- | --- | --- |
| Pass | 69/70 | 70/70 |
| Pass^5 | 0.928571 | 1.000000 |
| Seed min–max | 0.928571–1.000000 | 1.000000–1.000000 |
| Variance | 0.000816 | 0 |
| Cost/success, VND mô phỏng | 49.57 | 48.72 |

Hypothesis đúng trên bộ đo: C-002/seed 55 đổi từ resolved sang denied, không còn trial fail. Cost giảm vì tránh lần tính lại quote và mẫu số success tăng. Số model call giữ nguyên, trung bình 3/trial.

Giới hạn: lỗi được cài sẵn trong reference; kết quả chỉ cô lập đường ghi đè delay, không chứng minh multi-agent nói chung kém hơn. Nhãn “lỗi kiểm chứng” là diễn giải trong lab theo MAST. Corpus nhỏ; latency: `unavailable`.
