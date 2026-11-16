"""Dados exclusivamente fictícios para o ambiente de demonstração."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class Registration:
    first_name: str = "Alex"
    last_name: str = "Teste"
    address: str = "Rua Ficticia, 123"
    email: str = field(default_factory=lambda: f"qa.{uuid4().hex[:12]}@example.com")
    phone: str = "1198765432"
    gender: str = "Male"
    hobbies: tuple[str, ...] = ("Movies", "Hockey")
    languages: tuple[str, ...] = ("English", "Portuguese")
    skill: str = "Python"
    country: str = "India"
    year: str = "1995"
    month: str = "May"
    day: str = "15"
    password: str = "DemoQa123!"
