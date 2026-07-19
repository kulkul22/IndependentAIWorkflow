import os
import glob
import sqlite3
import chromadb
from chromadb.utils import embedding_functions

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_DIR = os.path.join(PROJECT_ROOT, 'brain', 'chroma_db')

def _enable_sqlite_wal_mode():
    """Enable WAL before Chroma opens the persistent SQLite database."""
    os.makedirs(DB_DIR, exist_ok=True)
    database_path = os.path.join(DB_DIR, 'chroma.sqlite3')

    with sqlite3.connect(database_path) as connection:
        result = connection.execute("PRAGMA journal_mode=WAL").fetchone()

    if not result or result[0].lower() != 'wal':
        raise RuntimeError("Failed to enable SQLite WAL mode for ChromaDB")

def get_collection():
    """Khởi tạo ChromaDB và Model 1 lần duy nhất để lưu trên RAM."""
    print("[RAG] Đang tải mô hình nhúng (Embedding Model) vào RAM. Vui lòng đợi...")
    _enable_sqlite_wal_mode()
    client = chromadb.PersistentClient(
        path=DB_DIR,
        settings=chromadb.Settings(
            sqlite_wal_mode=True
        )
    )
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="second_brain",
        embedding_function=sentence_transformer_ef
    )
    return collection

def sync_files(collection, vault_dir, specific_files=None):
    """Đồng bộ danh sách file cụ thể, hoặc toàn bộ thư mục nếu không truyền specific_files."""
    if specific_files:
        md_files = specific_files
    else:
        md_files = glob.glob(os.path.join(vault_dir, '**', '*.md'), recursive=True)
    
    documents = []
    metadatas = []
    ids = []
    
    for file_path in md_files:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if not content:
                continue
                
            rel_path = os.path.relpath(file_path, vault_dir)
            mtime = os.path.getmtime(file_path)
            
            documents.append(content)
            metadatas.append({"source": rel_path, "mtime": mtime})
            ids.append(rel_path)
            
        except Exception as e:
            print(f"Lỗi khi đọc file {file_path}: {e}")
            
    if documents:
        try:
            collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Đã đồng bộ {len(documents)} ghi chú vào Second Brain.")
        except Exception as e:
            print(f"Lỗi khi ghi vào ChromaDB: {e}")
    else:
        if not specific_files:
            print("Không tìm thấy ghi chú nào để đồng bộ.")
