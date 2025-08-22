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

def page_to_image(uri: str, data_dir: Path) -> None:
    """
    Navigates to a URI and saves a screenshot to the specified data directory.
    """
    config = argparse.Namespace(
        browser="chromium",
        img_type="png",
        quality=90,
        scale="css",
        omit_background=False,
        full_page=True,
    )

    with sync_playwright() as playwright:
        browser_type = getattr(playwright, config.browser)
        browser = browser_type.launch()
        page = browser.new_page()

        try:
            page.goto(uri)
            page.wait_for_load_state("networkidle", timeout=15000)

            if not extract_uri(page.url):
                print(f"Invalid URI after redirection: {uri!r} -> {page.url!r}")
                return

            filename = re.sub(r"[^a-zA-Z0-9.-]", "_", page.url.replace("https://", "").replace("http://", ""))
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
    # In a real application, this could come from command-line arguments or a config file.
    DATA_DIRECTORY = Path("./data")
    parser = argparse.ArgumentParser(description="Take a screenshot of a web page.")
    parser.add_argument(
        "uri",
        nargs="?",
        default="https://playwright.dev/",
        help="The URI of the web page to capture (default: %(default)s)",
    )
    args = parser.parse_args()
    TARGET_URI = args.uri

    page_to_image(uri=TARGET_URI, data_dir=DATA_DIRECTORY)
