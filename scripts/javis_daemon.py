import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VAULT_DIR = os.path.join(PROJECT_ROOT, 'brain', 'vault')
SYNC_SCRIPT = os.path.join(PROJECT_ROOT, 'scripts', 'brain_sync.py')

class VaultChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_sync = 0
        self.debounce_seconds = 5 # Prevent multiple syncs in a short time

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self.trigger_sync()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self.trigger_sync()

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.md'):
            self.trigger_sync()

    def trigger_sync(self):
        current_time = time.time()
        if current_time - self.last_sync > self.debounce_seconds:
            self.last_sync = current_time
            print("\n[DAEMON] Phát hiện thay đổi trong Vault. Đang gọi đồng bộ...")
            try:
                # Call sync script
                subprocess.run([sys.executable, SYNC_SCRIPT], check=True)
                print("[DAEMON] Đồng bộ hoàn tất.")
            except subprocess.CalledProcessError as e:
                print(f"[DAEMON] Lỗi khi chạy sync script: {e}")
            except Exception as e:
                print(f"[DAEMON] Lỗi không xác định: {e}")

def start_daemon():
    print(f"Khởi động Javis Daemon giám sát thư mục: {VAULT_DIR}")
    
    # Run initial sync
    print("[DAEMON] Chạy đồng bộ lần đầu...")
    try:
        subprocess.run([sys.executable, SYNC_SCRIPT], check=True)
    except Exception as e:
        print(f"[DAEMON] Lỗi đồng bộ lần đầu: {e}")

    event_handler = VaultChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, VAULT_DIR, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[DAEMON] Đã dừng Javis Daemon.")
    observer.join()

if __name__ == "__main__":
    start_daemon()
