from src.devmate.rag.retriever import RAGRetriever

def test_ingest_documents():
    """测试ingest_documents方法，验证处理没有文档的情况"""
    try:
        retriever = RAGRetriever()
        retriever.ingest_documents()
        print("ingest_documents方法执行成功")
        return True
    except Exception as e:
        print(f"ingest_documents方法执行失败: {e}")
        return False

if __name__ == "__main__":
    print("测试RAGRetriever的ingest_documents方法...")
    test_ingest_documents()
