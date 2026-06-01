import os
import pytest
import allure
from pages.login_page import LoginPage
from playwright.async_api import async_playwright, expect

TEST_USERNAME="thanhblink@gmail.com"
TEST_PASSWORD="Th@nhthanh200"

# # Test Case 1: Login thành công → verify Logout link
# @pytest.mark.asyncio
# @allure.feature("Authentication")
# @allure.story("Valid Login")
# @allure.title("Verify successful login displays account dashboard")
# async def test_login_success(browser_session, llm_model, base_url):
#     username = TEST_USERNAME
#     password = TEST_PASSWORD
#     login_page = LoginPage(browser_session, llm_model, base_url)
#     actual_text = await login_page.login(username, password)

#     assert "Logout" in actual_text

# # Test Case 2: Login với username và password sai
# @pytest.mark.asyncio
# @allure.feature("Authentication")
# @allure.story("Invalid Login")
# @allure.title("Verify invalid username and password error message")
# async def test_login_invalid(browser_session, llm_model, base_url):
#     login_page = LoginPage(browser_session, llm_model, base_url)
#     expected_message = (
#         "The username wrongusername is not registered on this site. "
#         "If you are unsure of your username, try your email address instead."
#     )
#     actual_text = await login_page.login("wrongusername", "wrong_password_12345", expected_message)
#     assert expected_message in actual_text

# # Test Case 3: Login sai với password sai
# @pytest.mark.asyncio
# @allure.feature("Authentication")
# @allure.story("Invalid Login")
# @allure.title("Verify invalid password error message")
# async def test_login_invalid_password(browser_session, llm_model, base_url):
#     login_page = LoginPage(browser_session, llm_model, base_url)
#     expected_message = (
#         f"The password you entered for the username {TEST_USERNAME} is incorrect"
#     )
#     actual_text = await login_page.login(TEST_USERNAME, "wrong_password_12345", expected_message)
#     assert expected_message in actual_text

# # Test Case 4: Login sai với username sai
# @pytest.mark.asyncio
# @allure.feature("Authentication")
# @allure.story("Invalid Login")
# @allure.title("Verify invalid username error message")
# async def test_login_invalid_username(browser_session, llm_model, base_url):
#     login_page = LoginPage(browser_session, llm_model, base_url)
#     expected_message = (
#         "The username wrongusername is not registered on this site. "
#         "If you are unsure of your username, try your email address instead."
#     )
#     actual_text = await login_page.login("wrongusername", TEST_PASSWORD, expected_message)
#     assert expected_message in actual_text

# # Test Case 5: Login với kí tự in hoa username
# @pytest.mark.asyncio
# @allure.feature("Authentication")
# @allure.story("Case-sensitive Login")
# @allure.title("Verify login fails when username has uppercase letters")
# async def test_login_case_sensitive_username(browser_session, llm_model, base_url):
#     login_page = LoginPage(browser_session, llm_model, base_url)
#     expected_error = "The username Thanhblink@gmail.com is not registered on this site."
#     actual_text = await login_page.login("Thanhblink@gmail.com", "Th@nhthanh200", expected_error)
#     assert expected_error in actual_text

# # Test Case 6: Kiểm tra phân biệt in hoa và chữ thường trong password
# @pytest.mark.asyncio
# @allure.feature("Authentication")
# @allure.story("Case-sensitive Login")
# @allure.title("Verify login fails when password has uppercase letters")
# async def test_login_case_sensitive_password(browser_session, llm_model, base_url):
#     login_page = LoginPage(browser_session, llm_model, base_url)
#     expected_error = f"The password you entered for the username {TEST_USERNAME} is incorrect. Lost your password?"
#     actual_text = await login_page.login(TEST_USERNAME, "th@nhthanh200", expected_error)
#     assert expected_error in actual_text

# # Test Case 7: Empty username + valid password → Invalid username
# @pytest.mark.asyncio
# @allure.feature("Authentication")
# @allure.story("Empty Username with valid password")
# @allure.title("Verify error for empty username")
# async def test_empty_username_valid_password(browser_session, llm_model, base_url):
#     login_page = LoginPage(browser_session, llm_model, base_url)
#     expected_error = "Username is required."
#     actual_text = await login_page.login("", TEST_PASSWORD, expected_error)
#     assert expected_error in actual_text

# Test Case 8: Logout + back button → user không còn đăng nhập
@pytest.mark.asyncio
@allure.feature("Authentication")
@allure.story("Logout and Back Button")
@allure.title("Verify user cannot access account after logout and back")
async def test_logout_back_behavior(browser_session, llm_model, base_url):
    login_page = LoginPage(browser_session, llm_model, base_url)
    
    # login thành công
    await login_page.login(TEST_USERNAME, TEST_PASSWORD)
    
    # logout và nhấn back
    async with async_playwright() as p:
        pw_browser = await p.chromium.connect_over_cdp(browser_session.cdp_url)
        try:
            page = pw_browser.contexts[0].pages[-1]

            # Click Logout
            await page.locator("text=Logout").click()

            # Nhấn back
            await page.go_back()

            # Đợi page load và kiểm tra nút Logout không còn hiển thị
            logout_locator = page.locator("text=Logout")
            await expect(logout_locator).not_to_be_visible(timeout=10000)

            # Chụp screenshot attach vào Allure
            screenshot = await page.screenshot(full_page=True)
            allure.attach(screenshot, name="Back After Logout", attachment_type=allure.attachment_type.PNG)

        finally:
            await pw_browser.close()