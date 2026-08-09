pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    ./venv/bin/python -m pytest tests/ 
                '''
            }
        }

        stage('Security Check') {
            steps {
                sh '''
                    echo "Running basic security checks..."
                    ./venv/bin/pip check
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Build completed successfully.'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully.'
        }

        failure {
            echo 'CI pipeline failed.'
        }
    }
}
