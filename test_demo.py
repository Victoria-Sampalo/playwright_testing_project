from playwright.sync_api import sync_playwright, expect
import re, time


def test_demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.saucedemo.com/")
        expect(page).to_have_title(re.compile("Swag Labs"))
        #Change time value (seconds) for debugging purposes.
        time.sleep(5)