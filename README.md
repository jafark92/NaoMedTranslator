# NaoMedTranslator

# Process of Deployment



Deploy to see the behavior on live

**After Deployment **

- Use Azure TTS, for now using gTTS
- `secret_key="your-secret-key` Replace with a real key
- Cleaning requirements.txt
- ~~Restructure project~~
- Test cases
- Removing fake_db with real one
- ~~Load Env Variables using .ps1 command instead of load_end()~~ Vercel add them in env during deployment

**Before Pushing Always update requirements.txt**

**Folder Structure**
.
├── .venv
├── app
│   ├── __init__.py
│   ├── main.py             # Only application setup & router includes
│   ├── dependencies.py     # get_current_user, get_current_user_ws, etc.
│   ├── database.py         # fake_db, pwd_context
│   ├── schemas.py          # Pydantic models for requests & responses
│   ├── services/
│   │   ├── translator.py   # translate_message
│   │   └── audio.py        # text_to_speech
│   ├── routers/
│   │   ├── auth.py         # login/logout routes
│   │   ├── home.py         # GET /
│   │   └── chat.py         # WebSocket & history endpoints
│   ├── static/
│   └── templates/
└── tests/
│    └── test_*.py
├── requirements.txt
└── README.md