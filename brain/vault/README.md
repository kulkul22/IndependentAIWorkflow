# 🧠 Javis OS - Second Brain Vault

Chào mừng đến với **Second Brain** của hệ thống Javis OS. 
Đây là nơi lưu trữ toàn bộ tri thức, ngữ cảnh (context) và ý tưởng của sếp dưới dạng các file Markdown thuần tuý.

## 📂 Cấu trúc Thư mục

- `projects/`: Nơi lưu trữ thông tin về các dự án đang làm, quyết định kỹ thuật, cấu trúc thư mục, context tổng quan.
- `content-ideas/`: Nơi lưu các ý tưởng viết bài blog, làm video, hoặc các đoạn text nháp.
- `journal/`: Nơi lưu các file daily notes theo định dạng `YYYY-MM-DD.md`. Ghi chép tiến độ hàng ngày.

## ✍️ Quy tắc Viết (Obsidian-Style)

Hệ thống RAG (Retrieval-Augmented Generation) được thiết kế để hiểu các liên kết ngữ nghĩa trong ghi chú của bạn:

1. **Liên kết (Links):** Sử dụng cú pháp `[[Tên-File]]` để liên kết các ghi chú lại với nhau. AI sẽ dựa vào các liên kết này để hiểu mối quan hệ giữa các concepts.
2. **Tags:** Sử dụng hashtag `#tag_name` ở đầu hoặc cuối file để phân loại (ví dụ: `#idea`, `#python`, `#marketing`).
3. **Frontmatter:** Nếu cần, có thể dùng YAML frontmatter ở đầu file để đánh dấu trạng thái (ví dụ: `status: draft`).

## 🤖 Cách AI (Orchestrator) sử dụng Vault này

- **Khi sếp giao task mới:** AI sẽ tự động kích hoạt `Phase 0: Brain Sync`, đọc lướt qua Vault này (thông qua ChromaDB Vector Search) để lấy lại trí nhớ về dự án, giúp AI không bao giờ quên những quy ước code sếp đã đặt ra.
- **Khi làm xong task:** AI sẽ tự động lưu lại những gì nó vừa làm vào thư mục `projects/` để phục vụ cho các task sau này.
- **Daemon chạy ngầm:** `javis_daemon.py` sẽ liên tục theo dõi thư mục này. Bất cứ khi nào sếp thay đổi file, nó sẽ tự cập nhật vào Vector Database.

> *Lưu ý: Không lưu các thông tin nhạy cảm (như mật khẩu trần, API Keys) trực tiếp vào đây nếu thư mục này được commit lên public repo.*
