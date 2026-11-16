"""Navegador isolado por teste e evidências mesmo quando o cenário falha."""

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from playwright.sync_api import Error as PlaywrightError

from pages.register_page import RegisterPage


def pytest_configure(config):
    stamp = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y%m%d-%H%M%S")
    config.evidence_root = Path("evidencias/execucoes") / stamp


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1440, "height": 1100}}


@pytest.fixture(autouse=True)
def evidence(page, request):
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", request.node.name)
    folder = request.config.evidence_root / name
    folder.mkdir(parents=True, exist_ok=True)
    steps = []

    def capture(label):
        filename = f"{len(steps) + 1:02d}-{label}.png"
        page.screenshot(
            path=folder / filename,
            full_page=True,
            mask=[page.locator('input[type="password"]')],
        )
        steps.append(filename)

    yield capture
    report = getattr(request.node, "rep_call", None)
    setup = getattr(request.node, "rep_setup", None)
    error = None
    try:
        capture("resultado")
    except (PlaywrightError, OSError) as exc:
        error = str(exc)
    selected = report or setup
    result = {
        "scenario": request.node.nodeid,
        "outcome": selected.outcome if selected else "error",
        "url": page.url,
        "screenshots": steps,
        "screenshot_error": error,
        "details": str(selected.longrepr) if selected and selected.longrepr else None,
    }
    (folder / "resultado.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )


@pytest.fixture
def registration_page(page):
    return RegisterPage(page).open()


@pytest.fixture
def photo():
    return Path(__file__).parent / "data" / "avatar.png"
