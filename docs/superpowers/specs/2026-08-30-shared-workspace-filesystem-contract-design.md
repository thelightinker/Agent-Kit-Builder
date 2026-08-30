# Shared Workspace & Universal Artifact Lifecycle Contract

> **Trạng thái:** DRAFT (Brainstorming Complete)  
> **Ngày:** 2026-08-30  
> **Tác giả:** @kit-architect & Sếp  
> **Mục tiêu:** Nâng cấp Agent Kit Builder sao cho mọi Agent Kit sinh ra đều có filesystem/workspace đơn giản, trực quan, khó dùng sai, tự dọn rác và dễ dàng tái sử dụng chéo (Cross-Kit Discovery) mà không cần cấu hình phức tạp.

---

## 1. Triết Lý Cốt Lõi (The Core Philosophy)

> **"User interacts with Inputs and Outputs. Agents work inside `.workspace`. Only intentional final Outputs become shared resources."**
> *(Người dùng chỉ tương tác với Inputs và Outputs. Agent tự làm việc trong `.workspace`. Chỉ thành phẩm có chủ đích mới trở thành tài nguyên dùng chung.)*

### 5 Nguyên Tắc 80/20 Bất Biến
1. **Zero Cognitive Load cho Input**: Người dùng có chỗ thả file rõ ràng; nếu lười phân loại thì có `_Dropzone/` tiếp nhận.
2. **The "Clean Dish" Principle (Bàn ăn sạch)**: Khách ăn steak không cần xem căn bếp bừa bãi. Mọi file chunk, log, cache, json tạm thời bị nhốt tuyệt đối trong `.workspace/`. Thư mục `outputs/` chỉ chứa sản phẩm hoàn chỉnh, mở ra đọc được ngay.
3. **Artifact-Level Promotion (Chia sẻ theo Artifact, không theo Kit)**: Quyền được dùng chung không thuộc về Agent Kit, mà thuộc về từng Artifact cụ thể. Một bản nháp không tự nhiên biến thành tài sản toàn hệ thống.
4. **Convention over Configuration (Quy ước thay vì Cấu hình)**: Không cần cơ sở dữ liệu hay artifact registry cồng kềnh ở V1. Cross-Kit Discovery hoạt động thuần túy dựa trên quy ước cây thư mục chuẩn.
5. **Progressive Architecture**: Không ép mọi tác vụ phải tạo Project. Tác vụ ăn liền (Standalone) chạy thẳng với zero-setup; tác vụ dài hơi nhiều bước mới kích hoạt cấu trúc Project.

---

## 2. Bản Đồ Cây Thư Mục Toàn Cục (Global Hierarchy)

Thư mục gốc chuẩn của toàn bộ hệ thống đặt tại: `Downloads/Shared Workspace/`

```plaintext
Downloads/
└── Shared Workspace/
    │
    ├── 📥 _Dropzone/              <-- Cửa nhận đồ: Ném bất cứ thứ gì vào đây khi chưa biết để đâu
    │
    ├── 🏛️ Shared/                 <-- Thư viện tài nguyên dùng chung toàn hệ sinh thái
    │   ├── Books/                <-- Sách nguồn và sách đã dịch hoàn thiện (epub, pdf, docx)
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
| **Không biết nên để ở đâu (Lười nghĩ)** | `_Dropzone/` | Mọi Agent Kit | Quét, nhận diện mục đích, ingest vào Project hoặc gợi ý chuyển vào `Shared/`. **KHÔNG TỰ XÓA SOURCE**. |

### 3.2. Quy Tắc Ứng Xử Tại `_Dropzone/` (Inbox An Toàn)
- **Bất biến**: Agent tuyệt đối **không tự ý xóa** file trong `_Dropzone/`.
- **Luồng xử lý (Ingest & Reference)**:
  1. Khi kích hoạt tác vụ mà không chỉ định file, Agent kiểm tra `_Dropzone/` đầu tiên.
  2. Copy hoặc link file sang `Projects/<Name>/inputs/`.
  3. Thông báo nhẹ nhàng: *"Đã nạp file X vào dự án Y. File gốc tại `_Dropzone/` sếp có thể dọn bất kỳ lúc nào."*

---

## 4. Mô Hình Vòng Đời Artifact (Universal Artifact Model)

Thay vì hard-code loại Kit, mọi artifact sinh ra đều được xác định qua bộ 3 thuộc tính:

$$\text{Artifact} = \langle \text{Scope}, \text{Lifecycle}, \text{Type} \rangle$$

```text
artifact
├── scope: project | shared
├── lifecycle: final | intermediate | cache
└── type: book | video | document | asset | data
```

### Bảng Phân Tầng Sinh Tử & Quyền Lưu Trữ (Retention Policy)

| Tầng Artifact | Lifecycle | Vị trí lưu trữ | Quyền xóa (Retention) | Tầm nhìn (Visibility) |
| :--- | :--- | :--- | :--- | :--- |
| **Deliverables** | `final` | `Projects/<Name>/outputs/` | **Bất biến**: Chỉ User được xóa. | User & Project |
| **Promoted Assets** | `final` + `shared` | `Shared/<Type>/` | **Bất biến**: Lưu trữ dùng chung lâu dài. | Toàn hệ thống |
| **Intermediates** | `intermediate` | `Projects/<Name>/.workspace/stages/` | **Auto-Purgeable**: Tự xóa khi task thành công hoặc qua lệnh dọn dẹp. | Blind (Ẩn với agent khác) |
| **Cache & Scratch** | `cache` | `Projects/<Name>/.workspace/cache/` | **Volatile**: Xóa an toàn 100% bất kỳ lúc nào. | Blind |

---

## 5. Cơ Chế Xuất Bản & Tái Sử Dụng Chéo (Promotion & Discovery)

### 5.1. Cơ Chế "Promote" Lên Thư Viện Dùng Chung (Promotion Flow)

Một sản phẩm hoàn thành trong `outputs/` của Project không tự động tràn vào `Shared/`.

```
[Project-A/outputs/] ──(Hoàn tất task)──> [Hỏi User 1 câu xác nhận] ──(YES)──> [Shared/<Type>/]
```

* **Ví dụ thực tế**:
  Book Translator hoàn thành:
  - `Projects/Translate-Book/outputs/book_vi.epub` (Sản phẩm chính)
  - `Projects/Translate-Book/outputs/translation_summary.md` (Báo cáo nội bộ)
* **Agent đề xuất**:
  > *"✨ Đã dịch xong `outputs/book_vi.epub`. Sếp có muốn publish cuốn sách này vào `Shared/Books/` để các kit khác (Marketing, Video) cùng dùng không?"*
* Khi sếp đồng ý: Agent copy/symlink `book_vi.epub` vào `Shared/Books/book_vi.epub`. File `translation_summary.md` vẫn nằm lại ở Project vì không mang giá trị tái sử dụng toàn cục.

### 5.2. Giao Thức Tìm Kiếm Không Cần Database (Cross-Kit Discovery)

Khi **Marketing Agent** hoặc **Video Editing Kit** nhận lệnh: *"Làm video ngắn cho cuốn sách vừa dịch"*:
1. **Thứ tự quét**:
   - Quét `Shared/Books/` trước tiên (Tài nguyên đã được duyệt dùng chung).
   - Nếu không thấy, quét `Projects/*/outputs/` tìm file định dạng `.epub`, `.pdf`.
   - Tuyệt đối **không bao giờ quét vào `.workspace/`** của bất kỳ thư mục nào.
2. **Quy tắc giải quyết**:
   - Nếu tìm thấy 1 file khớp: Tự động dùng và thông báo: *"Em lấy bản dịch từ `Shared/Books/book_vi.epub`"*.
   - Nếu tìm thấy nhiều bản hoặc mơ hồ: Hỏi đúng **1 câu chọn lựa**. Không tự tiện đoán.

---

## 6. Nâng Cấp Agent Kit Builder (Builder Implementation Specs)

Để đảm bảo mọi Agent Kit mới sinh ra đều tuân thủ hợp đồng này mà không cần lập trình viên phải nhớ quy tắc:

### 6.1. Cập Nhật `agent-template.md` (Filesystem Negative Constraints)
Bổ sung khối lệnh P0 vào System Prompt mẫu:

```markdown
### 🔒 FILESYSTEM & WORKSPACE CONTRACT (BẤT BIẾN)
1. **Inputs Authority (`inputs/` | `Shared/`)**: Chỉ đọc dữ liệu từ đây. Tuyệt đối KHÔNG ghi file tạm hoặc nháp vào thư mục này.
2. **Closed Kitchen (`.workspace/`)**: Mọi dữ liệu trung gian (chunks, split audio, temp json, embeddings, logs) BẮT BUỘC ghi vào `.workspace/`. Cấm xả rác ra root.
3. **Clean Deliverables (`outputs/`)**: Chỉ ghi vào `outputs/` khi file đã hoàn chỉnh 100%, sẵn sàng cho người dùng sử dụng.
4. **Zero-Pollution Discovery**: Khi tìm kiếm tài nguyên từ kit khác, chỉ quét `Shared/` hoặc `outputs/`. Không scan `.workspace/`.
```

### 6.2. Cập Nhật `manifest-template.json` (Artifact Contracts)
Bổ sung schema hợp đồng I/O vào manifest:

```json
{
  "artifact_contracts": {
    "consumes": [
      { "type": "book", "extensions": [".epub", ".pdf", ".docx"], "preferred_sources": ["Shared/Books", "inputs"] }
    ],
    "produces": [
      { "type": "book", "scope": "project", "path_pattern": "outputs/{slug}-vi.epub", "promotable_to": "Shared/Books" }
    ],
    "workspace_dir": ".workspace"
  }
}
```

### 6.3. Universal Path Resolution (Hỗ trợ cả Standalone & Project)
Mọi script hoặc checklist sinh ra trong kit đều hỗ trợ logic giải quyết đường dẫn:

```python
# Pseudo-code minh họa quy ước đường dẫn
if is_running_in_project():
    INPUT_DIR = Path("./inputs")
    OUTPUT_DIR = Path("./outputs")
    WORKSPACE_DIR = Path("./.workspace")
else:
    # Standalone mode (Zero setup)
    INPUT_DIR = Path(args.input).parent
    OUTPUT_DIR = INPUT_DIR  # Xuất ngay cạnh file nguồn kèm hậu tố
    WORKSPACE_DIR = Path("./.workspace")  # Tự dọn khi xong
```

### 6.4. Chuẩn Hóa README Giao Diện Người Dùng
Mọi kit khi sinh ra đều có bảng chỉ dẫn 3 dòng ở đầu README:

```markdown
> 📥 **Input:** Thả tài liệu vào `inputs/` (hoặc `Shared Workspace/_Dropzone/`)  
> ✨ **Output:** Thành phẩm sạch sẽ xuất hiện tại `outputs/`  
> ⚙️ **Working Files:** Nằm trong `.workspace/` (Thoải mái xóa để giải phóng ổ cứng)
```

---

## 7. Kế Hoạch Xác Minh (Verification & Validation)

1. **L1 Linter Anchor (`validate_kit.py`)**:
   - Thêm hàm kiểm tra `validate_workspace_contract()`: Xác nhận agent prompt có đủ 4 điều khoản Filesystem Contract; `manifest.json` có khai báo `artifact_contracts`.
2. **Adversarial Output Test**:
   - Chạy thử một Kit dịch sách hoặc biên tập video: Đảm bảo sau khi chạy xong, thư mục `outputs/` chỉ có đúng file thành phẩm, không có bất kỳ thư mục con `extracted/` hay file `.json` trung gian nào lọt ra ngoài. Toàn bộ nằm gọn trong `.workspace/`.
