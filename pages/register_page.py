"""Interações e seletores do formulário. As expectativas ficam nos testes."""

import os
import re
from pathlib import Path

from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from data.registration import Registration


class SiteDependencyError(RuntimeError):
    """O site não disponibilizou uma dependência necessária ao cadastro."""


class RegisterPage:
    URL = "https://demo.automationtesting.in/Register.html"

    def __init__(self, page: Page):
        self.page = page
        self.form = page.locator("#basicBootstrapForm")
        self.first_name = page.get_by_placeholder("First Name", exact=True)
        self.last_name = page.get_by_placeholder("Last Name", exact=True)
        self.address = self.form.locator("textarea")
        self.email = self.form.locator('input[type="email"]')
        self.phone = self.form.locator('input[type="tel"]')
        self.password = page.locator("#firstpassword")
        self.confirm_password = page.locator("#secondpassword")
        self.country = page.locator("#countries")
        self.skill = page.locator("#Skills")
        self.year = page.locator("#yearbox")
        self.month = page.locator('select[ng-model="monthbox"]')
        self.day = page.locator("#daybox")
        self.photo = page.locator("#imagesrc")

    def open(self):
        response = self.page.goto(
            os.getenv("REGISTER_URL", self.URL),
            wait_until="domcontentloaded",
            timeout=60000,
        )
        if response and response.status >= 400:
            raise SiteDependencyError(f"Página respondeu HTTP {response.status}")
        expect(self.first_name).to_be_visible()
        return self

    def fill_identity(self, data: Registration):
        self.first_name.fill(data.first_name)
        self.last_name.fill(data.last_name)
        self.address.fill(data.address)
        self.email.fill(data.email)
        self.phone.fill(data.phone)
        self.form.locator(f'input[type="radio"][value="{data.gender}"]').check()

    def set_hobbies(self, selected: tuple[str, ...]):
        for hobby in ("Cricket", "Movies", "Hockey"):
            self.form.locator(f'input[type="checkbox"][value="{hobby}"]').set_checked(
                hobby in selected
            )

    def select_languages(self, languages: tuple[str, ...]):
        links = self.page.locator("a.ui-corner-all")
        try:
            links.first.wait_for(state="attached", timeout=10000)
            self.page.locator("#msdd").click()
            expect(links.first).to_be_visible(timeout=10000)
        except (AssertionError, PlaywrightTimeoutError) as exc:
            raise SiteDependencyError("Lista de idiomas indisponível no site") from exc
        for language in languages:
            links.filter(has_text=re.compile(f"^{re.escape(language)}$")).click()
        self.page.get_by_role("heading", name="Register", exact=True).click()

    def set_passwords(self, password: str, confirmation: str):
        self.password.fill(password)
        self.password.press("Tab")
        self.confirm_password.fill(confirmation)
        self.confirm_password.press("Tab")

    def upload_photo(self, path: Path):
        self.photo.set_input_files(path)

    def select_secondary_country(self, country: str):
        self.page.locator(".select2-selection").click()
        self.page.locator("input.select2-search__field").fill(country)
        self.page.get_by_role("treeitem", name=country, exact=True).click()

    def set_birth_date(self, year: str, month: str, day: str):
        self.year.select_option(year)
        self.month.select_option(label=month)
        self.day.select_option(day)

    def dependency_status(self) -> dict:
        return {
            name: locator.locator("option").evaluate_all(
                "options => options.map(o => o.value).filter(Boolean)"
            )
            for name, locator in {
                "countries": self.country,
                "skills": self.skill,
                "years": self.year,
            }.items()
        }

    def fill_complete(self, data: Registration, photo: Path):
        # Verifique dependências obrigatórias antes de modificar o formulário.
        # O site pode apresentar uma lista Country vazia, que impede o envio.
        dependencies = self.dependency_status()
        for name, value in (
            ("countries", data.country),
            ("skills", data.skill),
            ("years", data.year),
        ):
            if value not in dependencies[name]:
                raise SiteDependencyError(
                    f"Opção {value!r} indisponível em {name}: {dependencies[name]}"
                )

        self.fill_identity(data)
        self.set_hobbies(data.hobbies)
        self.set_birth_date(data.year, data.month, data.day)
        self.set_passwords(data.password, data.password)
        self.upload_photo(photo)
        self.select_secondary_country(data.country)
        self.select_languages(data.languages)
        self.skill.select_option(label=data.skill)
        self.country.select_option(label=data.country)

    def invalid_fields(self) -> list[dict]:
        return self.form.locator("input:invalid, select:invalid").evaluate_all(
            "els => els.map(e => ({field: e.id || e.placeholder || e.type, "
            "message: e.validationMessage}))"
        )

    def submit(self):
        self.page.locator("#submitbtn").click()

    def refresh(self):
        self.page.locator("#Button1").click()
        expect(self.first_name).to_have_value("")
