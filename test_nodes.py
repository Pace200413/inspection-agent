from src.agent.nodes import retrieve, grade

state = {
    "question": "What causes D-cracking in concrete?",
    "queries": ["What causes D-cracking in concrete?"],
    "retrieved": [], "relevant": [], "rewrite_count": 0, "answer": "",
}
state.update(retrieve(state))
print(f"Retrieved: {len(state['retrieved'])} chunks")
state.update(grade(state))
print(f"Survived grading: {len(state['relevant'])}")
for c in state["relevant"]:
    print(" KEPT:", c["id"])