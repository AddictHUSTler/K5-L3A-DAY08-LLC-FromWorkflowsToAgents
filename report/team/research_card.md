# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 — Failure taxonomy |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Mert Cemri et al., “Why Do Multi-Agent LLM Systems Fail?”, NeurIPS 2025, Datasets and Benchmarks Track. [Trang bài báo NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html). Nghiên cứu thực nghiệm về taxonomy và bộ trace MAST. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | MAST nhận diện 14 dạng lỗi trong hệ multi-agent, gom thành ba nhóm: lỗi thiết kế hệ thống, lệch giữa các agent và kiểm chứng tác vụ. Taxonomy được xây qua phân tích 150 trace và đạt κ = 0.88 giữa người gán nhãn. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Kết luận nguồn dựa trên các trace và framework được nghiên cứu; ablation của nhóm chỉ có 14 claim public × 5 seed với MockLLM. Nhóm dùng các nhóm lỗi như khung diễn giải cho một lỗi được cài sẵn, không tái lập hay xác nhận độ khái quát của taxonomy MAST. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Nếu giữ swarm nhưng bỏ khả năng lấy `delay_days` từ ticket, lỗi T02 ở seed 55 sẽ được loại bỏ: pass rate tăng từ khoảng 98.6% lên 100%, pass^5 từ khoảng 92.9% lên 100%, variance giảm về 0; cost/success dự kiến gần như giữ nguyên hoặc giảm nhẹ. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ nguyên 14 claim, 5 seed (11, 22, 33, 44, 55), MockLLM, tools, bảng giá, evaluator và DB mới cho mỗi trial. Chỉ thay đổi việc dùng parser `parse_delay_days`: baseline swarm đọc độ trễ từ ticket; `swarm_order_only` tắt parser để quyết định theo dữ liệu order. Namespace run ID riêng chỉ để trace hai nhánh không đè lên nhau. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến là lỗi kiểm chứng: ở T02/seed 55 swarm tin ticket “trễ 5 ngày” thay vì order “2 ngày”, dẫn tới resolved thay vì denied. Đo pass rate, pass^5, seed variance và cost/success trên cùng 70 trial; kiểm tra thêm safety counts trong report. |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes swarm,swarm_order_only --extra-shape swarm_order_only=scripts.research_ablation:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_ticket_delay.json`
- Run id / file report: `src/reports/ablation_ticket_delay.json`; trial lỗi baseline `R-swarm-C-002-s55`; trial tương ứng của biến thể `R-swarm_order_only-C-002-s55`.
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: Ủng hộ hypothesis trong bộ public này. Swarm đạt 69/70 (pass rate 0.986; pass^5 0.929; variance 0.000816; cost/success 49.57 VND), còn `swarm_order_only` đạt 70/70 (1.000; 1.000; 0; 48.72 VND). Lỗi duy nhất của baseline là T02/seed 55; biến thể không còn lỗi. Cost/success giảm khoảng 1.7% trong phép đo này.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
