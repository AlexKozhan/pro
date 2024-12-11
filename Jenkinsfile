pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AlexKozhan/pro.git'
            }
        }

        stage('Setup') {
            steps {
                script {
                    // Создание виртуального окружения и установка зависимостей
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Install Playwright and Dependencies') {
            steps {
                script {
                    // Установка Playwright и его зависимостей
                    sh '''
                    . ${VENV_DIR}/bin/activate
                    pip install playwright
                    python3 -m playwright install-deps
                    python3 -m playwright install
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Запуск тестов с записью результатов для Allure
                    sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest --alluredir=allure-results || true
                    '''
                }
            }
        }

        stage('Report') {
            steps {
                // Генерация отчета Allure
                allure([
                    results: [[path: 'allure-results']],
                    report: 'allure-report'
                ])
            }
        }
    }

    post {
        always {
            // Очистка рабочей директории после выполнения pipeline
            cleanWs()
        }
    }
}
