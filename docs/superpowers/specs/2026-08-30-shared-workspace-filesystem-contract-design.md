# Shared Workspace & Universal Artifact Lifecycle Contract

> **Trạng thái:** FROZEN (Brainstorming Finalized)  
> **Ngày:** 2026-08-30  
> **Tác giả:** @kit-architect & Sếp  
> **Mục tiêu:** Nâng cấp Agent Kit Builder sao cho mọi Agent Kit sinh ra đều có filesystem/workspace đơn giản, trực quan, khó dùng sai, tự dọn rác và dễ dàng tái sử dụng chéo (Cross-Kit Discovery) mà không cần cấu hình phức tạp.

---

## 1. Triết Lý Cốt Lõi (The Core Philosophy)

> **"User interacts with Inputs and Outputs. Agents work inside `.workspace`. Only intentional final Outputs become shared resources."**  
> *(Người dùng chỉ tương tác với Inputs và Outputs. Agent tự làm việc trong `.workspace`. Chỉ thành phẩm có chủ đích mới trở thành tài nguyên dùng chung.)*

### 5 Nguyên Tắc 80/20 Bất Biến
1. **Zero Cognitive Load cho Input**: Người dùng có chỗ thả file rõ ràng (`Shared/` cho đồ chung, `Projects/<Name>/inputs/` cho việc riêng); nếu lười phân loại thì có `_Dropzone/` tiếp nhận an toàn.
2. **The "Clean Dish" Principle (Bàn ăn sạch)**: Khách ăn steak không cần xem căn bếp bừa bãi. Mọi file chunk, log, cache, json tạm thời bị nhốt tuyệt đối trong `.workspace/`. Thư mục `outputs/` chỉ chứa sản phẩm hoàn chỉnh, mở ra đọc được ngay.
3. **Artifact-Level Promotion (Scope Promotion)**: Quyền được dùng chung không thuộc về Agent Kit, mà là quyết định thăng hạng phạm vi (`scope: project -> shared`) của từng Artifact cụ thể. Một bản nháp không tự nhiên biến thành tài sản toàn hệ thống.
4. **Convention over Configuration (Quy ước thay vì Cấu hình)**: Không cần cơ sở dữ liệu hay artifact registry cồng kềnh ở V1. Cross-Kit Discovery hoạt động dựa trên quy ước cây thư mục chuẩn và nhận diện semantic artifact type (không phụ thuộc đuôi file).
5. **Progressive Architecture (Tiệm tiến linh hoạt)**: Tuyệt đối không ép mọi Agent Kit phải dựng cấu trúc Project. Simple utility chạy thẳng với input/output trực tiếp; chỉ khi task có nhiều bước, nhiều agent hoặc cần lưu trạng thái mới kích hoạt bộ ba `inputs/` - `outputs/` - `.workspace/`.

---

## 2. Bản Đồ Cây Thư Mục Toàn Cục (Global Hierarchy)

Thư mục gốc chuẩn của toàn bộ hệ sinh thái đặt tại: `Downloads/Shared Workspace/`

```plaintext
Downloads/
└── Shared Workspace/
    │
    ├── 📥 _Dropzone/              <-- Cửa nhận đồ: Ném bất cứ thứ gì vào đây khi chưa biết để đâu
    │
    ├── 🏛️ Shared/                 <-- Thư viện tài nguyên dùng chung (ĐÃ PUBLISH / APPROVED)
    │   ├── Books/                <-- Sách nguồn & sách hoàn thiện dùng chung (epub, pdf, docx)
    │   ├── Videos/               <-- Footage gốc, âm thanh, video thành phẩm (mp4, mov, wav)
    │   └── Files/                <-- Báo cáo, template, dataset, prompt assets chung
    │
    └── 🚀 Projects/               <-- Không gian cho các chiến dịch / công việc có vòng đời
        ├── [Project-A]/
        │   ├── inputs/           <-- Dữ liệu đầu vào RIÊNG cho Project A
        │   ├── outputs/          <-- Thành phẩm sạch của Project A
        │   └── .workspace/       <-- "Căn bếp kín": chunks, intermediate, logs, cache
        │
        └── [Project-B]/
            ├── inputs/
            ├── outputs/
            └── .workspace/
```

---

## 3. Ma Trận Tương Tác Dữ Liệu (Interaction Matrix)

### 3.1. Phân Loại Nguồn Đầu Vào (Inputs)

| Khi Người Dùng Có | Ném Vào Đâu | Ai Được Quyền Dùng? | Hành Vi Của Agent |
| :--- | :--- | :--- | :--- |
| Cuốn sách / tài liệu muốn nhiều Kit dùng lại | `Shared/Books/` | Mọi Agent Kit | Đọc trực tiếp (Read-Only) |
| Video footage, b-roll, nhạc nền dùng chung | `Shared/Videos/` | Mọi Agent Kit | Đọc trực tiếp (Read-Only) |
| File chỉ phục vụ duy nhất 1 dự án cụ thể | `Projects/<Name>/inputs/` | Chỉ Project đó | Đọc và xử lý nội bộ |
| **Không biết nên để ở đâu (Lười nghĩ)** | `_Dropzone/` | Mọi Agent Kit | Quét, nhận diện mục đích, liên kết vào Project hoặc gợi ý chuyển vào `Shared/`. **KHÔNG TỰ XÓA SOURCE**. |

### 3.2. Quy Tắc Ứng Xử Tại `_Dropzone/` (Inbox An Toàn & Tiết Kiệm)
- **Bất biến**: Agent tuyệt đối **không tự ý xóa** file nguồn trong `_Dropzone/`.
- **Zero-Copy Ingestion (Tiết kiệm dung lượng)**:
  - Khi nạp video/sách nặng từ `_Dropzone/`, Agent ưu tiên **tạo reference/symlink** sang `Projects/<Name>/inputs/`.
  - Chỉ tạo bản copy vật lý khi công cụ xử lý bắt buộc một bản copy độc lập để chỉnh sửa trực tiếp.
  - Thông báo nhẹ nhàng: *"Đã liên kết file X vào dự án Y. File gốc tại `_Dropzone/` sếp có thể dọn bất kỳ lúc nào."*

---

## 4. Mô Hình Vòng Đời Artifact (Universal Artifact Model)

Mọi artifact trong hệ thống được xác định chặt chẽ qua bộ 3 thuộc tính:

$$\text{Artifact} = \langle \text{Scope}, \text{Lifecycle}, \text{Type} \rangle$$

```text
artifact
├── scope: project | shared
├── lifecycle: final | intermediate | cache
└── type: book | video | document | asset | data
```

### Bảng Phân Tầng Vòng Đời & Quyền Lưu Trữ

| Phân Loại Artifact | Scope | Lifecycle | Vị trí lưu trữ | Quyền xóa (Retention) | Tầm nhìn (Visibility) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Project Deliverables** | `project` | `final` | `Projects/<Name>/outputs/` | **Bất biến**: Chỉ User được xóa. | User & Project nội bộ |
| **Published Shared Assets** | `shared` | `final` | `Shared/<Type>/` | **Bất biến**: Tài sản dùng chung dài hạn. | Toàn bộ hệ sinh thái |
| **Intermediates** | `project` | `intermediate` | `Projects/<Name>/.workspace/stages/` | **Auto-Purgeable**: Tự xóa khi task thành công hoặc qua lệnh dọn dẹp. | Blind (Ẩn với agent khác) |
| **Cache & Scratch** | `project` | `cache` | `Projects/<Name>/.workspace/cache/` | **Volatile**: Xóa an toàn 100% bất kỳ lúc nào. | Blind |

> **Quy tắc Scope Promotion:** Quá trình "Promote" thực chất là chuyển trạng thái một artifact từ `scope: project` sang `scope: shared`, và di chuyển/link file từ `Projects/<Name>/outputs/` sang `Shared/<Type>/`.

---

## 5. Cơ Chế Xuất Bản & Tái Sử Dụng Chéo (Promotion & Discovery)

### 5.1. Cơ Chế "Promote" Có Chủ Đích (Intentional Promotion)

Một sản phẩm hoàn thành trong `outputs/` của Project không tự động tràn vào `Shared/`.

```
[Project-A/outputs/] ──(Hoàn tất task)──> [Hỏi User 1 câu xác nhận] ──(YES)──> [Shared/<Type>/]
```

* **Ví dụ thực tế**:
  Book Translator hoàn thành:
  - `Projects/Translate-Book/outputs/book_vi.epub` (Sản phẩm chính)
  - `Projects/Translate-Book/outputs/translation_summary.md` (Báo cáo nội bộ)
* **Agent đề xuất tại vạch đích**:
  > *"✨ Đã dịch xong `outputs/book_vi.epub`. Sếp có muốn publish cuốn sách này vào `Shared/Books/` để các kit khác (Marketing, Video) cùng dùng không?"*
* Khi sếp đồng ý: Agent chuyển file sang `Shared/Books/book_vi.epub`. File `translation_summary.md` vẫn nằm lại ở Project vì chỉ phục vụ nội bộ.

### 5.2. Giao Thức Cross-Kit Discovery (Quy Tắc Ưu Tiên & Semantic Matching)

Khi một Kit (ví dụ: Marketing Agent) cần tìm tài nguyên do Kit khác tạo ra:

1. **Thứ tự ưu tiên nguồn (Resolution Hierarchy)**:
   - **Ưu tiên 1: `Shared/<Type>/`**: Nơi chứa các tài sản đã được publish/approved chính thức. Đây là nguồn mặc định.
   - **Ưu tiên 2: `Projects/*/outputs/`**: Chỉ quét vào đây khi:
     - Người dùng chỉ định đích danh một Project cụ thể; HOẶC
     - Trong `Shared/` hoàn toàn chưa có tài nguyên tương ứng.
   - **Cấm kỵ tuyệt đối**: Không bao giờ quét vào bất kỳ thư mục `.workspace/` nào.
2. **Semantic Artifact Matching (Không phụ thuộc đuôi file thô)**:
   - Agent hiểu yêu cầu ở tầng ngữ nghĩa: *"Tìm book artifact phù hợp"* thay vì hard-code quét `.epub`. Đuôi file và đường dẫn chỉ là chi tiết kỹ thuật triển khai.
3. **Quy tắc giải quyết xung đột**:
   - Nếu tìm thấy 1 kết quả rõ ràng: Dùng luôn và thông báo nhẹ.
   - Nếu tìm thấy nhiều bản hoặc mơ hồ: Hỏi đúng **1 câu lựa chọn**. Tuyệt đối không đoán bừa.

---

## 6. Nâng Cấp Agent Kit Builder (Builder Implementation Specs)

### 6.1. Cập Nhật `agent-template.md` (Filesystem Negative Constraints)
Bổ sung khối lệnh P0 vào System Prompt mẫu:

```markdown
### 🔒 FILESYSTEM & WORKSPACE CONTRACT (BẤT BIẾN)
1. **Inputs Authority (`inputs/` | `Shared/`)**: Chỉ đọc dữ liệu từ đây. Tuyệt đối KHÔNG ghi file tạm hoặc nháp vào thư mục này.
2. **Closed Kitchen (`.workspace/`)**: Mọi dữ liệu trung gian (chunks, split audio, temp json, embeddings, logs) BẮT BUỘC ghi vào `.workspace/`. Cấm xả rác ra root.
3. **Clean Deliverables (`outputs/`)**: Chỉ ghi vào `outputs/` khi file đã hoàn chỉnh 100%, sẵn sàng cho người dùng sử dụng.
4. **Controlled Promotion**: Không tự ý đẩy file lên `Shared/`. Chỉ promote khi người dùng xác nhận hoặc workflow có chỉ thị rõ ràng.
5. **Zero-Pollution Discovery**: Khi tìm kiếm tài nguyên từ kit khác, ưu tiên quét `Shared/`, sau đó mới đến `outputs/`. Không bao giờ scan `.workspace/`.
```

### 6.2. Cập Nhật `manifest-template.json` (Artifact Contracts)
Khai báo semantic artifact contract trong manifest:

```json
{
  "artifact_contracts": {
    "consumes": [
      { "type": "book", "preferred_sources": ["Shared/Books", "inputs"] }
    ],
    "produces": [
      { "type": "book", "default_scope": "project", "path_pattern": "outputs/{slug}-vi.epub", "promotable_to": "Shared/Books" }
    ],
    "workspace_dir": ".workspace"
  }
}
```

### 6.3. Universal Path Resolution & Progressive Layout
Tôn trọng nguyên tắc tiệm tiến: Không bắt buộc mọi utility nhỏ phải tạo thư mục Project.

```python
# Pseudo-code minh họa quy ước đường dẫn
if is_running_in_project():
    INPUT_DIR = Path("./inputs")
    OUTPUT_DIR = Path("./outputs")
    WORKSPACE_DIR = Path("./.workspace")
else:
    # Standalone mode: Tiện ích đơn lẻ (Zero setup)
    # Nhận input trực tiếp -> xuất output trực tiếp -> dọn sạch tạm
    INPUT_DIR = Path(args.input).parent
    OUTPUT_DIR = INPUT_DIR
    WORKSPACE_DIR = Path("./.workspace")  # Tự dọn sạch sau khi hoàn tất
```

### 6.4. Chuẩn Hóa Giao Diện README (Card 4 Dòng)
Mọi kit khi sinh ra đều có bảng chỉ dẫn 4 dòng ở đầu README:

```markdown
> 📥 **Input:** Thả tài liệu vào `inputs/` (hoặc `Shared/`, `_Dropzone/`)  
> ✨ **Output:** Thành phẩm sạch của dự án nằm tại `outputs/`  
> 📤 **Share:** Chỉ publish lên `Shared/` khi muốn các Agent khác cùng tái sử dụng  
> ⚙️ **Working Files:** Nằm ẩn trong `.workspace/` (Thoải mái xóa để giải phóng ổ cứng)
```

---

## 7. Kế Hoạch Xác Minh (Verification & Validation)

1. **L1 Deterministic Linting (`validate_kit.py`)**:
   - Kiểm tra xem System Prompt có đủ 5 điều khoản Filesystem Contract.
   - Kiểm tra `manifest.json` có khai báo `artifact_contracts` với `consumes`, `produces`, và `workspace_dir`.
2. **Adversarial Output Test**:
   - Chạy thử nghiệm thực tế với Kit Dịch sách hoặc Biên tập Video:
   - Thư mục `outputs/` chỉ được chứa đúng deliverables sạch.
   - 100% intermediate files, logs, chunks phải nằm trong `.workspace/`.
   - Kiểm tra luồng promote lên `Shared/Books/` chỉ kích hoạt sau khi có xác nhận.
