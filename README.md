# 🌐 NaoMedTranslator

A multilingual chat application designed for medical professionals and patients to communicate seamlessly across language barriers, featuring real-time translation, text-to-speech (TTS), and WebSocket-based messaging.

---

## 🚀 Deployment Process

### Development Setup
To run the application locally during development:

```bash
uvicorn app.main:app --reload
```

### Production Setup
For production deployment, use Hypercorn to support ASGI with WebSocket capabilities:

```bash
hypercorn app.main:app
```

### Session Secret Key Generation
A secure session secret key is generated using Python's `secrets` module:

```python
import secrets
# Generate a 32-byte (256-bit) random hex string
secret_key = secrets.token_hex(32)
# Example output: '3fa6b4d28f... (64 characters)'
```

This key is used for session middleware in the FastAPI application.

---

## 🌍 Vercel Deployment

A separate branch (`vercel-deployment`) is maintained for deploying to Vercel. This branch integrates:
- **Vercel Blob** for audio file storage.
- **Ably WebSocket Service** for real-time chat.

### Steps to Deploy
1. **Push to GitHub**:
   - Push the `vercel-deployment` branch to your GitHub repository.
2. **Deploy on Vercel**:
   - Create a new project in Vercel, linking to the `vercel-deployment` branch.
   - Add environment variables in Vercel:
     - `OPENAI_API_KEY`: Your OpenAI API key.
     - `ABLY_API_KEY`: Your Ably API key.
     - `BLOB_READ_WRITE_TOKEN`: Automatically added by Vercel Blob.
   - Deploy the app to see live behavior.

---

## 🔍 Post-Deployment Tasks

### Required
- **Switch to Azure TTS**: Currently using `gTTS` for text-to-speech; replace with Azure TTS for better quality and language support.
- **Replace Fake Database**:
  - Replace `fake_db` in `app/database.py` with a real database (e.g., PostgreSQL or MongoDB).
- **Test Cases**:
  - Add unit and integration tests in the `tests/` directory to ensure functionality.
- **Validate Language Support**:
  - Check supported languages for translation and TTS.
  - Fix the issue where Russian text is not typed properly.
- **Completed Tasks**:
  - Replaced `secret_key="your-secret-key"` with a real key (generated above).
  - Cleaned up `requirements.txt` to remove unused dependencies.
  - Restructured the project (see Folder Structure below).
  - Loaded environment variables using Vercel’s dashboard instead of `load_env()` or `.ps1` scripts.

### Optional TODOs
- **Role-Based Access**:
  - Doctors can see a list of assigned patients.
  - Patients can only see themselves and their doctor.
- **Dockerization**:
  - Dockerize the application for consistent deployment across environments.
- **Database Integration**:
  - Use PostgreSQL or MongoDB to persistently store `chat_history`.
- **Caching for WebSockets**:
  - Implement Redis to manage `active_connections` for real-time WebSocket handling.
- **Session Management**:
  - Automatically remove user sessions after a set period of inactivity.

---

## 📋 Before Pushing to Repository

- **Update `requirements.txt`**:
  - Always run the following command to ensure dependencies are up-to-date:
    ```bash
    pip freeze > requirements.txt
    ```

---

## 📂 Folder Structure

The project is organized for modularity and maintainability:

```
.
├── .venv/                    # Virtual environment
├── app/                      # Main application directory
│   ├── __init__.py           # Marks app/ as a Python package
│   ├── main.py              # Application setup and router includes
│   ├── dependencies.py      # Dependency functions (e.g., get_current_user, get_current_user_ws)
│   ├── database.py          # Database setup (currently fake_db, pwd_context)
│   ├── schemas.py           # Pydantic models for requests and responses
│   ├── services/            # Business logic
│   │   ├── translator.py    # Translation logic (translate_message)
│   │   └── audio.py         # Text-to-speech logic (text_to_speech)
│   ├── routers/             # API routes
│   │   ├── auth.py          # Authentication routes (login/logout)
│   │   ├── home.py          # Home route (GET /)
│   │   └── chat.py          # Chat routes (WebSocket & history endpoints)
│   ├── static/              # Static files (e.g., CSS, JS, Audio Files)
│   └── templates/           # HTML templates (e.g., home.html)
├── tests/                   # Test cases
│   └── test_*.py            # Unit and integration tests
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🛠️ Technologies Used

| **Component**         | **Technology**         |
|-----------------------|------------------------|
| **Backend Framework** | FastAPI               |
| **WebSocket Service** | Ably                  |
| **Storage**           | Vercel Blob           |
| **Translation**       | OpenAI API (GPT-4)    |
| **Text-to-Speech**    | gTTS (to be Azure TTS)|
| **Templating**        | Jinja2                |

---

## 📝 Notes
- Ensure all environment variables are securely stored in Vercel’s dashboard.
- Monitor Ably’s free plan limits (200 concurrent connections, 6M messages/month) during testing.
- Before Pushing Always update requirements.txt.