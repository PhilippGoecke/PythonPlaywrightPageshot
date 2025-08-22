podman build --no-cache --rm -f Containerfile -t playwright:pageshot .
#podman run --interactive --tty -v ./data:/playwright/data playwright:pageshot
podman run --interactive --tty -v ./data:/playwright/data playwright:pageshot "source bin/activate && python pageshot.py 'https://podman.io/'"
