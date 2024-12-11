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
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    playwright install-deps || true
                    '''
                }
            }
        }
        stage('Install Playwright') {
            steps {
                script {
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
                    sh '''
                    . venv/bin/activate
                    pytest --alluredir=allure-results || true
                    '''
                }
            }
        }
        stage('Report') {
            steps {
                allure(
                    results: [[path: 'allure-results']],
                    report: 'allure-report'
                )
            }
        }
    }
}
