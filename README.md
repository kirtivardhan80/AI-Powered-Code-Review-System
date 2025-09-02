# AI-Powered-Code-Review-System

# Code Review Agent (FastAPI + Gemini + MongoDB)

A simple code review service built with **FastAPI**, **Gemini API (LangChain)**, and **MongoDB (Motor)**. This application allows you to send code snippets for review, get suggestions from Gemini, and optionally store reviews in MongoDB.

---

## ✅ Features
- Accepts code snippets via **FastAPI POST endpoint**
- Uses **Google Gemini API** (via LangChain) for code review
- Stores code reviews in **MongoDB Atlas** (using `motor`)
- Includes **test scripts** for API and MongoDB connection
- Environment variables managed via `.env`

---

## 📂 Project Structure
```
.
├── main.py             # FastAPI app
├── reviewer.py         # Gemini review logic
├── db.py               # MongoDB connection
├── test_request.py     # Test FastAPI POST endpoint
├── test_mongo.py       # Test MongoDB connection
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── README.md           # Project documentation
```

---

## ⚙️ Requirements
- Python 3.10+
- [MongoDB Atlas](https://www.mongodb.com/atlas/database)
- [Google AI Studio (Gemini API key)](https://ai.google.dev/)

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/code-review-agent.git
   cd code-review-agent
   ```

2. **Create Virtual Environment & Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Linux/Mac
   venv\Scripts\activate         # On Windows

   pip install -r requirements.txt
   ```

3. **Set Up `.env` File**
   Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key
   MONGO_URI=your_mongodb_connection_string
   ```

---

## ▶️ Running the App
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

Server will run at:
```
http://127.0.0.1:8000
```

Swagger docs:
```
http://127.0.0.1:8000/docs
```

---

## 🔗 API Endpoints

### **1. Review Code**
**POST** `/review`

#### ✅ Request:
```json
{
  "code": "def add(a, b): return a + b"
}
```

#### ✅ Response:
```json
{
  "review": "Gemini's review with suggestions and improvements"
}
```

---

## 🧪 Testing

### **Test API Endpoint**
Run:
```bash
python test_request.py
```

Expected Output:
```
Status Code: 200
Response JSON: {"review": "Gemini review response..."}
```

---

### **Test MongoDB Connection**
Run:
```bash
python test_mongo.py
```

Expected Output:
```
✅ MongoDB connection successful!
```

---

## ✅ File Overview

### **main.py**
- Creates FastAPI app
- Defines `/review` POST endpoint
- Calls `reviewer.py` for code analysis
- Optionally saves to MongoDB (`db.py`)

### **reviewer.py**
- Loads `GEMINI_API_KEY`
- Initializes Gemini model
- Sends code snippet for review

### **db.py**
- Connects to MongoDB using `motor`
- Defines `reviews_collection`

---

## ✅ requirements.txt
```
fastapi
uvicorn
langchain-google-genai
motor
python-dotenv
requests
```

---

## ⚠️ Notes
- Ensure `.env` file is created and valid
- MongoDB and Gemini credentials must be correct
- Do not commit `.env` file to GitHub (add it to `.gitignore`)

---

## ✅ License
MIT License

---

## 👨‍💻 Author
**Your Name**  
[GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-profile)

---

