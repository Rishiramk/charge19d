from playwright.sync_api import sync_playwright, Page, expect

def verify_student_dashboard_header(page: Page):
    """
    This script logs in as a student, navigates to the portal,
    and captures a screenshot of the redesigned profile header.
    """
    # 1. Arrange: Navigate to the login page
    # Assuming the Odoo instance is running on port 8069
    base_url = "http://localhost:8069"
    page.goto(f"{base_url}/web/login")

    # 2. Act: Log in as the demo student "johndoe" with password "demo"
    page.get_by_label("Email").fill("johndoe")
    page.get_by_label("Password").fill("demo")
    page.get_by_role("button", name="Log in").click()

    # 3. Act: Navigate to the student portal dashboard
    page.goto(f"{base_url}/my/home")

    # 4. Assert: Wait for the redesigned profile banner to be visible
    # We locate the new banner element and check for the student's name within it.
    profile_banner = page.locator("div.card-body.p-4")
    expect(profile_banner).to_be_visible()
    expect(profile_banner.get_by_role("heading", name="John Doe")).to_be_visible()

    # 5. Screenshot: Capture the banner element for visual verification.
    profile_banner.screenshot(path="jules-scratch/verification/profile_header_redesign.png")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_student_dashboard_header(page)
            print("Successfully created screenshot: jules-scratch/verification/profile_header_redesign.png")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()