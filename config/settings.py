from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")


# Validate required settings
required_settings = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "OPENAI_CHAT_MODEL": OPENAI_CHAT_MODEL,
    "OPENAI_EMBEDDING_MODEL": OPENAI_EMBEDDING_MODEL,
}

missing = [key for key, value in required_settings.items() if not value]

if missing:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing)}"
    )