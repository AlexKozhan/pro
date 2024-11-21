FROM jenkins/jenkins:latest

USER root

# Установка необходимых пакетов
RUN apt-get update && \
    apt-get install -y python3-pip python3-venv wget curl unzip gnupg

# Добавление официального ключа и репозитория Google Chrome
RUN curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update

# Установка последней версии Google Chrome
RUN apt-get install -y google-chrome-stable

# Установка подходящей версии ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Установка Allure Commandline
RUN wget -qO- https://github.com/allure-framework/allure2/releases/download/2.17.3/allure-2.17.3.tgz | tar -xz -C /opt/ && \
    ln -s /opt/allure-2.17.3/bin/allure /usr/bin/allure

# Очистка
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Возвращаемся к пользователю Jenkins
USER jenkins
