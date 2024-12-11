# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libssl-dev \
    libffi-dev \
    libsdl2-dev \
    libgtk-3-dev \
    libdbus-1-dev \
    libxcomposite-dev \
    libxdamage-dev \
    libxrandr-dev \
    libgbm-dev \
    libasound2-dev \
    libnss3-dev \
    libx11-xcb1 \
    && apt-get clean

# Устанавливаем OpenJDK 17
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Устанавливаем переменную JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Устанавливаем Playwright и необходимые библиотеки
RUN pip install --no-cache-dir playwright==1.32.0

# Устанавливаем зависимости проекта
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Playwright браузеры
RUN python -m playwright install

# Устанавливаем Allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.18.1/allure-2.18.1.zip -O allure.zip && \
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-2.18.1/bin/allure /usr/local/bin/allure && \
    rm allure.zip

# Копируем все файлы проекта в контейнер
COPY . .

# Команда для запуска тестов
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-q", "--alluredir=allure-results"]
