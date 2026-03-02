from fastapi import FastAPI
from pydantic import BaseModel
from agent.rag import query_local_db
import uvicorn

app = FastAPI(title="Agente de Suporte Técnico", description="RAG Local")

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        local_response = query_local_db(request.query)

        if local_response and local_response.text:
            return {
                "source": "local",
                "answer": local_response.text,
                "context": local_response.context,
            }
        else:
            return {
                "source": "local",
                "answer": "Não encontrei referências na base de conhecimento para essa pergunta.",
                "context": "",
            }
    except Exception as e:
        return {"source": "error", "answer": f"Erro interno: {e}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
