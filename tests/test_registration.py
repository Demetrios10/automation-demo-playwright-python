"""Cenários reais, sem alterar o DOM nem simular respostas de sucesso."""

import re

import pytest
from playwright.sync_api import expect

from data.registration import Registration


def test_formulario_disponivel(registration_page):
    expect(registration_page.first_name).to_be_visible()
    expect(registration_page.page.locator("#submitbtn")).to_be_visible()


def test_dados_pessoais(registration_page, evidence):
    data = Registration()
    registration_page.fill_identity(data)
    expect(registration_page.first_name).to_have_value(data.first_name)
    expect(registration_page.last_name).to_have_value(data.last_name)
    expect(registration_page.address).to_have_value(data.address)
    expect(registration_page.email).to_have_value(data.email)
    expect(registration_page.phone).to_have_value(data.phone)
    expect(registration_page.form.locator('input[value="Male"]')).to_be_checked()
    evidence("dados-pessoais")


@pytest.mark.parametrize("gender", ["Male", "FeMale"])
def test_genero_exclusivo(registration_page, gender):
    form = registration_page.form
    form.locator(f'input[type="radio"][value="{gender}"]').check()
    expect(form.locator('input[type="radio"]:checked')).to_have_count(1)
    expect(form.locator(f'input[value="{gender}"]')).to_be_checked()


def test_hobbies_multiplos_e_desmarcacao(registration_page):
    registration_page.set_hobbies(("Movies", "Hockey"))
    expect(registration_page.page.locator("#checkbox2")).to_be_checked()
    expect(registration_page.page.locator("#checkbox3")).to_be_checked()
    registration_page.set_hobbies(("Cricket",))
    expect(registration_page.page.locator("#checkbox1")).to_be_checked()
    expect(registration_page.page.locator("#checkbox2")).not_to_be_checked()
    expect(registration_page.page.locator("#checkbox3")).not_to_be_checked()


@pytest.mark.parametrize("value", ["invalido", "qa@", "qa example.com"])
def test_email_invalido(registration_page, value):
    registration_page.email.fill(value)
    assert registration_page.email.evaluate("e => e.validity.typeMismatch")


@pytest.mark.parametrize("value", ["123", "11987654321", "abcdefghij"])
def test_telefone_invalido(registration_page, value):
    registration_page.phone.fill(value)
    assert registration_page.phone.evaluate("e => e.validity.patternMismatch")


def test_campos_obrigatorios(registration_page):
    registration_page.submit()
    assert registration_page.first_name.evaluate("e => e.validity.valueMissing")
    expect(registration_page.page).to_have_url(re.compile(r"Register\.html"))
    assert len(registration_page.invalid_fields()) >= 6


def test_confirmacao_de_senha_divergente(registration_page):
    registration_page.set_passwords("DemoQa123!", "Diferente123!")
    assert registration_page.confirm_password.evaluate("e => e.validity.customError")
    expect(registration_page.confirm_password).to_have_js_property(
        "validationMessage", "Passwords dont match"
    )


def test_senha_sem_complexidade(registration_page):
    registration_page.set_passwords("apenasletras", "apenasletras")
    assert registration_page.password.evaluate("e => e.validity.customError")


def test_senha_valida(registration_page):
    registration_page.set_passwords("DemoQa123!", "DemoQa123!")
    assert registration_page.password.evaluate("e => e.validity.valid")
    assert registration_page.confirm_password.evaluate("e => e.validity.valid")


def test_upload_foto(registration_page, photo):
    registration_page.upload_photo(photo)
    assert registration_page.photo.evaluate("e => e.files.length") == 1


def test_previa_da_foto(registration_page, photo):
    registration_page.upload_photo(photo)
    expect(registration_page.page.locator("#imagetrgt")).to_have_attribute(
        "src", re.compile(r"^data:image/png;base64,")
    )


def test_data_de_nascimento(registration_page):
    registration_page.set_birth_date("1995", "May", "15")
    expect(registration_page.year).to_have_value("1995")
    expect(registration_page.month).to_have_value("May")
    expect(registration_page.day).to_have_value("15")


def test_pais_com_busca(registration_page):
    registration_page.select_secondary_country("India")
    expect(registration_page.page.locator("#country")).to_have_value("India")


def test_idiomas_multiplos(registration_page):
    registration_page.select_languages(("English", "Portuguese"))
    expect(registration_page.page.locator("#msdd")).to_contain_text("English")
    expect(registration_page.page.locator("#msdd")).to_contain_text("Portuguese")


def test_refresh_limpa_dados(registration_page):
    registration_page.fill_identity(Registration())
    registration_page.set_passwords("DemoQa123!", "DemoQa123!")
    registration_page.refresh()
    expect(registration_page.email).to_have_value("")
    expect(registration_page.password).to_have_value("")


@pytest.mark.complete
def test_cadastro_completo(registration_page, photo, evidence):
    data = Registration()
    registration_page.fill_complete(data, photo)
    expect(registration_page.email).to_have_value(data.email)
    expect(registration_page.country).to_have_value(data.country)
    assert registration_page.invalid_fields() == []
    evidence("cadastro-preenchido")
    registration_page.submit()
    # Só considera sucesso quando a navegação real esperada acontece.
    expect(registration_page.page).to_have_url(
        re.compile(r"WebTable\.html"), timeout=20000
    )
    evidence("apos-envio")
