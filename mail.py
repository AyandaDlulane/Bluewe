from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, List
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware


# --- CONFIG ---
genai.configure(api_key="AIzaSyB7YM9cdqEyjLJp1YN7n33hfvWaYBfQOQ8")
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Email Security API is running."}

# --- MODELS ---
# class EmailPayload(BaseModel):
#     url: Optional[str] = ""
#     sender: Optional[str] = ""
#     subject: Optional[str] = ""
#     body_text: Optional[str] = ""
#     links: Optional[List[str]] = []

class ExplainPayload(BaseModel):
    original: dict
    question: str
    memorry: Optional[str] = ""


# --- ENDPOINT 1: CHECK ---
@app.post("/api/check")
async def check_email(request: Request):
    data = await request.json()

    # Unpack the same keys your extension sends
    url = data.get("url", "")
    sender = data.get("sender", "")
    subject = data.get("subject", "")
    body_text = data.get("body_text", "")
    links = data.get("links", [])
    prompt = (
        "You are a phishing email detector.\n"
        "Firstly, you should read the url and chech whether it is legitimate or not.\n"
        "Then, check who the sender is and if they have a valid email.\n"
        "Also read the subject and see if there is any suspision of malicious activity (e.g. persuasio to pay for something or do something out of the ordinary).\n"
        "Proceed to reading the text body of the email and check if it aligns with the subject. Check for anything related to payments and due dates and make sure that they are legitimate.\n"
        "Also check for links in the text body that would lead to phishing, scamming or anything related to malware. Make sure that these links do not lead to dangerous sites that can lead to hacking or the damaging of a device.\n"
        "Decide if this email is SAFE or SUSPICIOUS.\n"
        "If the email is SUSPICIOUS, respond with: <short warning>, then comma, then 1, then comma, then a detailed explanation.\n"
        "If the email is SAFE, respond with: <short safe message>, then comma, then 0, then comma, then a detailed explanation.\n"
        "Use the contents of the sender, subject, body, links, and url to make your decision.\n"
        "In or to avoid false positives, only mark as SUSPICIOUS if there is clear evidence of phishing, malware, credential harvesting, or deceptive links/forms.\n"
        "if there is no clear evidence, mark as SAFE.\n"
        "For example, if the sender is from a free email service but the email is about a bank account or sending money, mark that as suspicious.\n"
        "Do not add anything else.\n\n"
        f"Sender: {sender}\n"
        f"Subject: {subject}\n"
        f"Body: {body_text}\n"
        f"Links: {links}\n"
        f"URL: {url}"
    )

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
    except Exception as e:
        return {"response": f"Error: {str(e)}", "status": "2", "details": ""}

    # Expecting: "Warning..., 1, Details..." or "Looks safe, 0, Details..."
    parts = raw_text.split(",", 2)
    response_msg = parts[0].strip() if len(parts) > 0 else raw_text
    status = parts[1].strip() if len(parts) > 1 else "0"
    details = parts[2].strip() if len(parts) > 2 else ""

    return {
        "response": response_msg,
        "status": status,
        "details": details
    }
