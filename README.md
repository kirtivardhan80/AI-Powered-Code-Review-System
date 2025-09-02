# 🚀 Code Review API using Gemini and FastAPI

This project provides an API to **review code snippets** using Google's **Gemini model** via the LangChain integration. It offers:

- ✅ AI-powered **code review** (bugs, best practices, security issues, improvements)
- ✅ **FastAPI endpoint** for easy integration
- ✅ **MongoDB connection test** (optional for future enhancements)
- ✅ **Testing scripts** for API and DB connectivity

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

## 📌 API Endpoint

### **POST /review**
Reviews a given code snippet using Gemini AI.

**Request Body (JSON):**
```json
{
  "code": "def add(a, b): return a+b"
}
```

**Sample cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/review" \
-H "Content-Type: application/json" \
-d '{"code": "def add(a, b): return a+b"}'
```

**Response Example:**
```json
{
  "review": "✅ No major issues. Consider adding type hints and docstrings for clarity."
}
```

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
