# Dự án TomAssistantKulBot

TomAssistantKulBot là một dự án Telegram Bot sử dụng Gemini 2.5 Flash để tự động hóa công việc.
Dự án được xây dựng bằng pyTelegramBotAPI. Nó có khả năng kết nối với máy tính cá nhân để quét email qua Outlook COM API, kiểm tra lịch trình và duyệt web bằng Playwright.

Các chức năng chính:
- Gửi báo cáo hàng ngày (Morning Briefing).
- Phân tích và tóm tắt nội dung báo cáo từ nhân viên.
- Nhắc nhở họp.
- Tự động check và duyệt email từ sếp lớn.

Công nghệ sử dụng:
- Python 3.11
- pyTelegramBotAPI
- win32com.client (Outlook)
- Playwright
- win11toast

## Cấu trúc thư mục:
- `src/bot/handlers.py`: Chứa các hàm xử lý lệnh của bot (ví dụ: `/start`, `/scan`).
- `src/services/outlook_service.py`: Xử lý giao tiếp với Microsoft Outlook.

## Ghi chú
Sếp đặc biệt dặn là không được gọi lệnh xóa file trực tiếp mà phải hỏi trước. Mọi file cấu hình nhạy cảm phải để trong file `.env` không được commit lên git.
