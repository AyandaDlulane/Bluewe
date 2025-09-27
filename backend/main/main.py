from fastapi import FastAPI
import uvicorn
from google.gemini import GeminiClient



app = FastAPI()

ai = GeminiClient("api_key")

#every thing before the application starts / varaibles and staff



@app.get("/html={html_content},javascript={javascript_content}")
async def process_content(html_content: str, javascript_content: str):
    # Combine HTML and JavaScript content
    combined_content = f"HTML: {html_content}\nJavaScript: {javascript_content}"
    
    # Create a prompt for the AI model
    prompt = f"Analyze the following web content and provide insights:\n{combined_content}"
    
    # Get response from the AI model
    response = ai.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract and return the AI's response
    ai_response = response.choices[0].message['content']
    return {"response": ai_response}




@app.post("/login-user={username},password={password}")
async def login_user(username: str, password: str):
    #creat a var login status
    return {"status": "success","token": "put_token_here"}