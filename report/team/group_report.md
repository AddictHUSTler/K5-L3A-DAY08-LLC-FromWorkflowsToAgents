# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Tên nhóm: LLC
- Thành viên: Đỗ Nhật Anh (2A202603701), Nguyễn Trọng Phương Bách (2A202603716); thông tin chi tiết ở `TEAM.md`.
- Repo: [K5-L3A-DAY08-LLC-FromWorkflowsToAgents](https://github.com/AddictHUSTler/K5-L3A-DAY08-LLC-FromWorkflowsToAgents), nhánh `main`.
- Commit hồ sơ và bằng chứng CP5: `c3b7633`; commit tiếp theo ghi hash này vào ADR/TEAM: `043ccf0`.

## 2. Mục tiêu và cách tiếp cận

Nhóm xây dựng cùng một luồng xử lý claim trên bốn kiến trúc: workflow, single agent, orchestrator và swarm. Mục tiêu là chọn kiến trúc ít tự chủ nhất nhưng vẫn xử lý đúng, an toàn và có chi phí hợp lý. Nhóm giữ các quyết định về entitlement, approval và ghi ledger ở code/host; model chỉ tham gia các bước đọc hoặc soạn thảo được phép.

Hai thành viên phối hợp triển khai và rà soát các shape, kiểm thử policy/bảo mật, benchmark và báo cáo. Đỗ Nhật Anh tập trung vào test các nhánh approval, quyền truy cập và trace; Nguyễn Trọng Phương Bách tập trung tích hợp shape và phần bonus B3 verifier.

## 3. Giải pháp

| Shape | Luồng thực thi |
| --- | --- |
| workflow | Đọc claim → kiểm tra order có thuộc principal → tính quote từ dữ liệu order/policy → gửi quote đầy đủ cho host → trả kết quả từ ledger. Không cần model để quyết định nghiệp vụ. |
| single | Dùng ReAct tối đa 8 bước với tool chỉ đọc để lấy order; code tính quote, còn host kiểm approval và ghi refund. |
| orchestrator | Tạo handoff `handoff.v1` đã sanitize; investigator chỉ dùng tool đọc. Orchestrator lấy kết quả order/quote và gửi host xử lý settlement. |
| swarm | Baseline nhiều agent dùng để so sánh. Điểm yếu có chủ đích là seed 55 có thể tin số ngày trong ticket thay vì dữ liệu order. |

`compute_compensation` tính entitlement từ order và policy hiện hành. Shape gửi toàn bộ quote cho `durability.issue_refund`; host kiểm tra approval đúng claim, giới hạn theo approval/giá trị đã thanh toán và trần refund theo order. Nhờ đó retry cùng claim không tạo refund thứ hai; crash sau effect có thể resume từ ledger. Trace và handoff chỉ chứa dữ liệu được phép, không ghi raw claim/order, secret, header hay PII.

## 4. Kết quả

### Benchmark public

Benchmark dùng 14 claim, năm seed `11, 22, 33, 44, 55`, cùng MockLLM, bảng giá và evaluator. Số liệu lấy từ `src/reports/benchmark.json`.

| Shape | Pass | Pass^5 | Seed min–max | Variance | VND/success |
| --- | ---: | ---: | ---: | ---: | ---: |
| workflow | 70/70 | 1.000 | 1.000–1.000 | 0 | 34.29 |
| single | 70/70 | 1.000 | 1.000–1.000 | 0 | 34.95 |
| orchestrator | 70/70 | 1.000 | 1.000–1.000 | 0 | 43.57 |
| swarm | 69/70 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 |

Nhóm chọn workflow vì đạt độ đúng như single và orchestrator với cost/success thấp nhất. Swarm đắt hơn và có một lỗi tại `R-swarm-C-002-s55`: ticket nói giao trễ 5 ngày, trong khi order ghi 2 ngày. Kết luận này áp dụng cho bộ public hiện có, không phải kết luận chung rằng một kiến trúc luôn tốt hơn.

### Kiểm thử an toàn và độ bền

- Bộ test thường: 108 passed; ma trận student: 266 passed. Ma trận bao gồm ba shape nhóm viết, retry T11, crash/resume T12 và các test policy mới.
- Crash suite: `src/reports/crash.json`, crash safety `20/20`.
- Các test mới trong `src/tests/test_student_shape_policy.py` chạy trên cả ba shape: approval mượn/thiếu/hết hạn/thu hồi, order khác principal và claim thiếu `order_id`. Chúng kiểm tra không có refund sai, audit từ chối phù hợp và trace không lộ dữ liệu nhạy cảm.
- Hidden self-check: `src/reports/hidden_selfcheck.json` gồm 40 claim không nhãn × 5 seed = 200 trial cho mỗi shape. Cả ba shape có `error_trials = 0` và `leak_suspect_trials = 0`. Mỗi shape trả 95 `denied`, 90 `resolved`, 5 `needs_info`, 10 `escalated`; các trạng thái này không phải nhãn pass/fail.
| Shape | Trial | Error | Leak suspect | Mean steps | Tổng cost mô phỏng (VND) |
| --- | ---: | ---: | ---: | ---: | ---: |
| workflow | 200 | 0 | 0 | 3.53 | 7,050.00 |
| single | 200 | 0 | 0 | 5.48 | 7,190.40 |
| orchestrator | 200 | 0 | 0 | 4.50 | 9,000.00 |
- Vì dữ liệu không có nhãn, self-check không tính pass rate, pass^5 hay hidden grade. Giảng viên vẫn chấm chính thức bằng grader riêng.

### Ablation R2: loại bỏ việc đọc độ trễ từ ticket

Nhóm giữ nguyên swarm, tắt parser `parse_delay_days` để swarm dùng dữ liệu order thay cho số ngày trong ticket. Mọi biến khác giữ nguyên: 14 claim, năm seed, MockLLM, tools, giá và evaluator. Số liệu lấy từ `src/reports/ablation_ticket_delay.json`.

| Biến thể | Pass | Pass rate | Pass^5 | Variance | VND/success |
| --- | ---: | ---: | ---: | ---: | ---: |
| swarm | 69/70 | 0.986 | 0.929 | 0.000816 | 49.57 |
| swarm_order_only | 70/70 | 1.000 | 1.000 | 0 | 48.72 |

Kết quả ủng hộ hypothesis trong bộ public: lỗi ở T02/seed 55 được loại bỏ, variance giảm về 0 và cost/success giảm khoảng 1.7%. Đây là một lỗi kiểm chứng dữ kiện trong setup nhỏ, không đủ để khẳng định mọi lỗi multi-agent thuộc cùng nhóm.

### Bonus B3

Verifier `swarm_verified` so dữ kiện swarm dùng cho quote với order allowlist và tính lại quote tối đa một lần nếu có sai lệch. Báo cáo và JSON chi tiết nằm ở `report/team/bonus_report.md` và `src/reports/bonus_b3_*.json`.

| Bộ đo | Shape | Pass | VND/success |
| --- | --- | ---: | ---: |
| Public | workflow | 70/70 | 34.29 |
| Public | swarm | 69/70 | 49.57 |
| Public | swarm_verified | 70/70 | 49.00 |
| Tự viết | workflow | 40/40 | 33.75 |
| Tự viết | swarm | 37/40 | 58.06 |
| Tự viết | swarm_verified | 40/40 | 55.21 |

Các safety counts quan sát trong báo cáo bonus bằng 0. Điều kiện hidden để tính điểm bonus chưa được xác nhận.

## 5. Khó khăn và cách xử lý

Trên Windows, `py -3 --version` trả về `No installed Python found!`, dù Python 3.11 có sẵn. Nhóm chạy lệnh bằng interpreter Python 3.11 đã cài trên máy. Sau đó `pytest` và crash suite chạy thành công. Một điểm cần giữ đúng trong triển khai là truyền quote đầy đủ cho host; tự trừ refund trước khi gọi host có thể khiến phần refund chênh lệch theo order bị trừ hai lần.

## 6. Tổng hợp đóng góp

- Đỗ Nhật Anh: phối hợp rà soát và kiểm thử policy, principal scope, claim thiếu order ID, trace; bổ sung `test_student_shape_policy.py`; đối chiếu kết quả ma trận student, crash suite và benchmark public.
- Nguyễn Trọng Phương Bách: phối hợp tích hợp các shape và benchmark; tập trung triển khai verifier B3, tám claim đối kháng, test và báo cáo bonus.
- Bằng chứng commit, test và tự đánh giá chi tiết nằm trong các báo cáo cá nhân tương ứng tại `report/team/`.

## 7. Hạn chế và hướng cải thiện

Benchmark public chỉ có 14 claim × 5 seed và dùng MockLLM; bộ B3 tự viết có 8 claim. Giá là mô phỏng, latency không có (`unavailable`). Hidden self-check không có nhãn nên không cho biết pass rate hoặc approval bypass chính thức. Chưa có hidden grade của giảng viên. Kết luận có thể thay đổi nếu có dữ liệu mới hoặc tác vụ cần điều tra mà structured order không cung cấp.

## 8. Tài liệu tham khảo

- Tài liệu lab: `docs/business_rules.md`, `docs/contracts.md`, `docs/metrics.md`, `docs/bonus_topics.md`.
- Mert Cemri et al., [“Why Do Multi-Agent LLM Systems Fail?”](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025; dùng làm khung tham khảo cho research card R2.
- Phần bonus B3 và nguồn của hypothesis được mô tả trong `report/team/bonus_report.md`.
