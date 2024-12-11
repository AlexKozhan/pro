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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Node.js (Playwright работает на Node.js)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Установка Playwright
RUN npm install -g playwright

# Установка Allure (если нужен для отчетов)
ARG ALLURE_VERSION="2.17.3"
RUN wget -qO- https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz | tar -xz -C /opt/ && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure

USER jenkins
