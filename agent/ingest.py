from llama_index.core import Document, VectorStoreIndex
from agent.rag import get_index, persist_dir
from agent.dedup import is_duplicate, save_metadata

def ingest_validated_answer(query: str, answer: str, context: str, source: str) -> bool:
    if is_duplicate(query, answer):
        return False
    
    # 1. Salvar Metadados (SQLite)
    save_success = save_metadata(query, answer, source)
    if not save_success:
        return False
        
    # 2. Inserir no Vector Store Local
    full_text = f"Pergunta/Problema: {query}\n\nSolução/Resposta: {answer}\n\nContexto Pesquisa: {context}"
    
    metadata = {
        "source": source,
        "type": "validated_feedback",
        "reliability": "Alta",
        "original_query": query
    }
    
    doc = Document(text=full_text, metadata=metadata)
    
    try:
        index = get_index()
        if index:
            index.insert(doc)
            index.storage_context.persist(persist_dir=persist_dir)
        else:
            # Se não existir, criar novo
            index = VectorStoreIndex.from_documents([doc])
            index.storage_context.persist(persist_dir=persist_dir)
        return True
    except Exception as e:
        print(f"Erro ao inserir documento no DB Vetorial: {e}")
        return False
