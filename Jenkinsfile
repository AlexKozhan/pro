pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/AlexKozhan/pro.git' // Укажите ваш репозиторий
            }
        }
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt' // Установите зависимости, если они есть
                sh 'playwright install' // Установка Playwright
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --headed --alluredir=allure-results' // Запуск тестов
            }
        }
        stage('Report') {
            steps {
                allure results: 'allure-results', report: 'allure-report' // Создание отчета Allure
            }
        }
    }
}
