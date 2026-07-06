import sys
from src.agent.graph import build_graph

question = " ".join(sys.argv[1:]) or "What repair methods are suitable for dormant cracks?"

app = build_graph()
state = {
    "question": question, "queries": [question],
    "retrieved": [], "relevant": [], "rewrite_count": 0, "answer": "",
}

print(f"Q: {question}\n" + "=" * 70)
for step in app.stream(state):
    for node_name, update in step.items():
        if node_name == "retrieve":
            print(f"[retrieve] got {len(update['retrieved'])} chunks")
        elif node_name == "grade":
            kept = [c["id"] for c in update["relevant"]]
            print(f"[grade] kept {len(kept)}: {kept}")
        elif node_name == "rewrite":
            print(f"[rewrite] new queries: {update['queries']}")
        elif node_name == "generate":
            print("=" * 70 + "\n" + update["answer"])