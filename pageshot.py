#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
from pathlib import Path
from typing import Optional

from playwright.sync_api import Page, sync_playwright

def extract_uri(text: str) -> Optional[str]:
    """Extracts the first URI from a given text."""
    uri_regex = re.compile(r"https?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F]{2}))+")
    match = uri_regex.search(text)
    return match.group(0) if match else None

def take_screenshot(
    page: Page, imagepath: Path, config: argparse.Namespace
) -> int:
    """
    Takes a screenshot of the page.
    """
    screenshot_options = {
        "path": imagepath,
        "type": config.img_type,
        "scale": config.scale,
        "omit_background": config.omit_background,
        "full_page": config.full_page,
    }
    if config.img_type == "jpeg":
        screenshot_options["quality"] = config.quality

    screenshot_bytes = page.screenshot(**screenshot_options)
    return len(screenshot_bytes) if screenshot_bytes else 0

def page_to_image(uri: str, data_dir: Path, config: argparse.Namespace) -> None:
    """
    Navigates to a URI and saves a screenshot to the specified data directory.
    """
    launch_options = {}
    if config.proxy_server:
        proxy_config = {"server": config.proxy_server}
        if config.proxy_username:
            proxy_config["username"] = config.proxy_username
        if config.proxy_password:
            proxy_config["password"] = config.proxy_password
        launch_options["proxy"] = proxy_config

    with sync_playwright() as playwright:
        browser_type = getattr(playwright, config.browser)
        browser = browser_type.launch(**launch_options)
        page = browser.new_page()

        try:
            page.goto(uri, wait_until="networkidle", timeout=15000)

            if not extract_uri(page.url):
                print(f"Invalid URI after redirection: {uri!r} -> {page.url!r}")
                return

            filename = re.sub(r"[^a-zA-Z0-9.-]", "_", page.url.replace("https://", "").replace("http://", "")).rstrip("_")
            imagepath = data_dir / f"{filename}.{config.img_type}"
            data_dir.mkdir(exist_ok=True)

            pic_size = take_screenshot(page, imagepath, config)

            if pic_size <= 0:
                print(f"Failed to take screenshot of {uri}")
            elif pic_size <= 10 * 1024**2:  # 10 MB limit
                print(f"Screenshot saved to {imagepath}")
            else:
                print(f"Screenshot for {uri} is too large.")

        except Exception as e:
            print(f"An error occurred while processing {uri}: {e}")
        finally:
            browser.close()

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch a browser
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the page
        await page.goto("https://playwright.dev/")

        # Take a screenshot
        await page.screenshot(path="playwright_dev.png", full_page=True)
        print("Screenshot saved as playwright_dev.png")

        # Clean up
        await browser.close()

if __name__ == "__main__":
    DATA_DIRECTORY = Path("./data")
    parser = argparse.ArgumentParser(description="Take a screenshot of a web page.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_DIRECTORY,
        help="Directory to save screenshots (default: %(default)s)",
    )
    parser.add_argument(
        "uri",
        nargs="?",
        default="https://www.python.org/",
        help="The URI of the web page to capture (default: %(default)s)",
    )
    parser.add_argument("--browser", default="firefox", help="Browser to use (chromium, firefox, webkit)")
    parser.add_argument("--img-type", default="png", choices=["png", "jpeg"], help="Image type")
    parser.add_argument("--quality", type=int, default=90, help="JPEG quality (0-100)")
    parser.add_argument("--scale", default="css", choices=["css", "device"], help="Scale of the screenshot")
    parser.add_argument("--omit-background", action="store_true", help="Omit background from screenshot")
    parser.add_argument("--no-full-page", dest="full_page", action="store_false", help="Do not take a full page screenshot")
    parser.add_argument("--proxy-server", help="Proxy server URL (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--proxy-username", help="Username for proxy authentication")
    parser.add_argument("--proxy-password", help="Password for proxy authentication")

    args = parser.parse_args()
    TARGET_URI = args.uri

    page_to_image(uri=TARGET_URI, data_dir=DATA_DIRECTORY, config=args)
