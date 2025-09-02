# Ai-Powred-Code-Review-System
## Gemini Code Reviewer API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

An intelligent, lightweight code review service powered by **FastAPI**, **Google Gemini**, and **MongoDB**. This API provides a simple yet powerful endpoint to submit code for analysis, receive AI-driven feedback, and persist review history.

It serves as a perfect backend for developer tools, CI/CD pipelines, or educational platforms.

---

## ✨ Key Features

- **AI-Powered Reviews**: Leverages the power of Google Gemini via LangChain for insightful code analysis.
- **Asynchronous API**: Built with FastAPI and Motor for high-performance, non-blocking operations.
- **Persistent Storage**: Seamlessly stores code submissions and their reviews in MongoDB for future reference.
- **Simple & Scalable**: A clean, modular structure that is easy to understand, test, and extend.
- **Ready to Deploy**: Includes clear setup, testing, and usage instructions.

---

## ⚙️ How It Works

The application follows a simple data flow:

1. **Request**: A client sends a `POST` request with a JSON payload containing the code to the `/review` endpoint.
2. **Processing**: FastAPI receives the request and passes the code to the `reviewer` module.
3. **AI Analysis**: The `reviewer` module invokes the Gemini model to analyze the code for bugs, style, and optimizations.
4. **Database Storage**: The original code and the AI-generated review are saved as a new document in the MongoDB `reviews` collection.
5. **Response**: The AI-generated review is returned to the client as a JSON response.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+
- **API Framework**: FastAPI
- **AI Integration**: LangChain with `langchain-google-genai`
- **Database**: MongoDB with `motor` (asynchronous driver)
- **Server**: Uvicorn
- **Environment Management**: `python-dotenv`

---

## 📂 Project Structure

```
.
├── reviewer.py        # Gemini-based code review logic
├── main.py            # FastAPI server with /review endpoint
├── test_request.py    # Test script for API endpoint
├── test_mongo.py      # Test MongoDB connectivity
├── .env               # Environment variables
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## ⚙️ Requirements

- **Python** 3.9+
- **pip** for dependency management
- Google **Gemini API Key**
- **MongoDB URI** (optional for DB testing)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/code-review-api.git
   cd code-review-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory and add:

```
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=your_mongodb_connection_string_here  # Optional
```

---

## ▶️ Running the FastAPI Server

Start the server:

```bash
uvicorn main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

---

## 📌 API Endpoints

1. POST /review
Reviews a given code snippet using Gemini AI.

Request Body (JSON):
{
  "code": "def add(a, b): return a+b"
}

Sample cURL:
curl -X POST "http://127.0.0.1:8000/review" \
-H "Content-Type: application/json" \
-d '{"code": "def add(a, b): return a+b"}'

Response Example:
{
  "review": "✅ No major issues. Consider adding type hints and docstrings for clarity."
}

2. GET /reviews
Fetch all reviews (supports optional limit query parameter).

Query Parameters:
limit (integer, optional, default=100): Number of reviews to return

Sample cURL:
curl -X GET "http://127.0.0.1:8000/reviews?limit=50"

Response Example:
[
  {
    "_id": "64f8b7a3e8f6b5aadab75d2d",
    "code": "def add(a, b): return a+b",
    "language_detected": "Python",
    "issues": [],
    "suggestions": ["Add type hints", "Add docstrings"],
    "improved_code": "def add(a: int, b: int) -> int: return a+b",
    "details": {
      "pygments": {"language": "Python", "confidence": 0.8},
      "gemini": {"language": "Python", "confidence": 0.9}
    }
  }
]

3. GET /reviews/{review_id}
Fetch a single review by its _id.

Path Parameter:
review_id (string, required): The MongoDB ObjectId of the review

Sample cURL:
curl -X GET "http://127.0.0.1:8000/reviews/64f8b7a3e8f6b5aadab75d2d"

Response Example:
{
  "_id": "64f8b7a3e8f6b5aadab75d2d",
  "code": "def add(a, b): return a+b",
  "language_detected": "Python",
  "issues": [],
  "suggestions": ["Add type hints", "Add docstrings"],
  "improved_code": "def add(a: int, b: int) -> int: return a+b",
  "details": {
    "pygments": {"language": "Python", "confidence": 0.8},
    "gemini": {"language": "Python", "confidence": 0.9}
  }
}

4. GET /reviews/by-language/{language}
Fetch reviews filtered by detected programming language.

Path Parameter:
language (string, required): Language to filter reviews by (e.g., Python, JavaScript)

Query Parameters:
limit (integer, optional, default=100): Maximum number of reviews to return

Sample cURL:
curl -X GET "http://127.0.0.1:8000/reviews/by-language/Python?limit=10"

Response Example:
[
  {
    "_id": "64f8b7a3e8f6b5aadab75d2d",
    "code": "def add(a, b): return a+b",
    "language_detected": "Python",
    "issues": [],
    "suggestions": ["Add type hints", "Add docstrings"],
    "improved_code": "def add(a: int, b: int) -> int: return a+b",
    "details": {
      "pygments": {"language": "Python", "confidence": 0.8},
      "gemini": {"language": "Python", "confidence": 0.9}
    }
  }
]


---

## ✅ Testing the API

Use the provided `test_request.py`:

```bash
python test_request.py
```

Expected output:
```
Status Code: 200
Response JSON: { "review": "...review details..." }
```

---

## ✅ Testing MongoDB Connection (Optional)

Use the provided `test_mongo.py`:

```bash
python test_mongo.py
```

Expected output:
```
✅ MongoDB connection successful!
```

---

## 📜 requirements.txt

```
fastapi
uvicorn
langchain-google-genai
python-dotenv
requests
motor
```

---

## 👨‍💻 Author

**Your Name**  
[GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-profile)

---
