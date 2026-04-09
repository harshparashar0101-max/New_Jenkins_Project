pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\ADMIN\\AppData\\Local\\Python\\bin\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/harshparashar0101-max/New_Jenkins_Project.git'
            }
        }

        stage('Check Python') {
            steps {
                bat '"%PYTHON_EXE%" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON_EXE%" -m pip install --upgrade pip'
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat '"%PYTHON_EXE%" -m pytest --junitxml=reports/results.xml'
            }
        }

        stage('Publish Test Report in Jenkins') {
            steps {
                junit 'reports/results.xml'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/results.xml', fingerprint: true
        }
    }
}