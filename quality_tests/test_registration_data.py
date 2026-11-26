"""Testes de massa sintética sem dependência de browser ou conftest."""

import unittest
from dataclasses import FrozenInstanceError

from data.registration import Registration


class TestRegistrationData(unittest.TestCase):
    def test_email_unico_e_ficticio(self):
        first = Registration()
        second = Registration()
        self.assertNotEqual(first.email, second.email)
        self.assertTrue(first.email.endswith("@example.com"))
        self.assertTrue(second.email.endswith("@example.com"))

    def test_tipos_validos(self):
        record = Registration()
        fields = (
            "first_name",
            "last_name",
            "address",
            "email",
            "phone",
            "gender",
            "skill",
            "country",
            "year",
            "month",
            "day",
            "password",
        )
        for field in fields:
            with self.subTest(field=field):
                value = getattr(record, field)
                self.assertIsInstance(value, str)
                self.assertTrue(value)
        self.assertTrue(all(isinstance(x, str) for x in record.hobbies))
        self.assertTrue(all(isinstance(x, str) for x in record.languages))

    def test_dados_imutaveis(self):
        record = Registration()
        with self.assertRaises(FrozenInstanceError):
            record.first_name = "Alterado"


if __name__ == "__main__":
    unittest.main()
