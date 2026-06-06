"""
Frontend smoke tests — load every page in a real (system Chrome) browser and
assert there are no uncaught JS errors, and that switching language actually
localizes the page. Catches the things `node --check` can't.

Opt-in (needs a browser + a model-loading app start), so it does not slow the
unit suite:

    EDGE_SMOKE=1 pytest tests/test_frontend_smoke.py
"""
import os
import socket
import threading

import pytest

if not os.getenv("EDGE_SMOKE"):
    pytest.skip("set EDGE_SMOKE=1 to run browser smoke tests", allow_module_level=True)

sync_api = pytest.importorskip("playwright.sync_api")
from werkzeug.serving import make_server  # noqa: E402

ROUTES = ["/", "/chat", "/quiz", "/flashcard", "/slides", "/podcast", "/progress"]


def _free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="module")
def base_url():
    from app import app as flask_app
    port = _free_port()
    srv = make_server("127.0.0.1", port, flask_app)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{port}"
    srv.shutdown()


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="chrome", headless=True)
        except Exception as exc:                       # no system Chrome
            pytest.skip(f"system Chrome not available: {exc}")
        yield b
        b.close()


def _new_page(browser, lang=None):
    ctx = browser.new_context()
    init = "localStorage.setItem('edge_onboarded','1');"
    if lang:
        init += f"localStorage.setItem('edu_lang',{lang!r});"
    ctx.add_init_script(init)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    return page, errors


@pytest.mark.parametrize("route", ROUTES)
def test_page_loads_without_js_errors(browser, base_url, route):
    page, errors = _new_page(browser)
    page.goto(base_url + route, wait_until="load")
    page.wait_for_selector("nav.nav", timeout=5000)     # shell rendered
    assert errors == [], f"JS errors on {route}: {errors}"


def test_slides_localizes_to_filipino(browser, base_url):
    page, _ = _new_page(browser, lang="Filipino")
    page.goto(base_url + "/slides", wait_until="load")
    assert page.inner_text('[data-i18n="slides.title"]').strip() == "Mga Slide ng Aralin!"
    assert "Mga Slide" in page.inner_text('[data-i18n="nav.slides"]')


def test_quiz_localizes_to_filipino(browser, base_url):
    page, _ = _new_page(browser, lang="Filipino")
    page.goto(base_url + "/quiz", wait_until="load")
    assert page.inner_text('[data-i18n="quiz.title"]').strip() == "Hamon sa Quiz!"


def test_chat_restores_saved_diagram_on_reload(browser, base_url):
    # A bot bubble with a saved diagram spec must re-render its SVG on load.
    import json
    history = [{"who": "bot", "text": "Here is a number line.",
                "diagram": json.dumps({"type": "number_line", "min": 0, "max": 10, "step": 1,
                                       "points": [{"value": 7, "label": "7"}]})}]
    ctx = browser.new_context()
    ctx.add_init_script(
        "localStorage.setItem('edge_onboarded','1');"
        "localStorage.setItem('edu_chat__guest'," + repr(json.dumps(history)) + ");"
    )
    page = ctx.new_page()
    page.goto(base_url + "/chat", wait_until="load")
    page.wait_for_selector(".math-diagram svg", timeout=5000)   # diagram came back
    assert page.locator(".math-diagram svg").count() == 1


def test_language_switch_updates_live(browser, base_url):
    # Change the dropdown and confirm the hero re-localizes without a reload.
    page, _ = _new_page(browser)
    page.goto(base_url + "/slides", wait_until="load")
    assert page.inner_text('[data-i18n="slides.title"]').strip() == "Lesson Slides!"
    page.select_option("#langSel", "Bahasa Melayu")
    assert page.inner_text('[data-i18n="slides.title"]').strip() == "Slaid Pelajaran!"
