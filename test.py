import re
import pytest
import time
import config
import random
from pages.player_profile import Profile
from playwright.sync_api import Playwright, sync_playwright, expect
from methods import CustomMethods
from pages.welcomePage import WelcomePage
from evpn import ExpressVpnApi




# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://tombriches.com/")
#     page.get_by_role("button", name="ok").click()
#     page.get_by_role("button", name="Log in").click()
#     page.get_by_placeholder("E-Mail").click()
#     page.get_by_placeholder("E-Mail").fill("")
#     page.get_by_placeholder("E-Mail").click()
#     page.get_by_placeholder("E-Mail").fill("samoilenkofluttershy@gmail.com")
#     page.locator(".flex > div > .relative").first.click()
#     page.locator(".flex > div > .relative").first.click()
#     page.get_by_placeholder("Password").fill("193786Az()")
#
#     page.get_by_role("button", name="Account").click()
#     page.get_by_label("Wallet").click()
#     page.locator("div").filter(has_text=re.compile(r"^Deposit$")).click()
#     page.locator("div").filter(has_text=re.compile(r"^Funds withdrawal$")).click()
#
#     # ---------------------
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)


@pytest.mark.parametrize("account_key", config.accounts.keys())
def test(playwright: Playwright, account_key: str) -> None:

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    custom_methods = CustomMethods(page)
    email = config.accounts[account_key]['username']
    password = config.accounts[account_key]['password']


    with ExpressVpnApi() as api:
        locations = api.locations  # get available locations
        loc = next((location for location in locations if location["country_code"] == "IE"), None)
        api.connect(loc["id"])

    custom_methods.base_login(email, password)
    custom_methods.check_to_be_visible(WelcomePage.pop_up)
    page.reload()
    custom_methods.check_to_be_visible(WelcomePage.deposit_button)
    custom_methods.visit_page(config.wallet_url_deposit)

    if page.locator(WelcomePage.wrapper).is_visible():
        page.reload()
    else:
        pass

    custom_methods.check_to_be_visible(Profile.profile_elements['deposit_promo_code'])
    time.sleep(10)

    if page.locator(WelcomePage.wrapper).is_visible():
        page.reload()
    else:
        pass

    time.sleep(10)
    custom_methods.capture_screenshot(account_key, 'Deposit')
    custom_methods.visit_page(config.wallet_url_withdrawal)
    custom_methods.check_to_be_visible(Profile.profile_elements['send_withdrawal_btn'])
    time.sleep(10)
    custom_methods.capture_screenshot(account_key, 'Withdrawal')



# with sync_playwright() as playwright:
#     test(playwright)

