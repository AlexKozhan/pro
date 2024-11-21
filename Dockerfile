FROM jenkins/jenkins:latest

USER root

<<<<<<< HEAD

=======
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    xvfb \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

ARG CHROME_VERSION="128.0.6613.84"
RUN apt-get update \
    && apt-get install -y google-chrome-stable=${CHROME_VERSION}-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip \
  && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
  && rm /tmp/chromedriver.zip

ARG ALLURE_VERSION="2.17.3"
RUN wget -qO- https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.tgz | tar -xz -C /opt/ && \
    ln -s /opt/allure-${ALLURE_VERSION}/bin/allure /usr/bin/allure

USER jenkins
>>>>>>> origin/main
