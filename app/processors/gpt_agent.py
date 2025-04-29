import openai
from app.config import settings

openai.api_key = settings.openai_api_key


def summarize_tickets(tickets_text: str, model: str = settings.gpt_model) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": f"Voici des demandes clients: \n\n{tickets_text}\n\n Résume les besoins, problèmes fréquents et idées d'amélioration."}
        ]
    )
    return response.choice[0].message.content.strip()
