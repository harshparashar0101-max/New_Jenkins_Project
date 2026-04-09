pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/harshparashar0101-max/New_Jenkins_Project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'python -m pytest --junitxml=reports/results.xml'
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