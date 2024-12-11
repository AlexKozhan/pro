pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Убедитесь, что используете правильный бранч
                git branch: 'main', url: 'https://github.com/AlexKozhan/pro.git'
            }
        }
        stage('Setup') {
            steps {
                script {
                    // Создание виртуального окружения
                    sh 'python3 -m venv venv'

                    // Активация виртуального окружения
                    sh '. venv/bin/activate'

                    // Установка зависимостей в виртуальное окружение
                    sh 'pip install -r requirements.txt'

                    // Установка Playwright
                    sh 'playwright install'
                }
            }
        }
        stage('Test') {
            steps {
                // Запуск тестов
                sh '. venv/bin/activate && pytest --alluredir=allure-results'
            }
        }
        stage('Report') {
            steps {
                // Генерация отчета Allure
                allure results: ['allure-results'], report: 'allure-report'
            }
        }
    }
}
