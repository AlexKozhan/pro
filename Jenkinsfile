pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Проверка репозитория
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
        stage('Install Playwright') {
            steps {
                script {
                    // Установка Playwright и его зависимостей
                    sh '''
                    . venv/bin/activate
                    pip install playwright
                    playwright install
                    '''
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Запуск тестов в виртуальном окружении
                    sh '''
                    . venv/bin/activate
                    pytest --alluredir=allure-results || true
                    '''
                }
            }
        }
        stage('Report') {
            steps {
                script {
                    // Генерация отчета Allure с правильной конфигурацией
                    allure(
                        results: [[path: 'allure-results']],
                        report: 'allure-report'
                    )
                }
            }
        }
    }
}
