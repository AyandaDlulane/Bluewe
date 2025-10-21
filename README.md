# Bluewe - Your Always-Ready Cyber Attack Chrome Extension

## Description

Bluewe is a Chrome extension designed to provide continuous protection against cyber attacks. It analyzes emails and provides a security layer for users.

## Key Features & Benefits

*   **Real-time Email Analysis:** Analyzes emails for potential phishing attempts and malicious content.
*   **Proactive Threat Detection:** Identifies and flags suspicious emails.
*   **User-Friendly Interface:** Simple and intuitive design for easy use.
*   **Backend Security AI:** Uses AI to process and analysis security query

## Prerequisites & Dependencies

*   **Google Chrome Browser:** Required for running the extension.
*   **Python 3.6+:** Required for the backend server.
*   **FastAPI:** Python web framework for building the API.
*   **uvicorn:** ASGI server for running the FastAPI application.
*   **google-generativeai:** Google's generative AI library.

    ```bash
    pip install fastapi uvicorn google-generativeai
    ```

## Installation & Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AyandaDlulane/Bluewe.git
cd Bluewe
```

### 2. Load the Chrome Extension

1.  Open Google Chrome and navigate to `chrome://extensions`.
2.  Enable "Developer mode" in the top right corner.
3.  Click "Load unpacked" and select the `Blue mail/` directory from the cloned repository.

### 3. Set up the Backend Server

1.  Navigate to the `backend/main/` directory.
2.  Install the required Python packages (if not already installed):

    ```bash
    pip install fastapi uvicorn google-generativeai
    ```
3.  Set up your Google Generative AI API key. Replace `"API_KEY"` in `backend/main/main.py` with your actual API key.

    ```python
    genai.configure(api_key="YOUR_API_KEY")
    ```

4.  Run the backend server:

    ```bash
    uvicorn main.main:app --reload
    ```

    (Note:  `--reload` is useful for development; for production, use a more robust server setup.)

## Usage Examples

Once installed, the Bluewe extension will automatically analyze emails as you view them in Gmail. The extension will display alerts and warnings for potentially malicious emails in the `Blue mail/popup.html` popup.

### Example: Email Analysis

The `Blue mail/content.js` file captures email content and sends it to the backend for analysis.

```javascript
// content.js
(() => {
  // ... (code to extract email content) ...
  fetch(BACKEND_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(emailData)
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response from the backend
    console.log('Backend response:', data);
  });
})();
```

### Example: Backend Chatbot Interaction

The `backend/main/chatbot.py` file shows how to set up a basic chatbot endpoint using FastAPI.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Your security AI logic here
    response = {"message_received": request.message}  # Acknowledge receipt
    return {"response": response}
```

## Configuration Options

*   **`BACKEND_URL` (in `Blue mail/content.js`):** Configure the URL of the backend server.
*   **API Key (in `backend/main/main.py`):** Set your Google Generative AI API Key.

## Project Structure

```
Bluewe/
├── Blue mail/
│   ├── chat.html
│   ├── content.js
│   ├── manifest.json
│   └── popup.html
└── backend/
    └── main/
        ├── .gitignore
        ├── chatbot.py
        └── main.py
        └── phising login/
            ├── __init__.py
            └── __pycache__/
                ├── auth.cpython-313.pyc
                ├── config.cpython-313.pyc
                └── models.cpython-313.pyc
            ├── auth.py
            ├── auth_js
            └── config.py

```

## Contributing Guidelines

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Submit a pull request.

## License Information

License not specified.

## Acknowledgments

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [Google Generative AI](https://ai.google.dev/)
