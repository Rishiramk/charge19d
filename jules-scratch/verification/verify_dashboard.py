from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to the login page
    page.goto("http://localhost:8069/web/login")

    # Fill in the login form
    page.fill('input[name="login"]', "johndoe")
    page.fill('input[name="password"]', "demo")

    # Click the login button
    page.click('button[type="submit"]')

    # Wait for the dashboard to load by looking for a key element
    expect(page.locator(".profile-card")).to_be_visible()

    # Take a screenshot of the dashboard
    page.screenshot(path="jules-scratch/verification/student_dashboard.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
