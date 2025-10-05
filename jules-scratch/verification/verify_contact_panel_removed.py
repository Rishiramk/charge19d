import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # 1. Navigate to the login page
    page.goto("http://localhost:8069/web/login")

    # 2. Perform login
    page.get_by_label("Email").fill("johndoe")
    page.get_by_label("Password").fill("demo")
    page.get_by_role("button", name="Log in").click()

    # 3. Navigate to the student dashboard
    page.goto("http://localhost:8069/my/home")

    # 4. Assert: Verify that the contact details panel is NOT visible.
    # The panel has the class 'o_portal_my_details'.
    contact_panel = page.locator(".o_portal_my_details")
    expect(contact_panel).not_to_be_visible(timeout=10000)

    # 5. Take a screenshot for visual confirmation of the clean layout
    page.screenshot(path="jules-scratch/verification/contact_panel_removed.png")

    # Close browser
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)