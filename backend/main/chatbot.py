from fastapi import FastAPI
from pydantic import BaseModel
# from google.gemini import GeminiClient


app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Your security AI logic here

    def process_security_query(ChatRequest):
        #everything
       

        return response
    

    response = process_security_query(request.message)
    return {"response": response}