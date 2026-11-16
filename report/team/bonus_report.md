# Bonus report: B3

- Topic + nguồn (tên, năm, slide): Google Research 2026, error amplification; slide 17, 22, 42, theo [hướng dẫn B3](../../docs/bonus_topics.md#b3--verifieraggregator-chống-khuếch-đại-lỗi).
- CLAIM của nguồn (1 câu): Kiểm chứng tập trung có thể giảm khuếch đại lỗi giữa các agent.
- BOUNDARY (model / dataset / setup): Kết quả nguồn thuộc các setup nghiên cứu; không dùng hệ số 17,2× / 4,4× làm dự đoán cho lab.
- HYPOTHESIS trên LogiX: Kiểm tra facts trước khi ghi sẽ sửa lỗi ticket-delay, đạt correctness bằng workflow nhưng cost cao hơn.
- Biến cố định / biến thay đổi: Cùng world, claim, 5 seed, MockLLM, tools, giá và evaluator; chỉ thêm verifier vào swarm. Giữ nguyên peer/parse/draft và lỗi tham chiếu. Mỗi trial dùng SQLite mới.
- Lệnh tái lập (copy-paste được, chạy trong `src/`, sau khi activate môi trường):

```bash
python -m bonus.measure
python -m pytest -q tests/test_bonus_verifier.py
```

- File report + run id: [src/reports/bonus_verifier.json](../../src/reports/bonus_verifier.json); `R-swarm_verified-C-002-s55`. Script đăng ký variant qua cùng cơ chế `--extra-shape`, dùng benchmark và evaluator có sẵn.

## Kết quả

14 claim public và 8 claim đối kháng × seed 11/22/33/44/55. Nhãn đối kháng viết tay theo README, không gọi quote để sinh nhãn.

| Bộ case | Shape | Pass | Pass rate | Pass^5 | Variance | VND/success |
| --- | --- | --- | --- | --- | --- | --- |
| Public | workflow | 70/70 | 1.000000 | 1.000000 | 0 | 34.29 |
| Public | swarm | 69/70 | 0.985714 | 0.928571 | 0.000816 | 49.57 |
| Public | swarm_verified | 70/70 | 1.000000 | 1.000000 | 0 | 49.00 |
| Đối kháng | workflow | 40/40 | 1.000000 | 1.000000 | 0 | 35.00 |
| Đối kháng | swarm | 37/40 | 0.925000 | 0.625000 | 0.022500 | 58.00 |
| Đối kháng | swarm_verified | 40/40 | 1.000000 | 1.000000 | 0 | 55.15 |

Verifier can thiệp 1 lần trên public, 6 lần trên đối kháng; tối đa một lần/trial. Có lần sửa facts mà quote không đổi. Mọi shape ở cả hai bộ có **0 secret leak, 0 PII leak, 0 approval bypass, 0 duplicate refund**. Safety counts lấy từ artifact và ledger; approval được đối chiếu với nhãn `approval_ok`.

Trace minh họa được nhúng trong report: `R-swarm_verified-C-002-s55` có `model_override` delay 5, rồi `verifier_override` sửa quote 20.000 → 0 theo order trễ 2 ngày; kết quả denied, không refund.

10 test bonus kiểm tra nhãn ở cả 5 seed, từng fact (`delay_days`, `status`, `damage_verified`), nhánh không cần sửa và crash/resume/retry với đúng một refund và một audit committed.

## Kết luận

Ủng hộ hypothesis trên hai bộ đo: verifier đưa correctness và variance về bằng workflow. Cost/success vẫn cao hơn workflow khoảng 43% trên public và 58% trên đối kháng. Cost/success thấp hơn swarm gốc vì giảm trial fail, dù mỗi lần sửa cần thêm một tool call.

Verifier quyết định facts dùng để quote; peer/parse/draft chưa cho thấy giá trị thêm trong task này. Giữ lựa chọn workflow. Quyết định có thể đổi nếu có bước điều tra độc lập giúp xử lý thêm case và lợi ích đo được bù chi phí.

## Giới hạn

MockLLM, giá mô phỏng, latency không đo; 22 claim và lỗi delay được cài sẵn. Ticket nói dối status/damage hiện không được swarm chuyển thành facts; test riêng gây sai từng field để kiểm verifier. Kết quả không tái lập hệ số khuếch đại lỗi của nguồn và không suy rộng sang mọi hệ multi-agent.
