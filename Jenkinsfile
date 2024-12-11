pipeline {
    agent any
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
                    python3 -m venv venv
                    . venv/bin/activate
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
                    . venv/bin/activate
                    pip install playwright
                    python3 -m playwright install-deps
                    playwright install
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Запуск тестов
                    sh '''
                    . venv/bin/activate
                    pytest --alluredir=allure-results || true
                    '''
                }
            }
        }
        stage('Report') {
            steps {
                // Генерация отчета Allure
                allure(
                    results: [[path: 'allure-results']],
                    report: 'allure-report'
                )
            }
        }
    }
}
