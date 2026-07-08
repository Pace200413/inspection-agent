import gradio as gr
from src.agent.graph import build_graph

app_graph = build_graph()

NODE_LABELS = {
    "analyze_image": "🔍 Vision analysis",
    "plan_queries": "🧭 Query planning",
    "retrieve": "📚 Retrieval",
    "grade": "⚖️ Relevance grading",
    "rewrite": "✏️ Query rewrite",
    "generate": "📝 Generation",
}


def run_agent(image, question):
    if not question or not question.strip():
        yield "Please enter a question (or click an example below).", ""
        return
    state = {
        "question": question, "queries": [question],
        "image_path": image if image else "", "defect_findings": {},
        "retrieved": [], "relevant": [], "rewrite_count": 0, "answer": "",
    }
    trace_lines, answer = [], ""
    for step in app_graph.stream(state):
        for node, update in step.items():
            label = NODE_LABELS.get(node, node)
            if node == "analyze_image":
                f = update["defect_findings"]
                dets = [(d["defect_type"], d["severity"]) for d in f.get("findings", [])]
                trace_lines.append(f"{label}: {f.get('defects_found', 0)} defect(s) {dets}")
            elif node == "plan_queries":
                trace_lines.append(f"{label}: {update['queries']}")
            elif node == "retrieve":
                trace_lines.append(f"{label}: {len(update['retrieved'])} chunks")
            elif node == "grade":
                kept = [c["id"] for c in update["relevant"]]
                trace_lines.append(f"{label}: kept {len(kept)} → {kept}")
            elif node == "rewrite":
                trace_lines.append(f"{label}: {update['queries']}")
            elif node == "generate":
                answer = update["answer"]
                trace_lines.append(f"{label}: done")
        yield answer or "_working..._", "\n".join(trace_lines)


with gr.Blocks(title="Agentic Inspection Intelligence") as demo:
    gr.Markdown(
        "# 🏗️ Agentic Multimodal Inspection Intelligence\n"
        "Upload a photo of concrete damage and/or ask a question. "
        "A LangGraph agent orchestrates a fine-tuned YOLOv8 defect detector and a "
        "clause-cited knowledge base built from **EM 1110-2-2002** (USACE concrete repair manual).\n\n"
        "*Every claim is cited to a manual section. The system refuses when the manual "
        "doesn't contain the answer.*"
    )
    with gr.Row():
        with gr.Column(scale=1):
            image_in = gr.Image(type="filepath", label="Inspection photo (optional)")
            question_in = gr.Textbox(label="Question",
                                     placeholder="What repair methods does the manual recommend for the defects in this image?")
            btn = gr.Button("Run inspection", variant="primary")
            gr.Examples(
                examples=[
                    [None, "What repair methods are suitable for dormant cracks?"],
                    ["data/test_images/crack_0548.jpg", "What repair methods does the manual recommend for the defects in this image?"],
                    ["data/test_images/spalling_0372.jpg", "What could have caused the defect shown in this image?"],
                    [None, "What is the airspeed velocity of an unladen swallow?"],
                ],
                inputs=[image_in, question_in],
            )
        with gr.Column(scale=2):
            answer_out = gr.Markdown(label="Inspection answer")
            trace_out = gr.Textbox(label="Agent trace", lines=10)
    btn.click(run_agent, inputs=[image_in, question_in], outputs=[answer_out, trace_out])

demo.launch()