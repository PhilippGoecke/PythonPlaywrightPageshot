podman build --no-cache --rm -f Containerfile -t playwright:pageshot .
podman run --interactive --tty -v ./data:/playwright/data:z playwright:pageshot bash -c "source bin/activate && python3 pageshot.py 'https://podman.io/'"
