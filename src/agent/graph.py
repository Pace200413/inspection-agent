from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent import nodes

MAX_REWRITES = 2
MIN_RELEVANT = 2  # fewer than this = weak retrieval -> try rewriting


def decide_after_grading(state: AgentState) -> str:
    """The agent's key decision: is the evidence good enough?"""
    if len(state["relevant"]) >= MIN_RELEVANT:
        return "generate"
    if state["rewrite_count"] < MAX_REWRITES:
        return "rewrite"
    return "generate"  # out of retries - generate from whatever we have (or refuse)


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("retrieve", nodes.retrieve)
    g.add_node("grade", nodes.grade)
    g.add_node("rewrite", nodes.rewrite)
    g.add_node("generate", nodes.generate)

    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "grade")
    g.add_conditional_edges("grade", decide_after_grading,
                            {"generate": "generate", "rewrite": "rewrite"})
    g.add_edge("rewrite", "retrieve")   # the loop: new queries -> search again
    g.add_edge("generate", END)
    return g.compile()