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
                    // Генерация отчета Allure
                    allure results: ['allure-results'], report: 'allure-report'
                }
            }
        }
    }
}
