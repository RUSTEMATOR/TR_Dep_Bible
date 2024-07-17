import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://tombriches.com/")
    page.goto("https://tombriches.com/de")
    page.get_by_role("button", name="ok").click()
    page.get_by_role("button", name="Einloggen").click()
    page.get_by_placeholder("E-Mail").click()
    page.get_by_placeholder("E-Mail").fill("")
    page.get_by_placeholder("E-Mail").click()
    page.get_by_placeholder("E-Mail").fill("samoilenkofluttershy@gmail.com")
    page.locator(".flex > div > .relative").first.click()
    page.locator(".flex > div > .relative").first.click()
    page.get_by_placeholder("Passwort").fill("193786Az()")
    page.locator("div").filter(has_text=re.compile(r"^EinloggenPasswort vergessen\?\?$")).get_by_role("button").click()
    page.locator(".cursor-pointer").first.click()
    page.locator(".cursor-pointer").first.click()
    page.locator(".cursor-pointer").first.click()
    page.get_by_role("button", name="deposit").click()
    page.locator(".cursor-pointer").first.click()
    page.get_by_role("button", name="Account").click()
    page.get_by_label("Wallet").click()
    page.locator("div").filter(has_text=re.compile(r"^Deposit$")).click()
    page.locator("div").filter(has_text=re.compile(r"^Funds withdrawal$")).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

@pytest.mark.parametrize