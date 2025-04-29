import json
from app.processors.gpt_agent import summarize_tickets

with open("data/raw/freshdesk_tickets.json") as f:
    tickets = json.load(f)

texts = "\n\n".join([t["initial_text"] for t in tickets[:10]])  # chunk simple

summary = summarize_tickets(texts)

with open("data/raw/freshdesk_summary.md", "w") as f:
    f.write(summary)

print("Résumé généré dans freshdesk_summary.md")
