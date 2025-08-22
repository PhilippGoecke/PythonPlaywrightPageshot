FROM debian:trixie-slim

#SHELL ["/bin/bash", "-c"]
RUN rm /bin/sh \
  && ln -s /bin/bash /bin/sh

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y \
  # install tools
  && apt install -y --no-install-recommends python3-virtualenv python3.13-venv python3-pip \
  # install Playwright dependencies
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
RUN useradd --shell /bin/bash $USER
USER $USER

WORKDIR /playwright

COPY pageshot.py pageshot.py

RUN python3 -m venv . \
  && source bin/activate \
  && pip install playwright pytest-playwright pil image \
  && playwright install

VOLUME /playwright/data

CMD source bin/activate && python pageshot.py
