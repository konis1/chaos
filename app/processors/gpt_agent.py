import openai
from ..config import settings

openai.api_key = settings.openai_api_key


def summarize_tickets(text_block: str, model: str = settings.gpt_model) -> str:
    prompt = (
        "Voici un ensemble de demandes clients issues d'un service de support :\n"
        f"{text_block}\n\n"
        "1. Résume les problèmes récurrents.\n"
        "2. Dégage les besoins implicites des utilisateurs.\n"
        "3. Priorise les tâches à faire en fonction des besoins utilisateurs\n"
        "Réponds en français."
    )

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
