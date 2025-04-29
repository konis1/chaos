import os
import json
import requests
import time
from typing import List
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth
from app.config import settings


class Ticket(BaseModel):
    id: int
    subject: str
    description: str | None = None
    descrtiption_text: str | None = None


class SimpleTicket(BaseModel):
    id: int
    subject: str
    initial_text: str


class Conversation(BaseModel):
    body_text: str


class FreshDeskClient:
    def __init__(self, domain: str, api_key: str):
        self.base_url = f"https://{domain}.freshdesk.com/api/v2"
        self.auth = HTTPBasicAuth(api_key, "X")

    def fetch_tickets(self, limit=100) -> List[Ticket]:
        url = f"{self.base_url}/tickets"
        params = {"per_page": limit, "order_type": "desc"}
        response = requests.get(url, auth=self.auth, params=params)
        response.raise_for_status()
        tickets = response.json()
        return [Ticket(**t) for t in tickets]

    def fetch_conversations(self, ticket_id: int) -> List[Conversation]:
        url = f"{self.base_url}/tickets/{ticket_id}/conversations"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        convos = response.json()
        return [Conversation(**c) for c in convos if "body_text" in c]

    def simplify_ticket(self, ticket: Ticket) -> SimpleTicket:
        initial = ticket.descrtiption_text or ticket.description

        if not initial:
            conversations = self.fetch_conversations(ticket.id)
            if conversations:
                initial = conversations[0].body_text
            else:
                initial = ""
        return SimpleTicket(id=ticket.id, subject=ticket.subject, initial_text=initial)


def save_simple_ticket_to_file(tickets: List[SimpleTicket], output_path: str):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump([t.dict() for t in tickets], f, indent=2, ensure_ascii=False)
        print(f"✅ {len(tickets)} tickets sauvegardés dans : {output_path}")
    except PermissionError:
        print(f"❌ Permission refusée : impossible d'écrire dans {output_path}")

    except FileNotFoundError:
        print(f"❌ Chemin invalide : {output_path}")

    except Exception as e:
        print(f"❌ Erreur inattendue lors de la sauvegarde : {e}")


def run_freshdesk_pipeline():
    client = FreshDeskClient(domain=settings.freshdesk_domain, api_key=settings.freshdesk_api_key)
    raw_tickets = client.fetch_tickets(limit=50)
    simple_tickets = []
    for t in raw_tickets:
        ticket = client.simplify_ticket(t)
        simple_tickets.append(ticket)
        time.sleep(1.6)
    save_simple_ticket_to_file(simple_tickets, "outputs/freshdesk/raw_tickets.json")


if __name__ == "__main__":
    run_freshdesk_pipeline()
