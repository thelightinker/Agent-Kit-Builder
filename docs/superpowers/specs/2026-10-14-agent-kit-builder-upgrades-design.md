
# Upgrade Spec — Agent Kit Builder

- **Repo audit:** `thelightinker/Agent-Kit-Builder`, nhánh `main`, commit `5faeb07` (clone nông, 50 commit)
- **Ngày audit:** 2026-10-14
- **Phạm vi:** chỉ audit, nghiên cứu, viết spec. Không sửa repo gốc. Mọi lệnh chạy trong bản clone tạm; các file bị test ghi đè trong clone đã được `git checkout` lại.
- **Trạng thái:** DRAFT, chờ bạn review trước khi sang bước lập plan triển khai.

---

## 0. Cách đọc tài liệu

Mỗi con số trong mục Bằng chứng đều lấy từ lệnh đã chạy hoặc file đã đọc trong phiên này. Chỗ nào là **ước lượng** thì ghi rõ. Phần "Giới hạn của audit" ở cuối nói rõ những gì chưa kiểm tra.

---

## 1. Hiểu biết về mục tiêu (để bạn sửa nếu sai)

|                                   | Nội dung                                                                                                                                                                                                                                                                                                                         |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bạn nói**               | Audit toàn repo bằng `domain-profiling`; tìm đòn bẩy 80/20; đúng 5 nâng cấp; xếp hạng theo giá trị, khả năng triển khai, chi phí token/độ phức tạp; không over-engineer; không sửa code.                                                                                                               |
| **Giả định của mình**  | (a) Người dùng chính của repo là bạn và những người bạn chia sẻ kit cho, chạy trên Antigravity IDE, có thể thêm Cursor/Claude. (b) "Mạnh hơn vượt bậc" ưu tiên **độ tin cậy** trước, rồi tới năng lực, rồi trải nghiệm. (c) Ràng buộc ngầm: không viết lại kiến trúc đã ổn. |
| **Thành công nghĩa là** | Sau 5 nâng cấp, repo tự chứng minh được nó hoạt động (không còn "báo xanh giả"), chạy được trên máy khác, tốn ít context hơn mỗi lượt, và có bài test thật cho thứ nó sinh ra.                                                                                                                  |

---

## 2. Domain Profile của chính repo (theo `domain-profiling`)

### 2.1 Core Verbs & Risk Profile

| Core Verb                                                     | Precision/Creativity   | Failure Severity                    | Kiểm chứng được tự động?                     |
| :------------------------------------------------------------ | :--------------------- | :---------------------------------- | :--------------------------------------------------- |
| Tạo kit mới (`/create-kit`)                               | Creativity + Precision | Critical (sinh ra sản phẩm)       | Một phần: script cho cấu trúc, LLM cho nội dung |
| Sửa kit (`/refactor-kit`)                                  | Precision              | Critical (ghi đè)                 | Có (snapshot, diff)                                 |
| Kiểm định (`/validate-kit`)                              | Precision              | Critical (báo sai = mất tin cậy) | Có (`validate_kit.py`)                            |
| Biên dịch contract (routing, invariants, state)             | Precision              | Serious                             | Có                                                  |
| Xuất sang nền tảng khác (`export_kit.py`)               | Precision              | Medium                              | Có                                                  |
| Ghi nhớ bài học (`/remember-kit`, `distill_memory.py`) | Creativity             | Low–Medium                         | Khó                                                 |

**Rủi ro chủ đạo:** **Omission** (kit thiếu cấu phần mà không ai biết), **Mutation** (refactor/sync ghi đè file), **Arithmetic nhẹ** (đếm số, hash, version phải khớp nhau).

**Archetype cần có:** Negative Completeness Matrix (đã có phần nào), Transactional Mutation (đã có `snapshot_manager`, `atomic_promoter`), Deterministic Computation Guard cho số đếm/version (đang thiếu, xem nâng cấp 5).

### 2.2 Failure Mode của chính repo (đối chiếu `references/failure-modes.md`)

| Failure Mode trong tài liệu                                     | Có xảy ra ở chính repo?               | Bằng chứng                                                                                                                                                      |
| :---------------------------------------------------------------- | :---------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phantom Routing (F5)** — contract JSON rỗng nhưng pass | **Có**                             | `routing_index.json` có `capabilities: {}`, `intent_map: {}`; `state_schema.json`, `evidence_schemas.json`, `task_classifier_index.json` đều rỗng |
| **Provider Lock-in**                                        | **Có** (khóa vào máy tác giả) | Đường dẫn `C:\Users\nhdcb\...` trong 6 file                                                                                                                 |
| **Redundant Constraints**                                   | **Có**                             | `core-guardrails` và `collaboration-protocol` đều `always_on` và lặp Grounding/HUD/Worker Briefing                                                     |
| **Lens Stuffing / Over-Engineered**                         | **Có** ở mức hệ thống          | 28.5 KB nạp mỗi lượt; 2,137 dòng script evolution/lifecycle chỉ được 2 workflow gọi                                                                     |
| **Safety theatre** (cơ chế có nhưng không enforce)     | **Có**                             | README ghi "100% PASS" nhưng validator tự đánh giá fail                                                                                                      |

### 2.3 Topology

Một Orchestrator (`kit-architect`) + 5 Role Profile + 11 skill + 7 workflow. Mức này hợp lý cho nhiệm vụ. Vấn đề không nằm ở topology mà ở **lớp xác minh và tính nhất quán**.

---

## 3. Kết quả audit (tóm tắt có số liệu)

| #   | Phát hiện                                   | Con số / bằng chứng                                                                                                                                                                                                                                                              |
| :-- | :-------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A1  | Validator tự kiểm repo → **FAIL**    | `validate_kit.py .agents`: 14 error (3 thiếu frontmatter ở `skill-creator`, 2 link skill hỏng, 4 link hỏng ở `golden-examples/README.md`, 3 script `--help` thoát mã 1, 2 lệch số đếm ARCHITECTURE)                                                              |
| A2  | Bộ test tự fail                             | 101 test chạy: **8 failure + 9 error = 17 lỗi**. 8 module test không import được (đã xác nhận ở `test_evolution_engine`: `import feedback_collector`, module này không còn tồn tại)                                                                       |
| A3  | README báo xanh giả                         | Badge tĩnh "Toolkit Validation 100% PASS" và "Unit Tests 17/17 Passed" (đọc từ URL shields.io), không có CI (`.github/` không tồn tại)                                                                                                                                  |
| A4  | Benchmark tự mâu thuẫn                     | `benchmark_behavior.py`: 4 dòng chaos in `✗`, nhưng verdict cuối in "4/4 Chaos Failure Injection scenarios passed"                                                                                                                                                          |
| A5  | Test ghi đè file đang theo dõi bởi git   | Sau khi chạy test, `git diff` cho thấy đổi `manifest.lock.json` (235 dòng), `ARCHITECTURE.md`, `execution_policy.json`                                                                                                                                                 |
| A6  | Đường dẫn tuyệt đối của tác giả     | 6 file chứa `nhdcb`: `kit-architect.md`, `create-kit.md`, `refactor-kit.md`, `skill-architecting`, `kit-verifying`, `golden-examples/README.md`. Bài học đã ghi ở `feedback-history.md` ngày 2026-09-06, lỗi cùng loại vẫn còn                          |
| A7  | Phụ thuộc ngoài không khai báo           | `superpowers:brainstorming/writing-plans/executing-plans`, `agy-customizations`, `ponytail` được gọi trong rule/workflow nhưng không có trong repo; `mcp_config.json` còn `YOUR_API_KEY`                                                                          |
| A8  | Context nạp mỗi lượt quá lớn            | 3 rule `always_on` (15,462 B) + orchestrator (13,053 B) = **28,515 B**. CHANGELOG 2026.8.17 từng tuyên bố rule "dưới 3 KB". Ước lượng ~9–12K token (tiếng Việt, **chưa đo bằng tokenizer**)                                                            |
| A9  | "Behavioral eval" thực chất là regex tĩnh | `eval_runner.py` chỉ có 4 loại assertion: `regex_match`, `contains_keywords`, `forbidden_keywords`, `min_sections` trên file. `evals.json` còn ghi `agentkit-builder` v3.0 với từ vựng Tier/Lens của bản cũ                                                |
| A10 | Không có kit mẫu chạy end-to-end          | Không có thư mục kit đầu ra nào trong repo; `golden-examples/` là mô tả markdown, không phải kit để chạy `validate_kit.py`                                                                                                                                       |
| A11 | Trôi từ vựng và số liệu                 | Version: README 2026.7.18 / 2026.8.24, `VERSION` 2026.8.22. Mode: orchestrator liệt kê 5, `dynamic-routing` có 10. Phân cấp: Tier 1–3 / Micro–Full Suite / `SUITE_BUILD`. Skill: README "10", thực tế 11. `failure-modes.md` đề "v3.0"                           |
| A12 | Phần phụ nặng hơn phần lõi              | `ui-ux-pro-max` 3.8 MB, `skill-creator` vendored 272 KB (485 dòng `SKILL.md`), `scripts/` 1.2 MB; lõi tạo kit chỉ là ~300 KB markdown                                                                                                                                  |
| A13 | Nhóm script evolution lớn, ít người gọi | 9 script (evolution_*, equip_evolution, snapshot_manager, lifecycle_engine, upgrade_gate_evaluator, convergence_engine) = 2,137 dòng; chỉ `create-kit` và `evolve-kit` tham chiếu. Convergence engine báo `converged=False` trên chính "Healthy Kit Baseline" của nó |

**Nút thắt chung:** repo có rất nhiều cơ chế kiểm tra, nhưng **không có thứ nào buộc chúng được chạy và buộc kết quả phải trung thực**. Đó là nguyên nhân gốc của A1–A5, A11.

---

## 4. Năm nâng cấp, xếp hạng

Công thức ROI lấy từ `domain-profiling` (ngưỡng chấp nhận ≥ 1.25). Điểm dưới đây là **ước lượng định tính** của mình (Năng lực tăng ÷ Chi phí token + độ phức tạp), không phải số đo.

| Hạng | Nâng cấp                                                          |  Giá trị  |  Khả thi  |  Chi phí token/độ phức tạp  | ROI ước lượng |
| :---: | :------------------------------------------------------------------ | :---------: | :---------: | :-------------------------------: | :---------------: |
|   1   | **Truth Gate**: một lệnh verify + CI, báo cáo trung thực |  Rất cao  |  Rất cao  | Thấp (không tốn token runtime) |       ~3.0       |
|   2   | **Portability & Dependency Contract**                         |     Cao     |  Rất cao  |            Rất thấp            |       ~2.5       |
|   3   | **Golden Kit E2E + Eval thật**                               |  Rất cao  | Trung bình |      Trung bình (một lần)      |       ~2.0       |
|   4   | **Context Diet**: rule always-on ≤ ngân sách               |     Cao     | Trung bình |      Giảm token mỗi lượt      |       ~1.8       |
|   5   | **SSOT cho số đếm, version, mode, từ vựng**              | Trung bình |     Cao     |               Thấp               |       ~1.4       |

**Thứ tự triển khai khuyến nghị** khác thứ tự giá trị một chút: 1 → 2 → 3 → 4 → 5. Lý do: nâng cấp 4 sửa nội dung prompt nên cần lưới an toàn của 1 và 3 trước.

---

### Nâng cấp 1 — Truth Gate: một lệnh verify, CI, báo cáo không nói dối

**Bằng chứng:** A1, A2, A3, A4, A5.

**Vấn đề.** Repo tự tuyên bố "100% PASS" nhưng validator của chính nó báo 14 lỗi và 17/101 test lỗi. Benchmark in verdict cố định bất kể kết quả. Test ghi đè file git theo dõi nên mỗi lần chạy làm bẩn working tree. Không có CI nên không gì chặn commit hỏng. Mọi cơ chế "Auto-Healing" và "Evidence Gate" phía trên đều đứng trên nền này.

**Giải pháp đề xuất.**

1. Thêm một entrypoint duy nhất (ví dụ `python .agents/scripts/verify_all.py`) chạy theo thứ tự: validator → unit test → benchmark. Thoát mã khác 0 nếu bất kỳ bước nào fail.
2. Verdict của `benchmark_behavior.py` **tính từ kết quả từng case**, không còn chuỗi cố định.
3. Test chạy trên **bản sao tạm** (temp dir) của kit, không ghi vào `.agents/` thật. Thêm một test "working tree sạch sau khi chạy test".
4. Xử lý 17 test lỗi theo quy tắc: test của module đã xóa (`feedback_collector`) thì **xóa test** hoặc port sang `feedback_hub`; còn lại thì sửa nguyên nhân (ví dụ frontmatter `skill-creator`).
5. Thêm `.github/workflows/verify.yml` chạy `verify_all.py` khi push/PR. Thay badge tĩnh bằng badge trạng thái workflow.
6. Quyết định rõ cho nhóm evolution (A13): hoặc phục hồi test và giữ, hoặc đánh dấu `experimental` và loại khỏi đường chạy mặc định. Chọn phương án nào thì ghi vào `tech-decisions.md`.

**Tác động kỳ vọng.** Mọi hồi quy từ nay bị chặn ở commit. Người dùng mới tin được báo cáo. Giảm phần lớn lỗi A6, A11 tái phát vì validator sẽ được chạy tự động.

**Trade-off.**

- Sửa 17 test có thể lộ thêm lỗi thật đang bị che. Đây là chi phí cần trả, không phải rủi ro.
- CI cần Python 3.12 và có thể chậm (bộ test hiện mất ~34 giây). Chấp nhận được.
- Quyết định giữ hay bỏ nhóm evolution là việc của bạn; spec không tự quyết.

**Tiêu chí thành công (nhị phân).**

- [ ] `verify_all.py` thoát mã 0 trên `main`.
- [ ] 0 error ở `validate_kit.py .agents`.
- [ ] 0 test lỗi/failure; không còn `_FailedTest`.
- [ ] Sau khi chạy toàn bộ test, `git status --short` rỗng.
- [ ] Cố tình làm hỏng một case benchmark thì verdict cuối đổi sang FAIL (kiểm bằng một test).
- [ ] Badge README lấy từ CI, không còn badge tĩnh.

---

### Nâng cấp 2 — Portability & Dependency Contract

**Bằng chứng:** A6, A7, A12 (một phần).

**Vấn đề.** Orchestrator và 2 workflow bắt buộc nạp `skill-creator` từ `C:\Users\nhdcb\.gemini\...`. Trên máy khác, đường dẫn này không tồn tại, trong khi bản `skill-creator` đã nằm sẵn ở `.agents/skills/skill-creator/`. Đây là đúng lỗi "Grounding Gate fail silently" mà `feedback-history.md` đã ghi nhận ngày 06/09 nhưng chưa có rào chắn nào ngăn tái phát. Ngoài ra repo gọi 4 thứ bên ngoài (`superpowers:*`, `agy-customizations`, `ponytail`, context7) mà không khai báo hay có phương án thay thế.

**Giải pháp đề xuất.**

1. Thay mọi đường dẫn tuyệt đối bằng đường dẫn tương đối `.agents/skills/skill-creator/SKILL.md` (6 file).
2. Thêm luật linter `path.absolute_user_path` vào `validate_kit.py` để không tái phát. Validator đã có `markdown.missing_link`, chỉ cần bổ sung luật bắt thẳng mẫu `C:\Users`, `/Users/`, `/home/<tên>`.
3. Thêm file `DEPENDENCIES.md` (hoặc mục trong `manifest.json`) liệt kê từng phụ thuộc ngoài: tên, dùng ở đâu, **bắt buộc hay tùy chọn**, và hành vi dự phòng khi thiếu (ví dụ: không có `superpowers:brainstorming` thì dùng quy trình hỏi-đáp tối thiểu ngay trong workflow).
4. Thay `YOUR_API_KEY` trong `mcp_config.json` bằng biến môi trường hoặc ghi rõ "tùy chọn".
5. Thêm bước preflight nhẹ ở đầu `/create-kit`: kiểm tra các file/skill bắt buộc tồn tại, báo rõ thứ nào thiếu thay vì lỗi im lặng.

**Tác động kỳ vọng.** Repo chạy được ngay sau khi clone trên máy khác; lỗi thiếu phụ thuộc hiện ra rõ ràng thay vì sinh kit kém chất lượng không báo.

**Trade-off.**

- Phương án dự phòng cho `superpowers:*` thêm vài dòng prompt vào workflow. Giữ ngắn.
- Nếu bạn cố ý muốn dùng `skill-creator` bản plugin cài ngoài (phiên bản mới hơn), cần nêu rõ cơ chế ưu tiên: bản vendored là mặc định, bản ngoài là ghi đè tùy chọn.

**Tiêu chí thành công.**

- [ ] `grep -rE "C:\\\\Users|nhdcb" .agents` (trừ dữ liệu CSV không liên quan) trả về 0 kết quả.
- [ ] Thêm một đường dẫn `C:\Users\x` giả vào một skill thì `validate_kit.py` fail với luật mới (test).
- [ ] Clone sạch vào thư mục khác, chạy `/create-kit` với `superpowers` vắng mặt: preflight báo rõ, workflow dùng phương án dự phòng, không dừng im lặng.
- [ ] Mọi phụ thuộc ngoài trong repo đều có dòng trong `DEPENDENCIES.md` (kiểm bằng script grep).

---

### Nâng cấp 3 — Golden Kit E2E và Eval kiểm chứng thật

**Bằng chứng:** A9, A10, và F5 trong 2.2.

**Vấn đề.** Sản phẩm của repo là **kit đầu ra**, nhưng repo không có kit mẫu nào để chạy toàn bộ chuỗi compile → validate → export. Hậu quả: 7 script compiler (~1,000 dòng) chạy trên chính repo cho kết quả **rỗng** (Phantom Routing) mà không ai phát hiện, vì không có ca nào buộc chúng phải ra kết quả khác rỗng. Eval hiện tại chỉ so regex/từ khóa trên file, và bộ `evals.json` còn theo phiên bản cũ.

**Giải pháp đề xuất.**

1. Thêm **một** kit fixture nhỏ gọn, cố định (`tests/fixtures/golden-kit/`): ví dụ kit Standard 1 agent + 2 skill + 1 workflow. Ưu tiên nhỏ và dễ đọc hơn là "đẹp".
2. Thêm test E2E: chạy 6 compiler → `validate_kit.py` → `export_kit.py` trên fixture, rồi khẳng định các artifact **không rỗng** (routing có ≥ 1 capability, state schema có key, v.v.).
3. Thêm luật validator `routing.empty_capabilities` thành lỗi cứng cho kit có ≥ 1 agent (luật này đã được mô tả trong `failure-modes.md` F5 nhưng chưa thấy áp dụng cho trường hợp rỗng của chính repo). Với chính `.agents/` (Creator), hoặc khai báo `routing_exempt` có lý do, hoặc điền contract thật.
4. Làm mới `evals.json` theo từ vựng hiện tại (mode, role profile), giữ số ca nhỏ (5–8 ca), mỗi ca gắn với một failure mode đã biết.
5. Đổi tên "Behavioral Eval" thành "Structural Eval" nếu vẫn chỉ kiểm file, để không hứa quá mức. Eval gọi LLM thật là việc riêng, **ngoài phạm vi** spec này.

**Tác động kỳ vọng.** Lần đầu có thước đo cho câu hỏi quan trọng nhất: "kit sinh ra có đúng không". Đây cũng là lưới an toàn bắt buộc cho nâng cấp 4.

**Trade-off.**

- Fixture phải được cập nhật mỗi khi đổi template; đó là cái giá của việc có test thật. Giữ fixture nhỏ để chi phí này thấp.
- Không giải quyết chất lượng **nội dung** do LLM sinh (đó vẫn cần đánh giá của người). Spec này chỉ đảm bảo phần tất định đúng.

**Tiêu chí thành công.**

- [ ] Test E2E trên fixture pass, và sinh ra 5 contract JSON, mỗi file có ≥ 1 mục.
- [ ] Xóa tay `capabilities` khỏi agent của fixture thì validator fail với `routing.empty_capabilities`.
- [ ] `evals.json` không còn từ khóa Tier/Lens của bản cũ; mỗi ca ghi failure mode mà nó bảo vệ.
- [ ] Mỗi lần thêm một `compile_*.py` mới đều yêu cầu có ca trên fixture (ghi vào quy ước kiểm ở `validate_kit`).

---

### Nâng cấp 4 — Context Diet: ngân sách cho nội dung always-on

**Bằng chứng:** A8, A12 (phần context), A13.

**Vấn đề.** Mỗi lượt, agent nạp ~28.5 KB (3 rule always-on + orchestrator), trong khi chính CHANGELOG từng đặt mục tiêu rule dưới 3 KB. `collaboration-protocol` (8.1 KB) và `core-guardrails` (3.9 KB) lặp nhau ở Grounding, Worker Briefing, Central Feedback. Benchmark JIT tự hào "giảm 82–88% token" nhưng đo phần tham chiếu nạp theo yêu cầu, **không đo phần nền always-on**, nên bỏ sót chi phí lớn nhất. `ui-ux-pro-max` và `skill-creator` chiếm phần lớn dung lượng dù chỉ liên quan tới nhánh visual và nhánh sửa skill.

**Giải pháp đề xuất.**

1. Đặt **ngân sách byte** cho nội dung `always_on`, ví dụ ≤ 8 KB tổng (rule) và ≤ 8 KB cho orchestrator. Con số cụ thể bạn chỉnh được; điều quan trọng là có ngân sách và có test.
2. Hợp nhất `collaboration-protocol` vào `core-guardrails`, mỗi quy tắc chỉ xuất hiện đúng một nơi. Phần mô tả dài (HUD, role profile chi tiết) chuyển sang `references/` và chỉ nạp khi vào đúng mode.
3. Thêm test "context budget": tính tổng byte file `always_on` + orchestrator, fail nếu vượt ngân sách. Đo token thật bằng tokenizer của nền tảng đích nếu có; nếu không thì dùng byte làm đại diện và ghi rõ.
4. Đưa `ui-ux-pro-max` thành module tùy chọn (chỉ nạp ở `VISUAL_TRACK`), và cập nhật benchmark để báo cả chi phí nền.
5. **Làm sau nâng cấp 1 và 3**, và so sánh trước/sau bằng fixture để chắc không mất hành vi.

**Tác động kỳ vọng.** Giảm đáng kể token nền mỗi lượt (mục tiêu theo ngân sách ở trên: giảm ~45–55% byte always-on, **đây là mục tiêu, chưa phải kết quả đo**). Giảm xung đột giữa các quy tắc lặp.

**Trade-off.**

- **Rủi ro lớn nhất của spec:** cắt quy tắc có thể làm LLM bỏ qua một bất biến mà trước đây nó tuân thủ nhờ lặp lại. Đó là lý do bắt buộc phải có nâng cấp 1 và 3 làm lưới an toàn, và triển khai theo từng bước nhỏ, mỗi bước chạy lại fixture.
- Chuyển nội dung sang `references/` làm tăng độ phụ thuộc vào việc nạp đúng lúc (JIT). Cần giữ một dòng trỏ rõ trong rule.

**Tiêu chí thành công.**

- [ ] Test ngân sách pass: tổng byte always-on + orchestrator ≤ ngân sách đã chốt.
- [ ] Mỗi bất biến P0 xuất hiện đúng 1 lần ở nội dung always-on (kiểm bằng script đếm ID bất biến).
- [ ] Chạy lại fixture E2E và bộ eval: kết quả không đổi so với trước khi cắt.
- [ ] Benchmark báo thêm dòng "chi phí nền always-on" cạnh JIT.

---

### Nâng cấp 5 — Single Source of Truth cho số đếm, version, mode và từ vựng

**Bằng chứng:** A1 (2 lỗi lệch số đếm), A11.

**Vấn đề.** Cùng một thông tin được viết tay ở nhiều nơi nên lệch nhau: version có 3 giá trị, số skill 10 vs 11, số mode 5 vs 10, và ba hệ từ vựng phân cấp độ phức tạp. Các lệch này không gây lỗi runtime ngay, nhưng làm LLM nhận chỉ dẫn mâu thuẫn và làm người đọc mất tin tưởng.

**Giải pháp đề xuất.**

1. Chọn `manifest.json` (đã có) làm nguồn duy nhất cho: version, số lượng cấu phần, danh sách skill/workflow/rule.
2. Sinh các khối số liệu trong README và ARCHITECTURE từ manifest (giữa cặp marker `<!-- GENERATED:start/end -->`), không sửa tay. `validate_kit.py` đã có luật `architecture.count_mismatch`, chỉ cần chuyển từ "báo lỗi" sang "sinh".
3. Lập **bảng mode chuẩn duy nhất** (10 mode) ở `dynamic-routing`, orchestrator chỉ trỏ tới đó thay vì tự liệt kê.
4. Chốt một hệ từ vựng cấp độ (đề xuất giữ `Micro / Standard / Mini-Suite / Full Suite` vì `domain-profiling` dùng và có điều kiện rõ ràng), thêm bảng ánh xạ ngắn từ Tier 1–3 và `SUITE_BUILD` sang hệ này, rồi dọn dần các chỗ còn dùng từ cũ.
5. Cập nhật tiêu đề `failure-modes.md` và `evals.json` về đúng phiên bản.

**Tác động kỳ vọng.** Hết lệch số liệu; giảm chỉ dẫn mâu thuẫn trong prompt; mỗi lần thêm skill/workflow chỉ cần sửa một chỗ.

**Trade-off.**

- Sinh tài liệu từ manifest thêm một bước build; phải nằm trong `verify_all.py` để không bị quên.
- Đổi từ vựng có thể chạm file của kit đầu ra cũ; chỉ áp dụng cho repo này, kit cũ giữ nguyên và dùng bảng ánh xạ.

**Tiêu chí thành công.**

- [ ] Chạy script sinh tài liệu hai lần liên tiếp: lần hai không đổi file nào (idempotent).
- [ ] `grep` version trong README/ARCHITECTURE/VERSION cho đúng 1 giá trị.
- [ ] Orchestrator và `dynamic-routing` cùng liệt kê đúng 10 mode (hoặc orchestrator chỉ trỏ sang).
- [ ] Không còn dòng nào dùng "Tier 1/2/3" hoặc `SUITE_BUILD` ngoài bảng ánh xạ.

---

## 5. Những thứ cố ý KHÔNG đưa vào (tránh over-engineering)

| Ý tưởng                                                           | Lý do loại                                                                                |
| :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| Viết lại kiến trúc orchestrator hoặc thêm agent mới           | Audit không cho thấy topology là nút thắt                                              |
| Eval gọi LLM thật, chấm điểm tự động chất lượng nội dung | Tốn token, khó tái lập; làm sau khi nâng cấp 1–3 ổn định                         |
| Thêm nền tảng export mới (Gemini, Copilot…)                     | Chưa có bằng chứng nhu cầu; `export_kit.py` hiện chưa có test E2E trên fixture   |
| Xóa hẳn nhóm evolution                                            | Chưa đủ dữ kiện để quyết; nâng cấp 1 chỉ yêu cầu quyết định có chủ đích |
| Mở rộng `memory/`                                                | `user-preferences.md` còn rỗng; chưa có dấu hiệu bộ nhớ là nút thắt            |

---

## 6. Rủi ro và phụ thuộc

| Rủi ro                                               |     Mức     | Giảm thiểu                                                      |
| :---------------------------------------------------- | :-----------: | :---------------------------------------------------------------- |
| Sửa test lộ thêm lỗi thật                        |  Trung bình  | Chấp nhận; xử lý theo từng lỗi, không dồn một commit     |
| Cắt always-on làm LLM bỏ bất biến (nâng cấp 4) | **Cao** | Làm sau 1 và 3; từng bước nhỏ; so sánh fixture trước/sau |
| Fixture nhanh cũ so với template                    |     Thấp     | Giữ nhỏ; test fail khi lệch, buộc cập nhật                  |
| Hành vi LLM thay đổi theo model/nền tảng         |  Trung bình  | Ngoài phạm vi spec; ghi nhận ở Giới hạn                     |

**Phụ thuộc:** 1 → (2, 3) → 4 → 5. Nâng cấp 2 độc lập, có thể làm song song với 1.

---

## 7. Giới hạn của audit

- Chỉ đọc đầy đủ: `domain-profiling`, `kit-architect`, 3 rule, `create-kit`, `failure-modes`, `outcome-lenses`, `eval_runner`, phần đầu `benchmark_behavior`, các JSON contract, `memory/`. **Chưa đọc kỹ:** `prompt-compiling`, `kit-assembling`, `kit-verifying`, `kit-evolving`, 6 workflow còn lại, phần lớn `scripts/` ngoài các file đã nêu.
- Chưa chạy một lượt `/create-kit` thật bằng LLM nên chưa quan sát được hành vi tuân thủ bất biến trong thực tế.
- "Nghiên cứu bổ sung" ở đây chủ yếu là đối chiếu nội bộ (tài liệu tự mô tả đối chiếu với kết quả chạy). Mình không tra cứu nguồn bên ngoài trong phiên này.
- Số token chỉ là ước lượng từ byte. Điểm ROI là phán đoán định tính, không phải đo đạc.
- Audit dựa trên clone ở commit `5faeb07`; nếu bạn đã đẩy commit mới hơn, vài con số có thể đã khác.

---

## 8. Hiệu chỉnh sau khi đọc code để lập plan (2026-10-14)

Khi lập plan, mình đọc thêm code và phải sửa 8 điểm của spec. Chi tiết nằm ở bảng "Spec corrections" trong plan. Tóm tắt:

- Luật `routing.empty_capabilities` **đã tồn tại** (`validate_kit.py:732`); Creator thoát luật nhờ `routing_exempt: true`.
- Chỉ 4 trong 8 module test lỗi do `feedback_collector`; số còn lại lỗi do thiếu `pytest`/`jsonschema` (repo không có `requirements*`).
- Nguyên nhân test làm bẩn cây git: `validate()` mặc định `auto_heal=True` và `test_sync_registry` chạy trên repo thật.
- Nhóm evolution hỏng nặng hơn nêu ở A13: `evolution_engine.py` crash khi import; `equip_evolution.py` copy 2 file không tồn tại và được `create-kit` Bước 4 gọi (đọc code, chưa chạy trên kit thật).
- 3 script `skill-creator` fail `--help` do validator chạy sai thư mục, không phải do script hỏng.
- Mục tiêu giảm context hạ từ ~45–55% xuống **~35%** (18,432 B so với 28,515 B).
- Bỏ đề xuất đưa `ui-ux-pro-max` thành module tùy chọn (3.8 MB là file dữ liệu không nạp vào context).
- Từ vựng cũ (Tier 1/2/3, `SUITE_BUILD`) xử lý bằng test "ratchet" (allowlist chỉ co lại) thay vì xóa sạch một lần.
