# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`):

## 2. Mục tiêu và cách tiếp cận

Nhóm hiểu bài toán thế nào, chia việc ra sao, thứ tự làm bốn shape.

...

## 3. Giải pháp

| Shape | Luồng thực thi |
| --- | --- |
| workflow | Đọc claim → kiểm quyền sở hữu order → tính quote → gọi host nếu quote dương → trả kết quả từ ledger. Không gọi model. |
| single | Đọc claim → ReAct chỉ đọc, tối đa 8 bước → lấy order → tính quote bằng code → gọi host. Chạm giới hạn bước trả failed. MockLLM được gọi nhưng lựa chọn tool hiện do code cố định. |
| orchestrator | Đọc claim → tạo handoff → lookup_order rồi compute_compensation → gọi host. Runner hiện chạy tuần tự. |
| swarm | Đọc claim → peer/parse bằng MockLLM → investigator đọc order và policy, tính quote → draft → gọi host. Seed 55 có thể ghi đè delay bằng nội dung ticket. |

`compute_compensation` dùng order và policy hiện hành tại 2026-11-15. Quote đầy đủ được truyền vào `issue_refund`; host áp approval, paid cap và trừ khoản đã hoàn theo order. Quote bằng 0 không gọi refund.

## Quyền và handoff

Tool đọc bị giới hạn theo principal; order view không chứa phone, địa chỉ, tên hàng hay internal note. `issue_refund` và `append_audit` chỉ thuộc host, không có trong registry của worker.

`handoff.v1` chỉ giữ request/claim ID, principal scope, task, facts cho phép, danh sách tool đọc và giới hạn output. Orchestrator gửi `facts={}`, scope `owner_order_only`, giới hạn 400 token và hai tool theo thứ tự trên. Allowlist bằng code lọc secret, header và lịch sử parent khỏi handoff.

## Ghi tiền và khôi phục

Mọi shape gọi cùng `durability.issue_refund`. Host kiểm approval đúng claim, hiệu lực và trần theo order trong transaction. Ledger dùng khóa `refund:{claim_id}` để chống ghi trùng; amount khác khi retry trả conflict và giữ khoản cũ.

Crash sau effect, trước checkpoint được truyền ra ngoài để resume kiểm ledger. Kết quả cuối lấy refund và audit thực tế qua `finish`; mọi nhánh trả bình thường đều ghi trace mới với các field an toàn.

## 4. Kết quả

Bảng so sánh 4 shape trên bộ public (từ `src/reports/benchmark.json`): pass rate, pass^5, seed min–max, variance, cost/success, mean/p95 steps. Kèm crash safety (`src/reports/crash.json`) và, nếu có, kết quả tự kiểm trên `student_drop/`.

...

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

Lỗi gặp phải (kèm lệnh, output hoặc ảnh chụp) và cách nhóm xử lý.

...

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`. Nêu thêm giới hạn của nhóm và điều kiện làm kết luận thay đổi.

...

## 8. Tài liệu tham khảo

...
