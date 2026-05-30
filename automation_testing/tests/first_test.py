from playwright.sync_api import expect


def test_open_homepage(page):
    # Website đã được mở sẵn từ fixture trong conftest.py

    # Verify title của trang
    expect(page).to_have_title("Automation Practice Site")

    # Verify menu Shop hiển thị
    shop_menu = page.get_by_role("link", name="Shop")
    expect(shop_menu).to_be_visible()

    print("PASS: Homepage opened successfully and Shop menu is visible.")