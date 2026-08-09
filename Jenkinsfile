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
                    echo "Running application tests..."
                    if [ -d "tests" ]; then
                        ./venv/bin/python -m pytest tests/
                    else
                        echo "No tests directory found - skipping tests"
                    fi
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

        stage('Docker Build') {
            steps {
                sh '''
                    docker --version
                    docker build -t aisimdp:latest .
                '''
            }
        }

        stage('Docker Deploy') {
            steps {
                sh '''
                    docker stop monitoring_dashboard || true
                    docker rm monitoring_dashboard || true

                    docker run -d \
                        --name monitoring_dashboard \
                        -p 5000:5000 \
                        -v "$WORKSPACE/database/monitoring.db:/app/database/monitoring.db" \
                        aisimdp:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully.'
        }

        failure {
            echo 'CI/CD pipeline failed.'
        }
    }
}
