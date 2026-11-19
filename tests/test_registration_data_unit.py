"""Verificações determinísticas das massas fictícias de cadastro."""

from dataclasses import FrozenInstanceError

import pytest

from data.registration import Registration


def test_cada_cadastro_recebe_email_unico_e_ficticio():
    first = Registration()
    second = Registration()

    assert first.email != second.email
    assert first.email.endswith("@example.com")
    assert second.email.endswith("@example.com")


def test_massa_possui_tipos_esperados():
    record = Registration()
    for field in ("first_name", "last_name", "address", "email", "phone",
                  "gender", "skill", "country", "year", "month", "day", "password"):
        assert isinstance(getattr(record, field), str)
        assert getattr(record, field)
    assert all(isinstance(value, str) for value in record.hobbies)
    assert all(isinstance(value, str) for value in record.languages)


def test_cadastro_e_imutavel():
    record = Registration()
    with pytest.raises(FrozenInstanceError):
        record.first_name = "Alterado"
