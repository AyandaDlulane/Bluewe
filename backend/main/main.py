from fastapi import FastAPI, Request
import uvicorn
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# Add this before your routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyBEz5dIsXp-Y0AW9BxjTCv7c-7HmQtK9qk")
model = genai.GenerativeModel("gemini-2.5-flash")

#every thing before the application starts / varaibles and staff
@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/api/check")
async def process_content(request: Request):
    data = await request.json()
    html_content = data.get("html_content", "")
    javascript_content = data.get("javascript_content", "")
    url = data.get("url", "")

    prompt = (
        "Analyze the following website. First, determine what the website is trying to be (its purpose or type, such as banking, shopping, social, etc.). "
        "Then, check if the code and content match this purpose or if there are signs of deception, phishing, or malicious intent. "
        "If the site is suspicious or malicious, respond with a short warning message, then a comma, then the number 1. "
        "If the site is safe and matches its purpose, respond with a short message, then a comma, then the number 0. "
        "Do not add any extra explanation or formatting. "
        f"Here is the data: URL: {url},HTML: {html_content},JavaScript: {javascript_content}"
    )

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        return {"response": f"Error: {str(e)}", "status": "2"}

    ai_response = response.text
    response_data = ai_response.split(',')

    if len(response_data) != 2:
        return {"response": "Error: Unexpected response format from AI model.", "status": "3"}
    return {"response": response_data[0], "status": response_data[1]}











# @app.post("/login-user={username},password={password}")
# async def login_user(username: str, password: str):
#     #creat a var login status
#     return {"status": "success","token": "put_token_here"}