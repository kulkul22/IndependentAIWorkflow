import os
import sys
import time
import queue
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VAULT_DIR = os.path.join(PROJECT_ROOT, 'brain', 'vault')

# Import our refactored sync logic directly to keep models in RAM
from brain_sync import get_collection, sync_files

class VaultChangeHandler(FileSystemEventHandler):
    def __init__(self, update_queue):
        super().__init__()
        self.update_queue = update_queue

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self.update_queue.put(event.src_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self.update_queue.put(event.src_path)

def start_daemon():
    print(f"Khởi động Javis Daemon giám sát thư mục: {VAULT_DIR}")
    
    # Initialize ChromaDB and ONNX Model ONCE
    collection = get_collection()
    update_queue = queue.Queue()
    
    event_handler = VaultChangeHandler(update_queue)
    observer = Observer()
    observer.schedule(event_handler, VAULT_DIR, recursive=True)
    observer.start()
    
    # Initial full sync
    print("[DAEMON] Chạy đồng bộ lần đầu (toàn bộ vault)...")
    sync_files(collection, VAULT_DIR)
    
    try:
        while True:
            # Batch process queue with a 15-second debounce window
            time.sleep(15) 
            
            changed_files = set()
            while not update_queue.empty():
                try:
                    path = update_queue.get_nowait()
                    changed_files.add(path)
                except queue.Empty:
                    break
            
            if changed_files:
                print(f"\n[DAEMON] Phát hiện {len(changed_files)} file thay đổi. Đang đồng bộ...")
                sync_files(collection, VAULT_DIR, specific_files=list(changed_files))
                print("[DAEMON] Đồng bộ hoàn tất.")
                
    except KeyboardInterrupt:
        observer.stop()
        print("\n[DAEMON] Đã dừng Javis Daemon.")
    observer.join()

if __name__ == "__main__":
    start_daemon()
