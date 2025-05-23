import os
from dotenv import load_dotenv

# OpenAI API config
MODEL = "gpt-4o-mini"  # Options: gpt-3.5-turbo, gpt-4
TEMPERATURE = 0.2
MAX_TOKENS = 8192  # Maximum tokens for the response

# Chunk size for splitting the transcript
BLOCK_SIZE = 20
# Chunk overlap size
CHUNK_OVERLAP = 2

# Load environment variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
