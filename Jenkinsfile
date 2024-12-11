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
                    // Создание виртуального окружения и установка зависимостей
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
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
                    pytest --alluredir=allure-results
                    '''
                }
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
