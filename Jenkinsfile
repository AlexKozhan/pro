pipeline {
    agent any
    parameters {
        choice(name: 'TEST_SUITE', choices: ['smoke', 'critical', 'extended', 'API', 'UI'], description: 'Choose the test suite to run')
    }
    stages {
        stage('Setup Environment') {
            steps {
                script {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh """
                        . venv/bin/activate
                        pytest --alluredir=allure-results -m ${params.TEST_SUITE}
                    """
                }
            }
        }
    }
    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}
