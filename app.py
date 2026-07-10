import gradio as gr
from src.agent.graph import build_graph

app_graph = build_graph()

# ─────────────────────────────────────────────────────────────────────────────
#  Palette — engineering field-report identity
#    ink    #0b1220   deepest navy (header, trace bg)
#    slate  #1c2f52   primary structural blue
#    steel  #3a5a86   secondary / labels
#    amber  #de9224   caution + refusal accent
#    paper  #f6f8fb   assessment surface
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
html, body, .gradio-container {
  height: 100vh !important; margin: 0 !important; padding: 0 !important;
  overflow: hidden !important;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: #e9eef4 !important;
}
.gradio-container { max-width: 100% !important; }
footer { display: none !important; }
.contain, .main, .wrap { padding: 0 !important; gap: 0 !important; }

/* ── App shell: fixed viewport height, three rows (header / body / footer) ── */
#shell {
  display: flex; flex-direction: column; height: 100vh; overflow: hidden;
}

/* ── Header ── */
#appbar {
  background: linear-gradient(100deg, #0b1220 0%, #1c2f52 60%, #26406b 100%);
  padding: 16px 30px; display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid #22344f;
}
#appbar .brand { display: flex; align-items: baseline; gap: 14px; }
#appbar .mark {
  font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 1.34rem;
  color: #ffffff; letter-spacing: -0.01em;
}
#appbar .mark .amber { color: #de9224; }
#appbar .doc {
  font-size: 0.74rem; letter-spacing: 0.06em; text-transform: uppercase;
  color: #9db3d3; border-left: 1px solid #3a5a86; padding-left: 14px;
}
#appbar .tags { display: flex; gap: 7px; }
#appbar .tag {
  font-size: 0.66rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;
  color: #cddcef; background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.16); padding: 4px 11px; border-radius: 30px;
  white-space: nowrap;
}
#appbar .tag.on { background: rgba(222,146,36,0.16); border-color: rgba(222,146,36,0.5); color: #f2c586; }

/* ── Body: two columns filling remaining height ── */
#body { flex: 1; min-height: 0; padding: 18px 24px; }
#body > .gr-row, #body .gr-row { height: 100%; }

.col-left, .col-right { height: 100%; min-height: 0; }

.panel {
  background: #ffffff; border: 1px solid #d6dfea; border-radius: 13px;
  padding: 15px 17px; display: flex; flex-direction: column; min-height: 0;
}
.eyebrow {
  font-family: 'Space Grotesk', sans-serif; font-size: 0.7rem; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase; color: #3a5a86; margin: 0 0 9px 1px;
  display: flex; align-items: center; gap: 8px;
}
.eyebrow::before {
  content: ""; width: 6px; height: 6px; border-radius: 50%; background: #de9224; display: inline-block;
}

/* image + question inputs */
#img-in { border-radius: 9px !important; overflow: hidden; }
#img-in, #img-in > div { border: 1px dashed #c2cfdf !important; }
#q-in textarea {
  border-radius: 9px !important; border: 1px solid #d6dfea !important;
  font-size: 0.92rem !important; background: #fbfcfe !important; color: #12203a !important;
}

#run-btn {
  background: #1c2f52 !important; color: #fff !important;
  font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
  font-size: 0.98rem !important; letter-spacing: 0.02em;
  border: none !important; border-radius: 10px !important; padding: 13px !important;
  transition: background .15s ease !important;
}
#run-btn:hover { background: #0b1220 !important; }

.hint { font-size: 0.76rem; color: #6a80a1; line-height: 1.45; margin: 10px 1px 0 1px; }

/* ── Assessment output ── */
#answer-box {
  flex: 1; min-height: 0; overflow-y: auto;
  background: #f6f8fb; border: 1px solid #dbe3ee; border-left: 3px solid #1c2f52;
  border-radius: 10px; padding: 15px 19px; line-height: 1.58; color: #101f38; font-size: 0.92rem;
}
#answer-box::-webkit-scrollbar { width: 9px; }
#answer-box::-webkit-scrollbar-thumb { background: #c2cfdf; border-radius: 6px; }
#answer-box h1, #answer-box h2, #answer-box h3 { color: #1c2f52; font-size: 1.0rem; margin: .5em 0 .3em; }
#answer-box strong { color: #16294a; }
#answer-box.placeholder { display: flex; align-items: center; justify-content: center;
  color: #8296b3; font-style: italic; }

/* ── Trace ── */
#trace-box { border: none !important; background: transparent !important; box-shadow: none !important; }
#trace-box textarea {
  background: #0b1220 !important; color: #93b7d8 !important;
  font-family: 'JetBrains Mono', ui-monospace, monospace !important;
  font-size: 0.75rem !important; line-height: 1.85 !important;
  border: none !important; border-radius: 10px !important; padding: 13px 15px !important;
}

/* ── Examples strip ── */
#ex-wrap { margin-top: 11px; }
#ex-wrap .eyebrow { margin-bottom: 7px; }
#ex-wrap table { font-size: 0.82rem !important; }
#ex-wrap button, #ex-wrap td {
  background: #fbfcfe !important; border-color: #e3e9f1 !important; color: #23364f !important;
}

/* mobile fallback: allow scroll on small screens */
@media (max-width: 900px) {
  html, body, .gradio-container, #shell { height: auto !important; overflow: auto !important; }
  #appbar { flex-direction: column; align-items: flex-start; gap: 10px; }
}
"""

APPBAR = """
<div id="appbar">
  <div class="brand">
    <span class="mark">Structural&nbsp;Inspection&nbsp;<span class="amber">Intelligence</span></span>
    <span class="doc">EM 1110-2-2002 · USACE</span>
  </div>
  <div class="tags">
    <span class="tag on">§ clause-cited</span>
    <span class="tag">YOLOv8s detector</span>
    <span class="tag">LangGraph agent</span>
    <span class="tag">Refuses when unsupported</span>
  </div>
</div>
"""

INTRO = ("Upload an inspection photo and ask a question. A reasoning agent runs a fine-tuned "
         "defect detector, retrieves the governing clauses from the USACE concrete repair "
         "manual, and returns a cited field assessment — or declines when the manual is silent.")

PLACEHOLDER = "Awaiting inspection. Choose an example or ask a question."


def run_agent(image, question):
    if not question or not question.strip():
        yield "Enter a question, or pick an example below to begin.", ""
        return

    state = {
        "question": question, "queries": [question],
        "image_path": image if image else "", "defect_findings": {},
        "retrieved": [], "relevant": [], "rewrite_count": 0, "answer": "",
    }
    trace, answer = [], ""
    try:
        for step in app_graph.stream(state):
            for node, update in step.items():
                if node == "analyze_image":
                    f = update["defect_findings"]
                    dets = ", ".join(f"{d['defect_type']}·{d['severity']}"
                                     for d in f.get("findings", [])) or "none"
                    trace.append(f"▸ Vision analysis — {f.get('defects_found', 0)} defect(s): {dets}")
                elif node == "plan_queries":
                    n = len(update["queries"])
                    trace.append(f"▸ Query planning — {n} search quer{'y' if n == 1 else 'ies'}")
                elif node == "retrieve":
                    trace.append(f"▸ Retrieval — {len(update['retrieved'])} candidate chunks")
                elif node == "grade":
                    trace.append(f"▸ Relevance grading — {len(update['relevant'])} judged relevant")
                elif node == "rewrite":
                    trace.append(f"▸ Query rewrite — retrying: {', '.join(update['queries'])}")
                elif node == "generate":
                    answer = update["answer"]
                    trace.append("▸ Answer generation — complete")
            yield (answer or "_Analyzing…_"), "\n".join(trace)
    except Exception as e:
        msg = str(e)
        if "rate_limit" in msg.lower() or "429" in msg:
            yield ("**Free-tier quota reached.** This demo runs on free LLM tiers with a daily "
                   "limit. Please try again in a few minutes."), "\n".join(trace)
        else:
            yield f"**Something went wrong.** {msg[:300]}", "\n".join(trace)


with gr.Blocks(css=CSS, theme=gr.themes.Base(), title="Structural Inspection Intelligence") as demo:
    gr.HTML('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&'
            'family=Space+Grotesk:wght@500;600&family=JetBrains+Mono&display=swap" rel="stylesheet">')

    with gr.Column(elem_id="shell"):
        gr.HTML(APPBAR)

        with gr.Row(elem_id="body", equal_height=True):
            # ── Left column: inputs ──
            with gr.Column(scale=4, elem_classes="col-left"):
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<p class="eyebrow">Inspection photo — optional</p>')
                    image_in = gr.Image(type="filepath", show_label=False,
                                        height=232, elem_id="img-in")
                    gr.HTML('<p class="eyebrow" style="margin-top:13px">Question</p>')
                    question_in = gr.Textbox(
                        show_label=False, lines=2, elem_id="q-in",
                        placeholder="e.g. What repair methods does the manual recommend for the "
                                    "defects in this image?")
                    btn = gr.Button("Run inspection", elem_id="run-btn")
                    gr.HTML(f'<p class="hint">{INTRO}</p>')

            # ── Right column: assessment + trace ──
            with gr.Column(scale=6, elem_classes="col-right"):
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<p class="eyebrow">Field assessment</p>')
                    answer_out = gr.Markdown(PLACEHOLDER, elem_id="answer-box",
                                             elem_classes="placeholder")
                    gr.HTML('<p class="eyebrow" style="margin-top:13px">Agent reasoning trace</p>')
                    trace_out = gr.Textbox(show_label=False, lines=5, max_lines=5,
                                           elem_id="trace-box", interactive=False)

                with gr.Column(elem_id="ex-wrap"):
                    gr.HTML('<p class="eyebrow">Examples — including one the system will refuse</p>')
                    gr.Examples(
                        examples=[
                            [None, "What repair methods are suitable for dormant cracks?"],
                            ["data/test_images/crack_0548.jpg",
                             "What repair methods does the manual recommend for the defects in this image?"],
                            ["data/test_images/corrosion_0184.jpg",
                             "What does this image show and what does the manual say about repairing it?"],
                            ["data/test_images/spalling_0372.jpg",
                             "What could have caused the defect shown in this image?"],
                            [None, "What is the airspeed velocity of an unladen swallow?"],
                        ],
                        inputs=[image_in, question_in],
                    )

    btn.click(run_agent, inputs=[image_in, question_in], outputs=[answer_out, trace_out])

demo.launch()