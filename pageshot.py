from playwright.sync_api
import sync_playwright from argparse
import Namespace
import re
from time import sleep
from pathlib import Path
from typing import Optional
from PIL import Image

def extract_uri(text: str) -> Optional[str]:
    uri_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    match = uri_regex.search(text)

    if match:
        return match.group()

    return None

def take_pageshot(page, config: Namespace, imagepath: Path) -> int:

    def do_pageshot() -> int:
        return len(
            page.screenshot(
                path=imagepath,
                type=config.img_type,
                quality=config.quality,
                scale=config.scale,
                omit_background=config.omit_background,
                full_page=config.full_page,
            )
        )

    pic_size = do_pageshot()

    if pic_size <= 0:
        return pic_size

    config.omit_background = False
    while pic_size > 1024**2 * 1 and config.quality >= 40:
        config.quality -= 10
        pic_size = do_pageshot()
    return pic_size

def page2img(uri: str) -> None:
    config = Namespace(
        browser="firefox",
        img_type="jpg",
        quality=90,
        scale="css",
        omit_background=False,
        full_page=True,
    )

    with sync_playwright() as playwright:
        if config.browser == "firefox":
            browser_type = playwright.firefox
        elif config.browser == "webkit":
            browser_type = playwright.webkit
        else:
            browser_type = playwright.chromium
        browser = browser_type.launch()

        page = browser.new_page()
        page.goto(uri)
        page.wait_for_load_state("load")

        if extract_uri(page.url):
            sleep(3)

            data_dir = "/playwright/data"

            imagepath = Path(data_dir, f"pageshot.{config.img_type}")

            pic_size = take_pageshot(page, config, imagepath)

            if pic_size <= 0:
                print("Failed to load uri")
            elif pic_size <= 1024**2 * 10:
                print(f"Pageshot taken in {imagepath}")
                pageshot = Image.open(str(imagepath))
                pageshot.show()
            else:
                print("Failed with URI, page too huge")
        else:
            print(f"Invalid URI redirection: {uri!r} -> {page.url!r}")

        browser.close()

page2img(uri="https://test.de/")
