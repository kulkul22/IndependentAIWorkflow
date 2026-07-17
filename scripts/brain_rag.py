import os
import sys
import argparse
import chromadb
from chromadb.utils import embedding_functions

sys.stdout.reconfigure(encoding='utf-8')

# Config paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_DIR = os.path.join(PROJECT_ROOT, 'brain', 'chroma_db')

def query_brain(query_text, n_results=3):
    if not os.path.exists(DB_DIR):
        print("Second Brain chưa được khởi tạo. Vui lòng chạy brain_sync.py trước.")
        return

    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=DB_DIR)
    
    # Default embedding function
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    
    try:
        collection = client.get_collection(
            name="second_brain",
            embedding_function=sentence_transformer_ef
        )
    except Exception as e:
        print("Không tìm thấy dữ liệu trong Second Brain.")
        return
        
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    print(f"--- KẾT QUẢ TÌM KIẾM CHO: '{query_text}' ---\n")
    
    if not results['documents'][0]:
        print("Không tìm thấy thông tin liên quan.")
        return
        
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        dist = results['distances'][0][i]
        
        print(f"[{meta['source']}] (Độ tương đồng: {dist:.4f})")
        print(f"{doc[:500]}...\n")
        print("-" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tìm kiếm thông tin trong Second Brain bằng RAG")
    parser.add_argument("query", help="Câu hỏi hoặc từ khóa cần tìm kiếm")
    parser.add_argument("--n", type=int, default=3, help="Số lượng kết quả trả về")
    
    args = parser.parse_args()
    query_brain(args.query, args.n)
