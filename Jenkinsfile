pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    venv\\Scripts\\python.exe -m pytest tests
                '''
            }
        }
    }

    post {
        always {
            bat '''
                docker rm -f fastapi-users 2>NUL
                exit /B 0
            '''
        }

        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'CI pipeline failed!'
        }
    }
}
