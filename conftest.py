"""Navegador isolado por teste e evidências mesmo quando o cenário falha."""

import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from playwright.sync_api import Error as PlaywrightError

from pages.register_page import RegisterPage

LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")
EVIDENCE_ROOT = Path("evidencias/execucoes")
VIEWPORT = {"width": 1440, "height": 1100}
PHOTO_PATH = Path(__file__).parent / "data" / "avatar.png"


def pytest_configure(config):
    stamp = datetime.now(LOCAL_TIMEZONE).strftime("%Y%m%d-%H%M%S")
    config.evidence_root = EVIDENCE_ROOT / stamp


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": VIEWPORT}


def _evidence_folder(request) -> Path:
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", request.node.name)
    folder = request.config.evidence_root / name
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _final_report(node):
    """Relatório da execução; cai para o setup quando o teste nem chegou a rodar."""
    return getattr(node, "rep_call", None) or getattr(node, "rep_setup", None)


def _write_result(folder: Path, request, page, steps, screenshot_error) -> None:
    report = _final_report(request.node)
    result = {
        "scenario": request.node.nodeid,
        "outcome": report.outcome if report else "error",
        "url": page.url,
        "screenshots": steps,
        "screenshot_error": screenshot_error,
        "details": str(report.longrepr) if report and report.longrepr else None,
    }
    (folder / "resultado.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )


@pytest.fixture(autouse=True)
def evidence(page, request):
    folder = _evidence_folder(request)
    steps: list[str] = []

    def capture(label: str) -> None:
        filename = f"{len(steps) + 1:02d}-{label}.png"
        page.screenshot(
            path=folder / filename,
            full_page=True,
            mask=[page.locator('input[type="password"]')],
        )
        steps.append(filename)

    yield capture

    screenshot_error = None
    try:
        capture("resultado")
    except (PlaywrightError, OSError) as exc:
        screenshot_error = str(exc)
    _write_result(folder, request, page, steps, screenshot_error)


@pytest.fixture
def registration_page(page):
    return RegisterPage(page).open()


@pytest.fixture
def photo():
    return PHOTO_PATH
