"""Regressões sem navegador: dependências do cadastro devem falhar cedo."""

import unittest
from pathlib import Path
from unittest.mock import Mock

from data.registration import Registration
from pages.register_page import RegisterPage, SiteDependencyError


class TestRegistrationDependencies(unittest.TestCase):
    def setUp(self):
        self.data = Registration()
        self.photo = Path("avatar-sintetico.png")
        self.page = object.__new__(RegisterPage)
        self.page.dependency_status = Mock(return_value={
            "countries": [self.data.country],
            "skills": [self.data.skill],
            "years": [self.data.year],
        })
        self.operations = (
            "fill_identity",
            "set_hobbies",
            "set_birth_date",
            "set_passwords",
            "upload_photo",
            "select_secondary_country",
            "select_languages",
        )
        for operation in self.operations:
            setattr(self.page, operation, Mock())
        self.page.skill = Mock()
        self.page.country = Mock()

    def test_opcoes_obrigatorias_inexistentes_falham_sem_preenchimento(self):
        for missing in ("countries", "skills", "years"):
            with self.subTest(missing=missing):
                for operation in self.operations:
                    getattr(self.page, operation).reset_mock()
                current = self.page.dependency_status.return_value
                self.page.dependency_status.return_value = {
                    key: ([] if key == missing else values)
                    for key, values in current.items()
                }

                with self.assertRaisesRegex(SiteDependencyError, missing):
                    self.page.fill_complete(self.data, self.photo)

                for operation in self.operations:
                    getattr(self.page, operation).assert_not_called()
                self.page.country.select_option.assert_not_called()
                self.page.skill.select_option.assert_not_called()
                self.page.dependency_status.return_value = {
                    "countries": [self.data.country],
                    "skills": [self.data.skill],
                    "years": [self.data.year],
                }

    def test_opcoes_disponiveis_permite_preenchimento_normal(self):
        self.page.fill_complete(self.data, self.photo)

        self.page.fill_identity.assert_called_once_with(self.data)
        self.page.upload_photo.assert_called_once_with(self.photo)
        self.page.country.select_option.assert_called_once_with(
            label=self.data.country
        )
        self.page.skill.select_option.assert_called_once_with(
            label=self.data.skill
        )


if __name__ == "__main__":
    unittest.main()
