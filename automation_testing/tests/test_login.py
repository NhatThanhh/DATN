import os
from browser_use import Agent
from playwright.async_api import async_playwright, expect
from utils.test_result_writer import save_test_result


# async def test_login_success(browser_session, llm_model, base_url):
#     username = os.getenv("TEST_USERNAME")
#     password = os.getenv("TEST_PASSWORD")

#     if not username or not password:
#         raise ValueError("Missing TEST_USERNAME or TEST_PASSWORD in .env file")

#     agent = Agent(
#         task=f"""
#             Go to '{base_url}'.
#             Click on My Account menu.
#             Enter registered username '{username}' in the username textbox.
#             Enter password '{password}' in the password textbox.
#             Click on the Login button.
#             Wait until the My Account page is loaded after login.
#             Do not close the browser.
#         """,
#         llm=llm_model,
#         use_vision=True,
#         browser_session=browser_session,
#     )

#     result = await agent.run()
#     print("Agent result:", result)

#     # Lấy CDP URL của browser mà Browser Use đang mở
#     cdp_url = getattr(browser_session, "cdp_url", None)

#     assert cdp_url is not None, "Cannot get CDP URL from Browser Use session."

#     # Playwright connect vào đúng browser đó để verify bằng locator
#     async with async_playwright() as p:
#         pw_browser = await p.chromium.connect_over_cdp(cdp_url)

#         try:
#             assert len(pw_browser.contexts) > 0, "No browser context found from CDP connection."

#             context = pw_browser.contexts[0]

#             assert len(context.pages) > 0, "No page found in browser context."

#             page = context.pages[-1]

#             await page.wait_for_load_state("domcontentloaded")

#             logout_link = page.locator("a:has-text('Logout')")

#             await expect(logout_link).to_be_visible(timeout=10000)

#         finally:
#             await pw_browser.close()


# Login with invalid username and invalid pass
async def test_login_with_invalid_credentials(browser_session, llm_model, base_url):
    invalid_username = "wrongusername"
    invalid_password = "wrong_password_12345"

    expected_message = (
        "The username wrongusername is not registered on this site. "
        "If you are unsure of your username, try your email address instead."
    )

    agent = Agent(
        task=f"""
            Go to '{base_url}'.
            Click on My Account menu.
            Enter incorrect username '{invalid_username}' in the username textbox.
            Enter incorrect password '{invalid_password}' in the password textbox.
            Click on the Login button.
            Wait until the login error message is displayed.
            Do not close the browser.
        """,
        llm=llm_model,
        use_vision=True,
        browser_session=browser_session,
    )

    await agent.run()

    async with async_playwright() as p:
        pw_browser = await p.chromium.connect_over_cdp(browser_session.cdp_url)

        try:
            page = pw_browser.contexts[0].pages[-1]

            error_message = page.locator(f"text={expected_message}")

            await expect(error_message).to_be_visible(timeout=10000)

            actual_result = await error_message.inner_text()

            save_test_result(
                test_name="test_login_with_invalid_credentials",
                status="PASSED",
                expected_result=expected_message,
                actual_result=actual_result,
                file_name="test_login_with_invalid_credentials.json",
                extra={
                    "url": base_url,
                    "invalid_username": invalid_username,
                    "verified_by": "Playwright text locator"
                }
            )

        except Exception as e:
            save_test_result(
                test_name="test_login_with_invalid_credentials",
                status="FAILED",
                expected_result=expected_message,
                actual_result=str(e),
                file_name="test_login_with_invalid_credentials.json",
                extra={
                    "url": base_url,
                    "invalid_username": invalid_username,
                    "verified_by": "Playwright text locator"
                }
            )
            raise

        finally:
            await pw_browser.close()