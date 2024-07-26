import pytest
import time
import config
from pages.player_profile import Profile
from playwright.sync_api import Playwright
from methods import CustomMethods
from pages.welcomePage import WelcomePage
from evpn import ExpressVpnApi

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
        loc = next((location for location in locations if location["country_code"] == account_key), None)
        api.connect(loc["id"])

    custom_methods.base_login(email, password)

    time.sleep(10)

    if page.locator(WelcomePage.wrapper).is_visible():
        page.reload()
    else:
        pass

    time.sleep(10)
    if page.locator(WelcomePage.pop_up).is_visible():
        page.reload()
    else:
        pass

    time.sleep(10)
    if page.locator(WelcomePage.wrapper).is_visible():
        page.reload()
    else:
        pass

    custom_methods.check_to_be_visible(WelcomePage.deposit_button)
    custom_methods.visit_page(config.wallet_url_deposit)


    custom_methods.check_to_be_visible(Profile.profile_elements['deposit_promo_code'])
    time.sleep(10)

    time.sleep(10)

    custom_methods.capture_screenshot(account_key, 'Deposit', 'Deposit', account_key)

    custom_methods.visit_page(config.wallet_url_withdrawal)
    custom_methods.check_to_be_visible(Profile.profile_elements['send_withdrawal_btn'])
    time.sleep(10)

    custom_methods.capture_screenshot(account_key, 'Withdrawal', 'Withdrawal', account_key)

    browser.close()

