# Decision record

- Shape chọn: workflow
- Commit hash: 35eccc8 (commit của code dùng cho benchmark public)
- Run id dẫn chứng: R-workflow-C-001-s11; src/reports/benchmark.json
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0
- Cost per success (mô phỏng, VND): 34.29
- Crash safety: 20/20 (src/reports/crash.json, host/swarm); T12 kiểm crash/resume riêng cho cả ba implementation.
- Secret leak / approval bypass: 0 vi phạm được phát hiện trong 70 trial workflow theo assertion public; test host và handoff đều pass.
- Hidden self-check (không nhãn): 40 claim × 5 seed; workflow, single và orchestrator đều có 0 error và 0 `leak_suspect`. Kết quả này không phải hidden pass rate.

## Vì sao shape này

Chọn workflow: trên cùng 14 claim × 5 seed, workflow, single và orchestrator đều đạt 70/70; workflow có cost/success thấp nhất (34.29 VND, so với 34.95 của single và 43.57 của orchestrator). Swarm đạt 69/70 và cost/success cao nhất (49.57 VND); lỗi duy nhất là tin ticket nói trễ 5 ngày trong khi order ghi 2 ngày tại T02, seed 55. Workflow có luồng xác định, không cần thêm model hay delegation cho bộ case này.

| Shape | Pass | Pass^5 | Seed min–max | Variance | VND/success |
| --- | --- | --- | --- | --- | --- |
| workflow | 70/70 | 1.000 | 1.000–1.000 | 0 | 34.29 |
| single | 70/70 | 1.000 | 1.000–1.000 | 0 | 34.95 |
| orchestrator | 70/70 | 1.000 | 1.000–1.000 | 0 | 43.57 |
| swarm | 69/70 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 |

Nguồn: `src/reports/benchmark.json`. Cost/success tính cả trial fail. Swarm sai tại `R-swarm-C-002-s55`: tin ticket ghi trễ 5 ngày trong khi order ghi 2 ngày.

## Có đáng đổi lấy multi-agent không

Chưa có lợi ích về correctness trong kết quả này. Orchestrator đắt hơn workflow khoảng 27%; swarm khoảng 45%. Chỉ đổi khi có bước điều tra độc lập hoặc yêu cầu mới mà workflow xử lý kém, và phép đo cùng điều kiện cho thấy lợi ích đủ bù cost, vẫn giữ các cổng approval, leak và crash.

## Trace và bằng chứng

Workflow ghi `claim` (found/has_order), `order` (visible/reason), `quote`, `refund` (ok/reason) và `crash` khi được inject. Không ghi raw claim/order, ticket, secret, header, phone, địa chỉ, tên hàng hay internal note.

Trace ở `traces/<run_id>.json`, có run_id khớp và danh sách events. Evaluator quét trace, file cùng prefix và kết quả; implementation không ghi debug ra vị trí khác. Ledger/audit cùng assertion public quyết định pass.

## Giới hạn

Kết luận áp dụng cho 14 claim public và 5 seed với MockLLM. Single hiện chọn tool bằng code; chênh lệch giữa bốn shape không tách riêng ảnh hưởng topology khỏi prompt/tool calls. Giá là mô phỏng; latency: `unavailable`.
