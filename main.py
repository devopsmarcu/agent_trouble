from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.rag import query_local_db
from agent.web_search import search_web
from agent.ingest import ingest_validated_answer
import uvicorn

app = FastAPI(title="Agente de Suporte Técnico Híbrido", description="Local RAG + Web Fallback")

class QueryRequest(BaseModel):
    query: str
    mode: str = "auto"  # 'auto', 'local', 'web'

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    context: str
    source: str
    is_helpful: bool

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    mode = request.mode.lower()
    
    # 1. Tentar base local se não for estritamente web
    if mode in ["auto", "local"]:
        try:
            local_response = query_local_db(request.query)
            
            # Se for apenas local, retorna mesmo se não tiver certeza (para forçar o uso da base)
            if mode == "local" or (local_response and local_response.is_sufficient):
                return {
                    "source": "local",
                    "answer": local_response.text if local_response.text else "Não encontrei referências suficientes na base local para essa pergunta.",
                    "context": local_response.context,
                    "url": "N/A"
                }
        except Exception as e:
            print(f"Error querying local DB: {e}")
            if mode == "local": return {"source": "local", "answer": f"Erro interno: {e}", "context": ""}
    
    # 2. Pesquisa web 
    try:
        web_response = search_web(request.query)
        
        return {
            "source": "web",
            "answer": web_response['answer'],
            "context": web_response['context'],
            "url": web_response['url'],
            "needs_feedback": True
        }
    except Exception as e:
        return {"source": "error", "answer": f"Erro ao consultar web: {e}"}

@app.post("/feedback")
async def provide_feedback(request: FeedbackRequest):
    if request.is_helpful:
        # 3. Ingestão e verificação de duplicidade
        success = ingest_validated_answer(
            query=request.query,
            answer=request.answer,
            context=request.context,
            source=request.source
        )
        if success:
            return {"message": "Conhecimento salvo com sucesso na base local!"}
        else:
            return {"message": "Conhecimento já existia na base local ou houve um erro ao salvar."}
    
    return {"message": "Feedback registrado. Solução descartada e não armazenada."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
