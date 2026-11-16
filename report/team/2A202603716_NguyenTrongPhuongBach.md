# Báo cáo cá nhân — MSSV_HoTen

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Nguyễn Trọng Phương Bách
- MSSV: 2A202603716
- Email: 26ai.bachntp@vinuni.edu.vn
- GitHub: 

## 2. Phần việc phụ trách

Phần B3: verifier trước settlement của swarm, bộ case đối kháng, test và báo cáo bonus. 

## 3. Đóng góp cụ thể

- Commit chính: add bonus submission
- Code: `src/bonus/swarm_verified.py`, `src/bonus/evaluate.py`; tám claim trong `src/bonus/cases.jsonl`, world trong `src/bonus/world.json`.
- Test thêm: `src/tests/test_bonus_swarm_verified.py` kiểm nhãn viết tay trên năm seed, sửa từng field quote, chi phí lượt sửa, trace, quote ban đầu bằng 0 và crash/resume/idempotency.
- Quyết định thiết kế của patch: giữ luồng swarm; so dữ kiện với order allowlist trước nhánh denied/write; quote lại tối đa một lần, ghi `verifier_override` chỉ gồm tên field. Tiền do code tính; quote đầy đủ đi vào host để tránh trừ prior refund hai lần.

## 4. Bằng chứng

- Lệnh từ `src/`: `python -m pytest -q tests/test_bonus_swarm_verified.py`.
- Tái lập đo: `python -m bonus.evaluate --extra-shape swarm_verified=bonus.swarm_verified:run_claim`.
- Report sinh bằng script: `src/reports/bonus_b3_public.json`, `src/reports/bonus_b3_adversarial.json`; phân tích trong `report/team/bonus_report.md`.
- Run id: `R-swarm_verified-C-002-s55` (ticket 5 ngày, order 2 ngày, sửa quote về 0); `R-swarm_verified-B3-002-s55` (ticket nói thiếu, sửa quote từ 0 lên 30.000).
- Public: swarm 69/70 → verified 70/70; tự viết: 37/40 → 40/40. Bảy override tổng cộng; safety counts quan sát đều 0. Đây không phải kết quả hidden.
- Link commit: 
## 5. Công cụ AI đã dùng

- Công cụ AI: Codex; hỗ trợ đọc rubric/rules/submission, viết code verifier, test, case và báo cáo. Runtime lab chỉ dùng MockLLM, không gọi API model thật.

## 6. Tự đánh giá

Phần B3 đã có verifier, test và số liệu so sánh. Verifier sửa được lỗi tin ticket trong bộ đo, nhưng chi phí vẫn cao hơn workflow. Hạn chế là mới kiểm tra trên MockLLM và số claim ít; cần thêm dữ liệu để đánh giá khả năng áp dụng thực tế.
