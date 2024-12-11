FROM jenkins/jenkins:latest

USER root

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    curl \
    gnupg \
    unzip \
    xvfb \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libgdk-pixbuf2.0-0 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуальной среды для Playwright
RUN python3 -m venv /venv

# Установка Playwright в виртуальной среде
RUN /venv/bin/pip install playwright \
    && /venv/bin/python -m playwright install --with-deps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Allure (если нужен для отчетов)
ARG ALLURE_VERSION="2.17.3"
RUN wget -qO- https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz | tar -xz -C /opt/ && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure

# Возвращаемся к пользователю jenkins
USER jenkins
