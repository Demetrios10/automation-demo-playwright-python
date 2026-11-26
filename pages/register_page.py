"""Interações e seletores do formulário. As expectativas ficam nos testes."""

import os
import re
from pathlib import Path

from playwright.sync_api import Locator, Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from data.registration import Registration

NAVIGATION_TIMEOUT_MS = 60_000
LANGUAGE_LIST_TIMEOUT_MS = 10_000
HTTP_ERROR_THRESHOLD = 400
HOBBY_OPTIONS = ("Cricket", "Movies", "Hockey")

OPTION_VALUES_JS = "options => options.map(o => o.value).filter(Boolean)"
INVALID_FIELDS_JS = (
    "els => els.map(e => ({field: e.id || e.placeholder || e.type, "
    "message: e.validationMessage}))"
)


class SiteDependencyError(RuntimeError):
    """O site não disponibilizou uma dependência necessária ao cadastro."""


class RegisterPage:
    URL = "https://demo.automationtesting.in/Register.html"

    def __init__(self, page: Page) -> None:
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
        self.secondary_country = page.locator("#country")
        self.skill = page.locator("#Skills")
        self.year = page.locator("#yearbox")
        self.month = page.locator('select[ng-model="monthbox"]')
        self.day = page.locator("#daybox")
        self.photo = page.locator("#imagesrc")
        self.photo_preview = page.locator("#imagetrgt")
        self.languages = page.locator("#msdd")
        self.submit_button = page.locator("#submitbtn")
        self.refresh_button = page.locator("#Button1")

    # Localizadores parametrizados ------------------------------------------

    def gender_radio(self, gender: str) -> Locator:
        return self.form.locator(f'input[type="radio"][value="{gender}"]')

    def hobby_checkbox(self, hobby: str) -> Locator:
        return self.form.locator(f'input[type="checkbox"][value="{hobby}"]')

    # Ações ------------------------------------------------------------------

    def open(self) -> "RegisterPage":
        response = self.page.goto(
            os.getenv("REGISTER_URL", self.URL),
            wait_until="domcontentloaded",
            timeout=NAVIGATION_TIMEOUT_MS,
        )
        if response and response.status >= HTTP_ERROR_THRESHOLD:
            raise SiteDependencyError(f"Página respondeu HTTP {response.status}")
        expect(self.first_name).to_be_visible()
        return self

    def fill_identity(self, data: Registration) -> None:
        self.first_name.fill(data.first_name)
        self.last_name.fill(data.last_name)
        self.address.fill(data.address)
        self.email.fill(data.email)
        self.phone.fill(data.phone)
        self.gender_radio(data.gender).check()

    def set_hobbies(self, selected: tuple[str, ...]) -> None:
        for hobby in HOBBY_OPTIONS:
            self.hobby_checkbox(hobby).set_checked(hobby in selected)

    def select_languages(self, languages: tuple[str, ...]) -> None:
        options = self._open_language_list()
        for language in languages:
            options.filter(has_text=re.compile(f"^{re.escape(language)}$")).click()
        self.page.get_by_role("heading", name="Register", exact=True).click()

    def set_passwords(self, password: str, confirmation: str) -> None:
        self._fill_and_leave(self.password, password)
        self._fill_and_leave(self.confirm_password, confirmation)

    def upload_photo(self, path: Path) -> None:
        self.photo.set_input_files(path)

    def select_secondary_country(self, country: str) -> None:
        self.page.locator(".select2-selection").click()
        self.page.locator("input.select2-search__field").fill(country)
        self.page.get_by_role("treeitem", name=country, exact=True).click()

    def set_birth_date(self, year: str, month: str, day: str) -> None:
        self.year.select_option(year)
        self.month.select_option(label=month)
        self.day.select_option(day)

    def dependency_status(self) -> dict[str, list[str]]:
        selects = {"countries": self.country, "skills": self.skill, "years": self.year}
        return {
            name: select.locator("option").evaluate_all(OPTION_VALUES_JS)
            for name, select in selects.items()
        }

    def fill_complete(self, data: Registration, photo: Path) -> None:
        # Verifica dependências obrigatórias antes de modificar o formulário:
        # o site pode apresentar uma lista Country vazia, que impede o envio.
        self._ensure_dependencies(data)

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
            INVALID_FIELDS_JS
        )

    def submit(self) -> None:
        self.submit_button.click()

    def refresh(self) -> None:
        self.refresh_button.click()
        expect(self.first_name).to_have_value("")

    # Auxiliares privados ----------------------------------------------------

    def _ensure_dependencies(self, data: Registration) -> None:
        available = self.dependency_status()
        required = {"countries": data.country, "skills": data.skill, "years": data.year}
        for name, value in required.items():
            if value not in available[name]:
                raise SiteDependencyError(
                    f"Opção {value!r} indisponível em {name}: {available[name]}"
                )

    def _open_language_list(self) -> Locator:
        options = self.page.locator("a.ui-corner-all")
        try:
            options.first.wait_for(state="attached", timeout=LANGUAGE_LIST_TIMEOUT_MS)
            self.languages.click()
            expect(options.first).to_be_visible(timeout=LANGUAGE_LIST_TIMEOUT_MS)
        except (AssertionError, PlaywrightTimeoutError) as exc:
            raise SiteDependencyError("Lista de idiomas indisponível no site") from exc
        return options

    @staticmethod
    def _fill_and_leave(field: Locator, value: str) -> None:
        field.fill(value)
        field.press("Tab")
