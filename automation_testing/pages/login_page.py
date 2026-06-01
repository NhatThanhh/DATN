from browser_use import Agent
from playwright.async_api import async_playwright, expect
import allure

class LoginPage:
    def __init__(self, browser_session, llm_model, base_url):
        self.browser_session = browser_session
        self.llm_model = llm_model
        self.base_url = base_url

    async def login(self, username: str = "", password: str = "", expected_message: str = None):
        agent_task = f"""
            Go to '{self.base_url}'.
            Click on My Account menu.
            Enter username '{username}' in the username textbox.
            Enter password '{password}' in the password textbox.
            Stop after clicking the login button. Do not perform any further actions or retry any goal.
            Do not close the browser."""
        agent = Agent(
            task=agent_task,
            llm=self.llm_model,
            use_vision=True,
            browser_session=self.browser_session,
            max_failures=1,                # chỉ retry 1 lần nếu lỗi
            max_retries=1,                 # LLM gọi lại 1 lần
            stop_on_failure=True,           # không lập kế hoạch lại khi step lỗi
            disable_autocorrect=True
        )
        await agent.run()

        # Playwright verify
        async with async_playwright() as p:
            pw_browser = await p.chromium.connect_over_cdp(self.browser_session.cdp_url)
            try:
                page = pw_browser.contexts[0].pages[-1]

                if expected_message:
                    element = page.locator(f"text={expected_message}")
                else:
                    element = page.locator("text=Logout")

                await expect(element).to_be_visible(timeout=10000)
                actual_text = await element.inner_text()
                screenshot = await page.screenshot(full_page=True)

                # Attach trực tiếp vào Allure
                allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)
                allure.attach(actual_text, name="Actual Text", attachment_type=allure.attachment_type.TEXT)

                return actual_text
            finally:
                await pw_browser.close()