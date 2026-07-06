import chromadb
from src.agent.state import AgentState
from src.agent.llm import llm_fast, llm_main

client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection("standards")

TOP_K = 4


def retrieve(state: AgentState) -> dict:
    """Search the vector store with the current queries."""
    seen, results = set(), []
    for q in state["queries"]:
        res = collection.query(query_texts=[q], n_results=TOP_K)
        for id_, text, meta in zip(res["ids"][0], res["documents"][0], res["metadatas"][0]):
            if id_ not in seen:
                seen.add(id_)
                results.append({"id": id_, "text": text, "meta": meta})
    return {"retrieved": results}

GRADE_PROMPT = """You are grading whether a document chunk is relevant to a question.

Question: {question}

Chunk:
{chunk}

Does this chunk contain information that helps answer the question?
Answer with exactly one word: yes or no."""


def grade(state: AgentState) -> dict:
    """Keep only chunks the LLM judges relevant."""
    relevant = []
    for chunk in state["retrieved"]:
        verdict = llm_fast.invoke(
            GRADE_PROMPT.format(question=state["question"], chunk=chunk["text"][:2000])
        ).content.strip().lower()
        if verdict.startswith("yes"):
            relevant.append(chunk)
    return {"relevant": relevant}

REWRITE_PROMPT = """A search over a concrete repair manual (EM 1110-2-2002) failed to find good results.

Original question: {question}
Queries already tried: {queries}

Write 2 NEW search queries using different technical vocabulary that an engineering
manual would use (think: synonyms, causes, mechanisms, related repair methods).
Return exactly 2 queries, one per line, nothing else."""


def rewrite(state: AgentState) -> dict:
    """Generate alternative queries when retrieval was weak."""
    out = llm_fast.invoke(REWRITE_PROMPT.format(
        question=state["question"], queries=state["queries"]
    )).content.strip()
    new_queries = [q.strip("-• ").strip() for q in out.splitlines() if q.strip()][:2]
    return {
        "queries": new_queries,
        "rewrite_count": state["rewrite_count"] + 1,
    }

GENERATE_PROMPT = """You are an assistant for concrete structure inspection, answering
STRICTLY from the provided excerpts of EM 1110-2-2002.

Question: {question}

Excerpts:
{context}

Rules:
1. Answer using ONLY information from the excerpts above.
2. After every factual claim, cite the section in brackets, e.g. [§3-2] or [§6-22].
3. If the excerpts do not contain enough information to answer, say exactly:
   "The available documents do not contain sufficient information to answer this."
   Do not guess. Do not use outside knowledge.

Answer:"""


def generate(state: AgentState) -> dict:
    if not state["relevant"]:
        return {"answer": "The available documents do not contain sufficient information to answer this."}
    context = "\n\n---\n\n".join(c["text"] for c in state["relevant"])
    answer = llm_main.invoke(GENERATE_PROMPT.format(
        question=state["question"], context=context
    )).content
    return {"answer": answer}