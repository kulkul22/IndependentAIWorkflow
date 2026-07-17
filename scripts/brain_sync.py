import os
import sys
import glob
import time
from filelock import FileLock
import chromadb
from chromadb.utils import embedding_functions

sys.stdout.reconfigure(encoding='utf-8')

# Config paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VAULT_DIR = os.path.join(PROJECT_ROOT, 'brain', 'vault')
DB_DIR = os.path.join(PROJECT_ROOT, 'brain', 'chroma_db')
LOCK_FILE = os.path.join(PROJECT_ROOT, 'brain', 'sync.lock')

def sync_vault():
    print(f"Bắt đầu đồng bộ Second Brain tại {VAULT_DIR}...")
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Default embedding function (uses all-MiniLM-L6-v2 by default)
    # We can switch to OpenAI/Gemini embeddings later if needed.
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name="second_brain",
        embedding_function=sentence_transformer_ef
    )
    
    # Find all markdown files
    md_files = glob.glob(os.path.join(VAULT_DIR, '**', '*.md'), recursive=True)
    
    documents = []
    metadatas = []
    ids = []
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if not content:
                continue
                
            # Get relative path for the ID
            rel_path = os.path.relpath(file_path, VAULT_DIR)
            mtime = os.path.getmtime(file_path)
            
            # Simple chunking (by file for now, can be improved to split by paragraph)
            documents.append(content)
            metadatas.append({"source": rel_path, "mtime": mtime})
            ids.append(rel_path)
            
        except Exception as e:
            print(f"Lỗi khi đọc file {file_path}: {e}")
            
    if documents:
        # Upsert into ChromaDB
        # This will add new docs and update existing ones if ID matches
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Đã đồng bộ {len(documents)} ghi chú vào Second Brain.")
    else:
        print("Không tìm thấy ghi chú nào để đồng bộ.")

def main():
    print("Đang chờ lock để đồng bộ...")
    # Use filelock to prevent concurrent syncs
    lock = FileLock(LOCK_FILE, timeout=10)
    try:
        with lock:
            sync_vault()
    except Exception as e:
        print(f"Không thể lấy lock hoặc có lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()
