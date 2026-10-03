from crewai import LLM


llm = LLM(
    model="ollama/qwen2:7b",
    base_url="http://localhost:11434"
)

print("Using local Ollama model: qwen2:7b")


""""
import os

from dotenv import load_dotenv
from crewai import LLM


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

print("HF token loaded:", bool(hf_token))


# ============================================================
# CONFIGURE LLM
# ============================================================

llm = LLM(
    model="openai/gpt-oss-120b:groq",
    api_key=hf_token,
    base_url="https://router.huggingface.co/v1",
    provider="openai"
)
"""

