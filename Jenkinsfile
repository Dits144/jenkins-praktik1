pipeline {
    agent {
        docker {
            image 'python:3.10'
        }
    }

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Setup Environment & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest test_app.py
                '''
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch pattern: 'release/.*', comparator: 'REGEXP'
                }
            }
            steps {
                echo "Deploying from branch ${env.BRANCH_NAME}"
                script {
                    def payload = [
                        content: "Build SUCCESS on ${env.BRANCH_NAME}"
                    ]
                    httpRequest(
                        httpMode: 'POST',
                        contentType: 'APPLICATION_JSON',
                        requestBody: groovy.json.JsonOutput.toJson(payload),
                        url: 'https://discordapp.com/api/webhooks/1371549307827781763/7cGxC2z6Ep0UfUklstlzQhXN6c07CRDobkVBblFxbiSdqPS-OGURifUjuurvjrCdY4aa'
                    )
                }
            }
            post {
                success {
                    echo 'Deployment Successful'
                }
                failure {
                    script {
                        def payload = [
                            content: "Build FAILED on branch ${env.BRANCH_NAME}. View details at ${env.BUILD_URL}"
                        ]
                        httpRequest(
                            httpMode: 'POST',
                            contentType: 'APPLICATION_JSON',
                            requestBody: groovy.json.JsonOutput.toJson(payload),
                            url: 'https://discordapp.com/api/webhooks/1371549307827781763/7cGxC2z6Ep0UfUklstlzQhXN6c07CRDobkVBblFxbiSdqPS-OGURifUjuurvjrCdY4aa'
                        )
                    }
                }
            }
        }
    }
}
