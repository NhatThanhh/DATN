import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from playwright.async_api import ViewportSize

from browser_use import ChatGroq
from browser_use.browser.session import BrowserSession
from browser_use.browser.profile import BrowserProfile


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

BASE_URL = "http://practice.automationtesting.in/"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def llm_model():
    api_key = os.getenv("GROQ_API_KEY")

    print("GROQ_API_KEY loaded:", bool(api_key))
    print("GROQ_API_KEY prefix:", api_key[:4] if api_key else None)
    print("GROQ_API_KEY length:", len(api_key) if api_key else None)

    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env file")

    return ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=api_key.strip(),
        temperature=0.0
    )


@pytest_asyncio.fixture(scope="function")
async def browser_session():
    recording_path = os.path.join(PROJECT_ROOT, "exports", "recordings")
    trace_path = os.path.join(PROJECT_ROOT, "exports", "traces")

    os.makedirs(recording_path, exist_ok=True)
    os.makedirs(trace_path, exist_ok=True)

    browser_profile = BrowserProfile(
        user_data_dir=None,
        headless=False,
        no_viewport=True,
        disable_security=True,
        wait_for_network_idle_page_load_time=3.0,
        highlight_elements=True,
        viewport_expansion=-1,

        # Nếu chưa cài browser-use[video] thì có thể tạm comment 2 dòng record_video này
        record_video_dir=recording_path,
        record_video_size=ViewportSize(width=1920, height=1080),

        record_har_path=os.path.join(recording_path, "login.har"),
        traces_dir=trace_path,

        args=[
            "--disable-save-password-bubble",
            "--disable-features=PasswordManagerOnboarding,PasswordLeakDetection,AutofillServerCommunication",
            "--disable-popup-blocking",
            "--disable-notifications",
        ],
    )

    session = BrowserSession(browser_profile=browser_profile, keep_alive=True)

    yield session

    await session.kill()