import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()

# Grading & rewriting: many short calls -> Groq (fast, 1000 req/day free)
llm_fast = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_retries=3)

# Final answer generation: Gemini Flash (better quality, ~large daily quota)
llm_main = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, max_retries=3)