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
                        url: 'https://discordapp.com/api/webhooks/1372109455017119784/zLGKZUT-vq55TlO7XkE4EP4VVuMNX4tDcim5jUm3ntsgHYVcIsRcOJt2U1zL4lH8xDD8'
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
                            url: 'https://discordapp.com/api/webhooks/1372109455017119784/zLGKZUT-vq55TlO7XkE4EP4VVuMNX4tDcim5jUm3ntsgHYVcIsRcOJt2U1zL4lH8xDD8'
                        )
                    }
                }
            }
        }
    }
}
