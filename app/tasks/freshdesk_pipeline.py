import json
import requests
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

    def simplify_ticket(self, ticket: Ticket) -> SimpleTicket:
        initial = ticket.descrtiption_text or ticket.description or ""
        return SimpleTicket(id=ticket.id, subject=ticket.subject, initial_text=initial)


def save_simple_ticket_to_file(tickets: List[SimpleTicket], output_path: str):
    with open(output_path, "w") as f:
        json.dump([t.dict() for t in tickets], f, indent=2, ensure_ascii=False)


def run_freshdesk_pipeline():
    client = FreshDeskClient(domain=settings.freshdesk_domain, api_key=settings.freshdesk_api_key)
    raw_tickets = client.fetch_tickets(limit=50)
    simple_tickets = [client.simplify_ticket(t) for t in raw_tickets]
    save_simple_ticket_to_file(simple_tickets, "/data/raw/freshdesk_tickets.json")


if __name__ == "__main__":
    run_freshdesk_pipeline()
