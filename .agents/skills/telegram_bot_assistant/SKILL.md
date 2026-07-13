---
name: telegram_bot_assistant
description: Trợ lý quản lý, vận hành và phát triển hệ thống Telegram Bot Kul kết nối cầu nối điều khiển IDE Agent từ xa.
---

# Trợ Lý Vận Hành & Phát Triển Telegram Bot Kul

Tài liệu này tổng hợp toàn bộ cấu trúc, cơ chế hoạt động, các câu lệnh và quy trình xử lý sự cố của hệ thống trợ lý chạy ngầm **Telegram Bot Kul** kết hợp cầu nối tương tác từ xa với **IDE Agent**.

> [!NOTE]
> Hệ thống này được thiết kế để hoạt động độc lập trên máy của sếp, duy trì kết nối giữa thiết bị di động (qua Telegram) và môi trường phát triển IDE để sếp có thể giám sát hoặc ra lệnh lập trình từ xa.

---

## 📁 Cấu Trúc Hệ Thống (`TomAssistantKulBot`)

Toàn bộ mã nguồn và cấu hình của bot daemon được đặt tại: [TomAssistantKulBot](file:///d:/TestProject/TomAssistantKulBot).

### 1. Mã Nguồn Chính (`src/`)
* **[telegram_agent.py](file:///d:/TestProject/TomAssistantKulBot/src/telegram_agent.py)**: Mã nguồn Python chính của bot, sử dụng thư viện `pyTelegramBotAPI` để lắng nghe tin nhắn và `google-generativeai` để chat tự nhiên bằng mô hình `gemini-2.5-flash`.
* **[outlook_local_checker.py](file:///d:/TestProject/TomAssistantKulBot/src/outlook_local_checker.py)**: Script độc lập kết nối Outlook Desktop cục bộ để quét các email xin nghỉ phép từ 7 ngày gần nhất.
* **[outlook_calendar_checker.py](file:///d:/TestProject/TomAssistantKulBot/src/outlook_calendar_checker.py)**: Script độc lập truy vấn Outlook Desktop Calendar (MAPI) lấy danh sách các lịch họp/sự kiện trong ngày hôm nay.
* **[teams_browser_scraper.py](file:///d:/TestProject/TomAssistantKulBot/src/teams_browser_scraper.py)**: Playwright Chromium scraper cào dữ liệu kênh MS Teams REPORT.
* **[teams_report_parser.py](file:///d:/TestProject/TomAssistantKulBot/src/teams_report_parser.py)**: Bộ bóc tách và định dạng báo cáo tiến độ chuẩn.
* **Thư mục `src/browser_profile`**: Lưu trữ cookies, session đăng nhập Microsoft SSO của sếp.

### 2. Cấu Hình & Dữ Liệu (`config/` & `data/`)
* **[telegram_config.json](file:///d:/TestProject/TomAssistantKulBot/config/telegram_config.json)**: Cấu hình `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `GEMINI_API_KEY`.
* **[pending_requests.json](file:///d:/TestProject/TomAssistantKulBot/data/pending_requests.json)**: Cache danh sách các đơn phép đang chờ duyệt.
* **[last_seen_requests.json](file:///d:/TestProject/TomAssistantKulBot/data/last_seen_requests.json)**: Cache danh sách tiêu đề email đã đọc (chống trùng lặp).
* **[approved_history.json](file:///d:/TestProject/TomAssistantKulBot/data/approved_history.json)**: Nhật ký lịch sử các đơn phép đã duyệt thành công.
* **[telegram_commands.json](file:///d:/TestProject/TomAssistantKulBot/data/telegram_commands.json)**: Hàng đợi lưu lệnh lập trình từ xa do sếp gửi qua lệnh `/run`.

### 3. Công Cụ & Cài Đặt (`tools/`)
* **[run_bot_background.vbs](file:///d:/TestProject/TomAssistantKulBot/tools/run_bot_background.vbs)**: Script VBS khởi chạy bot ẩn dưới nền Windows.
* **[install_bot_startup.ps1](file:///d:/TestProject/TomAssistantKulBot/tools/install_bot_startup.ps1)**: Script đăng ký bot tự động khởi động cùng Windows Startup.
* **[install_scheduler.ps1](file:///d:/TestProject/TomAssistantKulBot/tools/install_scheduler.ps1)**: Script đăng ký tác vụ quét mail định kỳ vào Windows Task Scheduler.
* **[send_telegram_msg.py](file:///d:/TestProject/TomAssistantKulBot/src/send_telegram_msg.py)**: Script tiện ích gửi thông báo Telegram.

---

## ⚡ Các Lệnh Điều Khiển Qua Telegram

Sếp có thể nhắn trực tiếp hoặc dùng menu nút bấm trên Telegram:

* 📊 `/report` - Tổng hợp báo cáo tiến độ công việc trong ngày từ kênh MS Teams REPORT (khớp định dạng chuẩn).
* 📅 `/calendar` - Quét và hiển thị danh sách lịch họp, sự kiện trong ngày hôm nay từ Outlook Desktop.
* 🏸 `/scan` - Quét Outlook tìm các đơn nghỉ phép chưa đọc. Nếu có, bot hiển thị thông tin kèm 2 nút bấm: **Duyệt phép (Accept)** (sử dụng Playwright tự động bấm duyệt) và **Mở link web** (mở URL trực tiếp trên trình duyệt của sếp).
* 📧 `/count` - Đếm tổng số email và số email chưa đọc sếp nhận được trong ngày hôm nay.
* 🔑 `/login` - Mở trình duyệt Chrome headful (hiển thị) trên máy sếp trỏ đến trang quản lý phép để sếp đăng nhập Microsoft SSO & xác thực MFA lần đầu (giữ mở 90 giây rồi tự đóng).
* 🖥️ `/status` - Kiểm tra sức khỏe máy tính (HĐH, phiên bản Python, trạng thái kết nối Outlook Desktop, trạng thái bot).
* 📋 `/logs` - In ra 15 dòng nhật ký hoạt động mới nhất từ file `bot.log`.
* 🔄 `/restart` - Khởi động lại Bot từ xa để nạp lại mã nguồn mới.
* 💻 `/run <mệnh lệnh>` - Gửi lệnh lập trình từ xa cho IDE Agent thực thi trực tiếp trên workspace.
* 🟢 `/scanon` - Kích hoạt chế độ kiểm tra hàng đợi lệnh từ xa của IDE Agent.
* 🔴 `/scanoff` - Tắt chế độ nhận lệnh để IDE Agent không hoạt động ngầm (tiết kiệm token và tài nguyên).

---

## ⚙️ Cơ Chế Đồng Bộ & Hoạt Động Ngầm

### 1. Cơ chế Quét Email Tự Động
Hệ thống sử dụng cơ chế kép để phát hiện email nghỉ phép mới:
* **Chạy ngầm (Proactive Thread):** Một luồng phụ trong `telegram_agent.py` quét hòm thư Outlook cứ mỗi **5 phút** một lần. Nếu phát hiện email xin nghỉ phép mới (chưa có trong `last_seen_requests.json`), nó sẽ chủ động gửi tin nhắn báo về Telegram cho sếp kèm nút bấm duyệt nhanh.
* **Task Scheduler:** Lên lịch qua Windows Task Scheduler (`OutlookLeaveChecker`) chạy mỗi **30 phút** trong khung giờ hành chính (9:00 - 12:00 & 13:30 - 16:30, T2 - T6). Khi phát hiện đơn phép mới, nó hiển thị một Windows Dialog Popup trực tiếp trên màn hình của sếp để sếp bấm OK để mở trình duyệt duyệt phép ngay.

### 2. Cầu Nối Lệnh Lập Trình Từ Xa (`/run`)
Khi sếp gửi lệnh từ xa bằng `/run <nội dung>`, quy trình hoạt động như sau:
1. Bot ghi nhận nội dung câu lệnh vào [telegram_commands.json](file:///d:/TestProject/TomAssistantKulBot/telegram_commands.json) với trạng thái `"PENDING"`.
2. Khi IDE Agent đang chạy (có thể cài đặt qua Cron Job hoặc loop rảnh rỗi):
   * Đọc cấu hình `telegram_config.json`. Nếu `REMOTE_SCAN_ENABLED` là `false` -> Phản hồi `HEARTBEAT_OK` lập tức.
   * Nếu là `true` -> Kiểm tra `telegram_commands.json`. Nếu thấy trạng thái `"PENDING"`:
     * Chuyển trạng thái thành `"IN_PROGRESS"`.
     * Thực hiện phân tích và thực thi mệnh lệnh của sếp trực tiếp trên workspace.
     * Khi hoàn thành, chuyển trạng thái thành `"COMPLETED"` (hoặc `"FAILED"` nếu lỗi).
     * Gọi script `send_telegram_msg.py` để gửi kết quả kèm báo cáo cụ thể về Telegram cho sếp.

---

## 🛠️ Hướng Dẫn Sửa Lỗi Thường Gặp (Troubleshooting)

### 1. Lỗi kẹt Chromium của Playwright (`browser_profile` folder locked)
* **Triệu chứng:** Khi sếp bấm duyệt nhanh hoặc chạy lệnh `/login` nhưng trình duyệt không xuất hiện, kiểm tra log thấy lỗi:
  `playwright._impl._api_types.Error: BrowserType.launch_persistent_context: ... Open in existing browser session`
* **Nguyên nhân:** Tiến trình Chrome chạy ngầm trước đó bị kẹt chưa đóng hẳn, dẫn đến việc khóa thư mục profile.
* **Cách xử lý:** Chạy lệnh PowerShell sau để giải phóng các tiến trình Chrome của Playwright:
  ```powershell
  Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*ms-playwright*" } | Stop-Process -Force
  ```

### 2. Lỗi Threading COM của Outlook trên Windows
* **Triệu chứng:** Gặp lỗi khi gọi API `win32com.client.Dispatch("Outlook.Application")` trong các thread phụ của Bot.
* **Nguyên nhân:** Windows yêu cầu khởi tạo môi trường COM đa luồng (Multi-threaded Apartment) khi gọi từ thread phụ.
* **Cách xử lý:** Bao bọc cuộc gọi COM bằng thư viện `pythoncom`:
  ```python
  import pythoncom
  pythoncom.CoInitialize()
  try:
      # Thực thi kết nối Outlook tại đây
  finally:
      pythoncom.CoUninitialize()
  ```

### 3. Sửa Lỗi và Nạp Lại Mã Nguồn
* Sau khi chỉnh sửa mã nguồn trong `telegram_agent.py`, sếp (hoặc IDE Agent) chỉ cần nhắn tin `/restart` tới Bot. Bot sẽ tự động khởi động lại tiến trình Python của chính nó thông qua cuộc gọi hệ thống `os.execv` để nạp mã nguồn mới mà không cần sếp phải vào Terminal gõ lệnh thủ công.
