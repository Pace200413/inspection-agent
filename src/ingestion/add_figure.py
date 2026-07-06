import json, sys
from pathlib import Path

# Usage: python src/ingestion/add_figure.py em2002_fig4-4 "4-7" "Figure 4-4: Selection of repair method for dormant cracks" transcript.txt

chunk_id, section, title, transcript_file = sys.argv[1:5]
text = Path(transcript_file).read_text()

chunks = json.load(open("data/chunks.json"))
if any(c["id"] == chunk_id for c in chunks):
    sys.exit(f"Chunk {chunk_id} already exists - aborting.")

chunks.append({
    "id": chunk_id,
    "text": f"[EM 1110-2-2002 §{section} {title}]\n{text}",
    "meta": {"doc": "EM 1110-2-2002", "chapter": section.split("-")[0],
             "section": section, "section_title": title},
})
json.dump(chunks, open("data/chunks.json", "w"), indent=2)
print(f"Added {chunk_id}. Total chunks: {len(chunks)}")