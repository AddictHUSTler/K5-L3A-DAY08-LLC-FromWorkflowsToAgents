# Báo cáo cá nhân — Nguyễn Trọng Phương Bách

## 1. Thông tin thành viên

- Họ tên: Nguyễn Trọng Phương Bách
- MSSV: 2A202603716
- Email: 26ai.bachntp@vinuni.edu.vn
- GitHub: [AddictHUSTler](https://github.com/AddictHUSTler)

## 2. Phần việc phụ trách

Cùng nhóm hoàn thiện ba shape và benchmark public; tập trung phát triển phần bonus B3: verifier kiểm tra dữ kiện của swarm trước khi settlement, bộ claim đối kháng và phân tích kết quả.

## 3. Đóng góp cụ thể

- Xây dựng `src/bonus/swarm_verified.py`: đối chiếu dữ kiện dùng cho quote với order allowlist; nếu phát hiện sai thì tính lại tối đa một lần. Trace chỉ ghi tên field đã sửa.
- Tạo tám claim đối kháng cùng world trong `src/bonus/cases.jsonl` và `src/bonus/world.json`.
- Thêm `src/tests/test_bonus_swarm_verified.py` để kiểm tra nhãn trên năm seed, sửa dữ kiện quote, chi phí sửa, trace, quote ban đầu bằng 0 và crash/resume/idempotency.
- Phân tích hiệu quả và giới hạn trong `report/team/bonus_report.md`: verifier cải thiện độ đúng trên các bộ đo hiện có nhưng có chi phí cao hơn workflow; kết quả chưa phải hidden grade.

## 4. Bằng chứng

- Các commit kỹ thuật liên quan: [6d1c7af](https://github.com/AddictHUSTler/K5-L3A-DAY08-LLC-FromWorkflowsToAgents/commit/6d1c7af) có phần triển khai ban đầu của các shape và verifier; [daa6183](https://github.com/AddictHUSTler/K5-L3A-DAY08-LLC-FromWorkflowsToAgents/commit/daa6183) sửa các shape; [25524f5 — add bonus submission](https://github.com/AddictHUSTler/K5-L3A-DAY08-LLC-FromWorkflowsToAgents/commit/25524f561ab3f569fcd41cef4aa8223c37796083) bổ sung B3, bộ case, test và reports; [c3b7633](https://github.com/AddictHUSTler/K5-L3A-DAY08-LLC-FromWorkflowsToAgents/commit/c3b7633) lưu hồ sơ CP5 và hidden self-check.
- Test: `python -m pytest -q tests/test_bonus_swarm_verified.py`.
- Lệnh tái lập: `python -m bonus.evaluate --extra-shape swarm_verified=bonus.swarm_verified:run_claim`.
- Reports sinh bằng script: `src/reports/bonus_b3_public.json` và `src/reports/bonus_b3_adversarial.json`.
- Hidden self-check CP5: `src/reports/hidden_selfcheck.json` có 200 trial mỗi student shape; workflow, single và orchestrator đều có 0 error và 0 `leak_suspect`.
- Run minh họa: `R-swarm_verified-C-002-s55` sửa trường hợp ticket nói trễ 5 ngày trong khi order ghi 2 ngày; `R-swarm_verified-B3-002-s55` sửa quote từ 0 lên 30.000 VND.
- Kết quả: public, swarm 69/70 và swarm_verified 70/70; bộ tự viết, swarm 37/40 và swarm_verified 40/40. Các kết quả này thuộc các bộ đo đã chạy, không thay thế hidden grade.

## 5. Công cụ và cách tự kiểm tra

Có dùng trợ lý AI để rà rubric, hỗ trợ triển khai và biên tập báo cáo; kết quả được tự kiểm bằng pytest, evaluator/benchmark của lab và các report JSON do script sinh ra. Runtime lab dùng MockLLM, không gọi model/API thật.

## 6. Tự đánh giá

Verifier sửa được lỗi tin số ngày trong ticket ở các bộ đo hiện có. Kết quả ủng hộ việc kiểm chứng dữ kiện trước settlement trong setup này, nhưng số claim còn ít, MockLLM không đại diện cho model sản xuất và latency không được đo. Cần hidden grade và dữ liệu rộng hơn trước khi kết luận về khả năng áp dụng thực tế.
