# Gemini Chatbot API

A simple chatbot backend built with **FastAPI** and powered by **Google's Gemini API**. It exposes a REST endpoint that takes a user message and returns an AI-generated response.

## Features

- 🚀 Fast, lightweight backend using FastAPI
- 🤖 Conversational responses powered by Google Gemini
- 🔐 API key managed securely via environment variables
- 📄 Interactive API docs (Swagger UI) out of the box

## Tech Stack

- **Backend Framework:** FastAPI
- **AI Model:** Google Gemini API
- **Language:** Python 3.9+
- **Server:** Uvicorn

## Project Structure

```
gemini-chatbot/
├── main.py              # FastAPI app and routes
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API key) - not committed
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.9 or higher
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/gemini-chatbot.git
   cd gemini-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the App

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:
```
http://127.0.0.1:8000
```

Interactive Swagger docs:
```
http://127.0.0.1:8000/docs
```

## API Usage

### `POST /chat`

Send a message to the chatbot and receive a response.

**Request body:**
```json
{
  "message": "Hello, how are you?"
}
```

**Response:**
```json
{
  "response": "I'm doing great, thanks for asking! How can I help you today?"
}
```

**Example with cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello!"}'
```

## Requirements File

Example `requirements.txt`:
```
fastapi
uvicorn
google-generativeai
python-dotenv
pydantic
```

## Environment Variables

| Variable         | Description                          |
|------------------|---------------------------------------|
| `GEMINI_API_KEY` | Your Google Gemini API key            |

## Future Improvements

- [ ] Add conversation history / memory
- [ ] Add streaming responses
- [ ] Add authentication for API access
- [ ] Deploy to a cloud platform (Render, Railway, etc.)



## Author

Built with ❤️ using FastAPI and Google Gemini.
