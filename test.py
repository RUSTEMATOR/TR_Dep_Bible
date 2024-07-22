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
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from datetime import datetime
import json

# Set up Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def setup_drive_api():
    creds = Credentials.from_authorized_user_file('client_secrets.json', SCOPES)
    return build('drive', 'v3', credentials=creds)

def create_folder(service, folder_name, parent_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')


def upload_file(service, filename, folder_id=None):
    file_metadata = {'name': os.path.basename(filename)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(filename, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    return file.get('id'), file.get('webViewLink')


@pytest.mark.parametrize("account_key", config.accounts.keys())
def test(playwright: Playwright, account_key: str) -> None:

    # Set up Google Drive API
    drive_service = setup_drive_api()

    # Create a folder for today's date
    today_folder_name = datetime.now().strftime("%Y-%m-%d")
    today_folder_id = create_folder(drive_service, today_folder_name)


    # Create a subfolder for this test run
    test_folder_name = f"Test_{account_key}_{datetime.now().strftime('%H-%M-%S')}"
    test_folder_id = create_folder(drive_service, test_folder_name, today_folder_id)

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    custom_methods = CustomMethods(page)
    email = config.accounts[account_key]['username']
    password = config.accounts[account_key]['password']

    screenshot_links = {}




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

    screenshot_path = custom_methods.capture_screenshot(account_key, 'Deposit')
    file_id, web_view_link = upload_file(drive_service, screenshot_path, test_folder_id)
    print(f"Deposit screenshot uploaded. File ID: {file_id}, Web View Link: {web_view_link}")
    screenshot_links[f'{account_key} ''Deposit'] = web_view_link

    custom_methods.visit_page(config.wallet_url_withdrawal)
    custom_methods.check_to_be_visible(Profile.profile_elements['send_withdrawal_btn'])
    time.sleep(10)

    screenshot_path = custom_methods.capture_screenshot(account_key, 'Withdrawal')
    file_id, web_view_link = upload_file(drive_service, screenshot_path, test_folder_id)
    print(f"Withdrawal screenshot uploaded. File ID: {file_id}, Web View Link: {web_view_link}")
    screenshot_links[f'{account_key} ''Withdrawal'] = web_view_link

    with open(f'screenshot_links_{account_key}.json', 'w') as f:
        json.dump(screenshot_links, f)

    browser.close()



# with sync_playwright() as playwright:
#     test(playwright)

