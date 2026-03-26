from src.devmate.utils.llm import get_llm, get_embeddings

def test_llm_init():
    """测试LLM初始化"""
    try:
        llm = get_llm()
        print("LLM初始化成功")
        return True
    except Exception as e:
        print(f"LLM初始化失败: {e}")
        return False

def test_embeddings_init():
    """测试Embeddings初始化"""
    try:
        embeddings = get_embeddings()
        print("Embeddings初始化成功")
        return True
    except Exception as e:
        print(f"Embeddings初始化失败: {e}")
        return False

if __name__ == "__main__":
    print("测试LLM和Embeddings初始化...")
    test_llm_init()
    test_embeddings_init()
