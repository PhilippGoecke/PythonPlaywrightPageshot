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


def take_dynamic_quality_screenshot(
    page: Page, imagepath: Path, config: argparse.Namespace
) -> int:
    """
    Takes a screenshot, reducing quality iteratively if the file size is too large.
    """
    quality = config.quality
    omit_background = config.omit_background

    def attempt_screenshot(current_quality: int, omit_bg: bool) -> int:
        """Helper to take a screenshot and return its size in bytes."""
        screenshot_bytes = page.screenshot(
            path=imagepath,
            type=config.img_type,
            quality=current_quality,
            scale=config.scale,
            omit_background=omit_bg,
            full_page=config.full_page,
        )
        return len(screenshot_bytes)

    size = attempt_screenshot(quality, omit_background)

    # If the initial screenshot is empty, fail early.
    if size <= 0:
        return 0

    # Reduce quality if the image is larger than 1MB, down to a minimum of 40.
    while size > 1024**2 and quality >= 40:
        quality -= 10
        # On the first quality reduction, disable background transparency if it was enabled
        if omit_background:
            omit_background = False
        size = attempt_screenshot(quality, omit_background)

    return size


def page_to_image(uri: str, data_dir: Path) -> None:
    """
    Navigates to a URI and saves a screenshot to the specified data directory.
    """
    config = argparse.Namespace(
        browser="firefox",
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

            imagepath = data_dir / f"pageshot.{config.img_type}"
            data_dir.mkdir(exist_ok=True)

            pic_size = take_dynamic_quality_screenshot(page, imagepath, config)

            if pic_size <= 0:
                print(f"Failed to take screenshot of {uri}")
            elif pic_size <= 10 * 1024**2:  # 10 MB limit
                print(f"Screenshot saved to {imagepath}")
            else:
                print(f"Screenshot for {uri} is too large even after reducing quality.")

        except Exception as e:
            print(f"An error occurred while processing {uri}: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    # In a real application, this could come from command-line arguments or a config file.
    DATA_DIRECTORY = Path("./data")
    TARGET_URI = "http://www.test.de/"

    page_to_image(uri=TARGET_URI, data_dir=DATA_DIRECTORY)
