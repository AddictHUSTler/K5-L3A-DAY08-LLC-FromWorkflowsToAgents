# Architecture

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
