FROM debian:trixie-slim

#SHELL ["/bin/bash", "-c"]
RUN rm /bin/sh \
  && ln -s /bin/bash /bin/sh

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y \
  # install tools
  && apt install -y --no-install-recommends python3-virtualenv python3.13-venv python3-pip \
  # install Playwright dependencies
  && apt install -y --no-install-recommends libglib2.0-0 libspr4 libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcb1 libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libcairo2 libpango-1.0-0 libasound2 \
  && apt install -y --no-install-recommends libffi-dev libwebp-dev libjpeg-dev libicu-dev \
  # make image smaller
  && rm -rf "/var/lib/apt/lists/*" \
  && rm -rf /var/cache/apt/archives

RUN cd /usr/lib/x86_64-linux-gnu \
  && ln -s libffi.so.8 libffi.so.7 \
  && ln -s libwebp.so.7 libwebp.so.6 \
  && ln -s libjpeg.so libjpeg.so.8 \
  && ln -s libicudata.so.76 libicudata.so.66 \
  && ln -s libicui18n.so.76 libicui18n.so.66 \
  && ln -s libicuuc.so.76 libicuuc.so.66

ARG USER=playwright
RUN useradd --create-home --shell /bin/bash $USER \
  && mkdir /playwright \
  && chown $USER /playwright
USER $USER

WORKDIR /playwright

COPY pageshot.py pageshot.py

RUN python3 -m venv . \
  && source bin/activate \
  && pip install pytest-playwright \
  && playwright install

VOLUME /playwright/data

CMD source bin/activate && python pageshot.py "https://playwright.dev"
