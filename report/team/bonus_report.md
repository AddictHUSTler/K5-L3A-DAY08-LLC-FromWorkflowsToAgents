# Bonus report: B3

- Topic + nguồn: Google Research 2026, *Towards a Science of Scaling Agent Systems*, error amplification; slide 17, 22, 42 theo `docs/bonus_topics.md`. Code biến thể dựa trên `src/lab8/shapes/swarm_reference.py`; policy của bộ case dùng lại từ public.
- CLAIM: theo đề bài, agent độc lập có thể khuếch đại lỗi tới 17,2×, orchestration tập trung còn 4,4×.
- BOUNDARY: các tỷ lệ thuộc setup nghiên cứu nguồn, không phải kết quả LogiX; thí nghiệm này chỉ kiểm verifier bằng code trên MockLLM, không tái lập tỷ lệ đó.
- HYPOTHESIS: một lượt kiểm dữ kiện trước settlement sửa lỗi tin ticket của swarm, đưa correctness về bằng workflow nhưng vẫn tốn thêm cost.
- Biến cố định: claim, seed `11,22,33,44,55`, policy, giá, evaluator chính thức, SQLite mới cho từng trial. Biến thay đổi: thêm verifier; giữ peer/parse/draft, investigator, lỗi theo seed và host của swarm.
- Lệnh tái lập (từ thư mục gốc; dùng Python trong môi trường đã cài `src/requirements.txt`):

```bash
cd src
python -m pytest -q
python -m bonus.evaluate --extra-shape swarm_verified=bonus.swarm_verified:run_claim
python -m lab8.check_submission
```

- File report: `src/reports/bonus_b3_public.json`, `src/reports/bonus_b3_adversarial.json`; do script gọi `lab8.benchmark.run_benchmark` và ghi JSON, không sửa tay. Run id minh họa: `R-swarm_verified-C-002-s55`, `R-swarm_verified-B3-002-s55`.
- Chạy trực tiếp bằng CLI chính thức cũng được: `python -m lab8.benchmark --shapes workflow,swarm,swarm_verified --extra-shape swarm_verified=bonus.swarm_verified:run_claim --seeds 11,22,33,44,55 --out reports/bonus_b3_cli.json`. Thêm `--cases bonus/cases.jsonl --world bonus/world.json` để đo bộ tự viết.

## Kết quả

Số liệu từ `by_shape` của hai report trên. Cost/success gồm cả chi phí trial fail; VND mô phỏng. Pass^5 là tỷ lệ claim pass cả năm seed; variance tính trên pass rate từng seed.

| Bộ | Shape | Pass | Pass^5 | Variance | VND/success | Override |
| --- | --- | --- | --- | --- | --- | --- |
| Public | workflow | 70/70 | 1.000 | 0 | 34.29 | 0 |
| Public | swarm | 69/70 | 0.929 | 0.000816 | 49.57 | 0 |
| Public | swarm_verified | 70/70 | 1.000 | 0 | 49.00 | 1 |
| Tự viết | workflow | 40/40 | 1.000 | 0 | 33.75 | 0 |
| Tự viết | swarm | 37/40 | 0.625 | 0.022500 | 58.06 | 0 |
| Tự viết | swarm_verified | 40/40 | 1.000 | 0 | 55.21 | 6 |

Mỗi dòng có secret leak = 0, PII leak = 0, approval bypass = 0, trace invalid = 0 trong `safety_counts`, quan sát đủ mọi trial. Scanner kiểm cả kết quả và artifact; approval kiểm độc lập trên ledger bằng host policy. Đây là phép đo public/tự viết, không phải hidden grade hay chứng nhận crash.

Verifier so tất cả field allowlist của order, gồm `delay_days`, `status`, `damage_verified`, phí ship và paid. Nếu lệch, gọi `compute_compensation` đúng một lần từ order có cấu trúc; tính thêm tool cost. Kiểm trước cả nhánh quote = 0 để sửa được trường hợp ticket nói thiếu. Không gọi thêm model. Host vẫn kiểm approval, idempotency và trần theo đơn bằng quote đầy đủ.

Trace minh họa được nhúng trong trường `example_trace` của report public: seed 55 của C-002 có `model_override` delay 5, rồi `verifier_override` với `fields=["delay_days"]`, `repair_round=1`; quote cuối 0, không refund. Trace chỉ ghi dữ kiện allowlist, không ticket/secret/PII. Sáu override trên bộ tự viết chỉ sửa ba trial fail; ba lần còn lại không đổi kết quả do status, damage hoặc approval đã quyết định.

## Kết luận

Ủng hộ hypothesis trong hai bộ đo: verifier bằng workflow về pass/pass^5/variance, nhưng cost/success cao hơn khoảng 43% public và 64% tự viết. Cost/success giảm so với swarm vì có thêm success, dù mỗi lượt sửa phải trả thêm tool cost.

Trong setup này, swarm không cho thấy giá trị bổ sung về quyết định tiền: verifier khôi phục dữ liệu, code quote quyết định entitlement, host quyết định ghi. Peer/parse/draft vẫn tồn tại nhưng chưa chứng minh được lợi ích tương xứng. Giữ workflow làm shape chính. Kết luận có thể đảo khi có tác vụ điều tra văn bản mà structured order thiếu thông tin và swarm cải thiện correctness đủ bù cost trên phép đo mới.

## Giới hạn

MockLLM có lỗi delay cố định theo seed, không mô phỏng đầy đủ lỗi model thật. Status/damage không bị swarm sửa trong runtime hiện tại; test chủ động làm sai từng field để kiểm verifier, không coi đó là cải thiện đã đo trên model. Tám claim tự viết có nhãn viết tay theo `docs/business_rules.md`, không dùng quote sinh nhãn; số claim nhỏ và có chủ đích nên không đại diện phân bố thực. Giá mô phỏng, latency không đo.
