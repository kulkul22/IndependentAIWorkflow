---
name: git_workflow_standards
description: Quy chuẩn quản trị Git chuyên nghiệp (Branching Strategy, Feature/Bugfix Workflow, Semantic Versioning, Conventional Commits) bắt buộc tuân thủ cho mọi dự án.
---

# 🌿 Tiêu Chuẩn Quản Trị Git Workflow & Phát Triển Phần Mềm

Tài liệu này định nghĩa **quy chuẩn quản trị Git chuyên nghiệp** bắt buộc Kul (AI Agent) phải tự động tuân thủ 100% trong tất cả các thao tác phát triển tính năng, sửa lỗi, và đóng gói phiên bản mã nguồn.

> [!IMPORTANT]
> **QUY TẮC VÀNG:**
> 1. **TUYỆT ĐỐI KHÔNG Direct Push vào nhánh `master`** khi phát triển tính năng hoặc sửa bug.
> 2. Nhánh `master` chỉ chứa các bản Release sản phẩm ổn định 100% và luôn được gắn **Git Tag phiên bản (SemVer: `vX.Y.Z`)**.
> 3. Tất cả công việc phát triển hàng ngày phải thực hiện trên nhánh `develop` hoặc các nhánh ngắn hạn (`feature/*`, `bugfix/*`, `hotfix/*`).

---

## 🏛️ Cấu Trúc Nhánh (Branching Strategy)

```mermaid
gitGraph
   commit id: "v1.0.0 (Release Initial)"
   branch develop
   checkout develop
   commit id: "docs: update readme"
   branch feature/gpm-login-control
   checkout feature/gpm-login-control
   commit id: "feat: add gpm login local API client"
   checkout develop
   merge feature/gpm-login-control
   branch bugfix/leave-request-parser
   checkout bugfix/leave-request-parser
   commit id: "fix: add parse_leave_request_subject helper"
   checkout develop
   merge bugfix/leave-request-parser
   checkout master
   merge develop tag: "v1.0.1"
```

| Tên Nhánh | Nhánh Gốc | Mục Đích Sử Dụng | Quy Tắc Merge & Release |
| :--- | :--- | :--- | :--- |
| **`master`** | - | Nhánh Production chứa mã nguồn ổn định nhất. | Không commit trực tiếp. Chỉ nhận merge từ `develop` hoặc `hotfix/*`. Luôn đánh Tag `vX.Y.Z`. |
| **`develop`** | `master` | Nhánh tích hợp mã nguồn chính cho công việc hàng ngày. | Nhận merge từ `feature/*` và `bugfix/*`. |
| **`feature/<tên-tính-năng>`** | `develop` | Phát triển tính năng mới (VD: `feature/gpm-login-control`). | Phát triển xong ➔ Test ➔ Merge về `develop` ➔ Xóa nhánh feature. |
| **`bugfix/<tên-lỗi>`** | `develop` | Sửa lỗi thông thường trong quá trình phát triển (VD: `bugfix/leave-parser`). | Fix xong ➔ Test ➔ Merge về `develop` ➔ Xóa nhánh bugfix. |
| **`hotfix/<tên-hotfix>`** | `master` | Sửa lỗi khẩn cấp trực tiếp trên Production (VD: `hotfix/nul-sandbox`). | Fix xong ➔ Merge vào CẢ `master` (đánh Tag `vX.Y.Z+1`) và `develop`. |

---

## ⚙️ Quy Trình Thực Hiện Tự Động Cho Agent

### 1. Khi Sếp yêu cầu Thêm Tính Năng Mới (`New Feature`)
1. **Kiểm tra & Checkout:** `git checkout develop` ➔ `git pull origin develop`.
2. **Tạo nhánh feature:** `git checkout -b feature/<tên-tính-năng>` (VD: `git checkout -b feature/wake-on-lan`).
3. **Thực thi code & Test:** Thực hiện code, tự động rà soát tất cả các file liên quan (`/start`, `/help`, `set_my_commands`, `ReplyKeyboardMarkup`, script phụ, docs).
4. **Commit chuẩn mực:** Commit theo định dạng Conventional Commits (`feat: ...`, `docs: ...`).
5. **Merge về `develop`:** 
   ```powershell
   git checkout develop
   git merge feature/<tên-tính-năng>
   git push origin develop
   git branch -d feature/<tên-tính-năng>
   ```

### 2. Khi Sếp yêu cầu Sửa Lỗi (`Bug Fix`)
1. **Tạo nhánh bugfix:** Từ `develop`, tạo `git checkout -b bugfix/<tên-lỗi>`.
2. **Khắc phục & Kiểm thử thực tế:** Sửa lỗi, chạy test thực tế trên hệ thống để xác nhận.
3. **Commit & Merge:** Commit `fix: ...`, merge về `develop` và push lên `origin develop`.

### 3. Đóng Gói Release & Đánh Tag Phiên Bản (`Release Management`)
Khi chốt bản Release ổn định hoặc Sếp yêu cầu release:
1. **Merge `develop` ➔ `master`:**
   ```powershell
   git checkout master
   git merge develop
   ```
2. **Đánh Tag phiên bản (Semantic Versioning):**
   - Lỗi nhỏ/Patch: `git tag -a v1.0.2 -m "v1.0.2 - Description"`
   - Tính năng mới/Minor: `git tag -a v1.1.0 -m "v1.1.0 - Description"`
3. **Cập nhật CHANGELOG.md:** Đảm bảo file [CHANGELOG.md](file:///d:/TestProject/TomAssistantKulBot/CHANGELOG.md) ghi đầy đủ các mục `Added`, `Changed`, `Fixed`.
4. **Push Master & Tags:**
   ```powershell
   git push origin master
   git push origin --tags
   git checkout develop
   ```

---

## 📝 Chuẩn Định Dạng Commit (Conventional Commits)

Mọi commit tin nhắn bắt buộc dùng một trong các tiền tố sau:

- `feat:` Thêm tính năng mới cho người dùng.
- `fix:` Sửa lỗi/bug trong hệ thống.
- `docs:` Cập nhật tài liệu (README, SKILL, MEMORY, docstrings).
- `style:` Định dạng code, dấu phẩy, khoảng trắng (không ảnh hưởng logic).
- `refactor:` Tái cấu trúc mã nguồn (không thêm tính năng, không sửa bug).
- `test:` Bổ sung hoặc sửa đổi các kịch bản kiểm thử (testcases).
- `chore:` Cập nhật cấu hình build, package.json, gitignore, v.v.

---

## 📋 Danh Sách Rà Soát File Liên Quan (Mandatory Checklist)

Khi phát triển bất kỳ tính năng hoặc sửa lỗi nào, Kul BẮT BUỘC phải kiểm tra và cập nhật đồng bộ các file sau:

- [ ] File xử lý chính (`telegram_agent.py`, `outlook_local_checker.py`, v.v.)
- [ ] Entry point hiển thị `/start` & `/help` (`send_welcome`)
- [ ] Menu gợi ý tự động (`bot.set_my_commands`)
- [ ] Bàn phím nút bấm phím tắt (`ReplyKeyboardMarkup`)
- [ ] Tài liệu kỹ thuật Skill ([SKILL.md](file:///d:/TestProject/TomAssistantKulBot/.agents/skills/telegram_bot_assistant/SKILL.md))
- [ ] Tài liệu hướng dẫn ([README.md](file:///d:/TestProject/TomAssistantKulBot/README.md))
- [ ] Nhật ký phiên bản ([CHANGELOG.md](file:///d:/TestProject/TomAssistantKulBot/CHANGELOG.md))
- [ ] Nhật ký làm việc ngày ([memory/YYYY-MM-DD.md](file:///d:/TestProject/TomAssistantKulBot/memory/)) và [MEMORY.md](file:///d:/TestProject/TomAssistantKulBot/MEMORY.md)
