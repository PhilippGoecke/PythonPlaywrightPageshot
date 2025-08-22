podman build --no-cache --rm -f Containerfile -t playwright:pageshot .
#podman run --interactive --tty -v ./data:/playwright/data playwright:pageshot
podman run --interactive --tty -v ./data:/playwright/data playwright:pageshot python pageshot.py "https://playwright.dev"
