pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarCloud Analysis') {
            steps {
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        echo "Running SonarCloud analysis..."
                        sonar-scanner \
                          -Dsonar.token="$SONAR_TOKEN"
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build --no-cache -t aisimdp:latest .
                '''
            }
        }

        stage('Test Container') {
            steps {
                sh '''
                    echo "Testing Python and dependencies..."
                    docker run --rm aisimdp:latest python --version
                    docker run --rm aisimdp:latest python -c "import flask; print('Flask:', flask.__version__)"
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    echo "Running Trivy security scan..."
                    trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 0 aisimdp:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "Deploying container..."
                    docker stop monitoring_dashboard || true
                    docker rm monitoring_dashboard || true
                    docker run -d \
                      --name monitoring_dashboard \
                      -p 5000:5000 \
                      -v /home/admin/AISIMDP/database:/app/database \
                      aisimdp:latest
                '''
            }
        }

        stage('Build Completed') {
            steps {
                echo 'AISIMDP CI/CD pipeline completed successfully.'
            }
        }
    }
}
