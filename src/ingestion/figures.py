import base64, json, sys
import fitz  # pip install pymupdf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

PROMPT = """This page from concrete repair manual EM 1110-2-2002 contains a figure
(a decision flowchart or table). Transcribe its complete logical content into plain,
detailed text. If it is a decision tree, write out every path as
'If X -> then Y' statements. Include the figure number and title."""

pdf_page = int(sys.argv[1])  # 1-based PDF page number
doc = fitz.open("data/raw_docs/em_1110-2-2002.pdf")
pix = doc[pdf_page - 1].get_pixmap(dpi=200)
img_b64 = base64.b64encode(pix.tobytes("png")).decode()

msg = HumanMessage(content=[
    {"type": "text", "text": PROMPT},
    {"type": "image_url", "image_url": f"data:image/png;base64,{img_b64}"},
])
print(llm.invoke([msg]).content)