import sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agent.graph import build_graph

RESULTS = "eval/results/run_full.json"
dataset = {d["id"]: d for d in json.load(open("data/eval/qa_dataset.json"))}
results = json.load(open(RESULTS))
app = build_graph()

for i, r in enumerate(results):
    if not r.get("error"):
        continue
    item = dataset[r["id"]]
    state = {"question": item["question"], "queries": [item["question"]],
             "image_path": item.get("image_path", ""), "defect_findings": {},
             "retrieved": [], "relevant": [], "rewrite_count": 0, "answer": ""}
    t0 = time.time()
    try:
        final = app.invoke(state)
        results[i] = {"id": item["id"], "type": item["type"], "question": item["question"],
                      "answer": final["answer"],
                      "kept_sections": sorted({c["meta"]["section"] for c in final["relevant"]}),
                      "kept_ids": [c["id"] for c in final["relevant"]],
                      "rewrites": final["rewrite_count"],
                      "latency_s": round(time.time() - t0, 1), "error": None}
        print(f"[{item['id']}] fixed ({results[i]['latency_s']}s)")
    except Exception as e:
        print(f"[{item['id']}] still failing: {e}")
    time.sleep(10)

json.dump(results, open(RESULTS, "w"), indent=2)
print("Merged back into", RESULTS)