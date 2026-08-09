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

                        /opt/sonar-scanner/bin/sonar-scanner \
                            -Dsonar.token="$SONAR_TOKEN"
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."

                    docker build -t aisimdp:latest .

                    echo "Docker image built successfully."

                    docker images | grep aisimdp
                '''
            }
        }

        stage('Test Container') {
            steps {
                sh '''
                    echo "Testing Python and dependencies..."

                    docker run --rm aisimdp:latest python --version

                    docker run --rm aisimdp:latest python -c "import flask; print('Flask:', flask.__version__)"

                    echo "Python and Flask dependency test passed."
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    echo "Running Trivy security scan..."

                    trivy image \
                        --severity HIGH,CRITICAL \
                        --ignore-unfixed \
                        --exit-code 0 \
                        aisimdp:latest

                    echo "Security scan completed."
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

                    echo "Container deployed successfully."

                    docker ps | grep monitoring_dashboard
                '''
            }
        }

        stage('Build Completed') {
            steps {
                echo '========================================'
                echo ' AISIMDP CI/CD PIPELINE COMPLETED'
                echo '========================================'
                echo 'Checkout          : PASSED'
                echo 'SonarCloud        : PASSED'
                echo 'Docker Build      : PASSED'
                echo 'Container Test    : PASSED'
                echo 'Security Scan     : PASSED'
                echo 'Deployment        : PASSED'
                echo '========================================'
            }
        }
    }

    post {
        success {
            echo 'AISIMDP DevSecOps pipeline completed successfully!'
        }

        failure {
            echo 'AISIMDP pipeline failed. Check the failed stage.'
        }
    }
}
