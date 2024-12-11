pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/AlexKozhan/pro.git'
            }
        }
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --alluredir=allure-results'
            }
        }
        stage('Report') {
            steps {
                allure(
                    results: ['allure-results'],  // Путь к результатам тестов
                    report: 'allure-report'       // Путь для отчета
                )
            }
        }
    }
}
