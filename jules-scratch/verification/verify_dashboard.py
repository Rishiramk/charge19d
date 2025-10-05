import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # 1. Navigate to the login page
    # Assuming the local Odoo instance is running on the default port 8069
    page.goto("http://localhost:8069/web/login")

    # 2. Perform login
    page.get_by_label("Email").fill("johndoe")
    page.get_by_label("Password").fill("demo")
    page.get_by_role("button", name="Log in").click()

    # 3. Navigate to the student dashboard
    # The controller is set to handle '/my/home'
    page.goto("http://localhost:8069/my/home")

    # 4. Assert: Wait for a key element of the new dashboard to be visible
    # We'll wait for the main profile card with the student's name to appear.
    profile_header = page.get_by_role("heading", name="John Doe")
    expect(profile_header).to_be_visible(timeout=10000) # Increased timeout for page load

    # 5. Take a screenshot for visual verification
    page.screenshot(path="jules-scratch/verification/dashboard_screenshot.png")

    # Close browser
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)