class WelcomePage:
    login_button = "aside > div > button.button-secondary"
    login_button_DE = "aside > div > button.button-secondary"
    email_field = "#email"
    password_field = "#password"
    confirm_login = "xpath=//div[contains(@class, 'flex')]//div[contains(@class, 'mb-5')]/following-sibling::button[contains(@class, 'button-secondary')]"
    deposit_button = "aside > div > button.button-primary"
    pop_up = '[data-test-id="dep_modal"]'
    wrapper = "[data-test-id='tourn_modal']"