pipeline {
    agent any

    environment {
        PYTHON_EXE    = 'C:\\Users\\ADMIN\\AppData\\Local\\Python\\bin\\python.exe'
        XRAY_BASE_URL = 'https://xray.cloud.getxray.app'
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

        stage('Convert JUnit to Xray JSON') {
            steps {
                bat '"%PYTHON_EXE%" junit_to_xray_json.py'
            }
        }

        stage('Authenticate to Xray') {
            steps {
                withCredentials([
                    string(credentialsId: 'XRAY_CLIENT_ID', variable: 'XRAY_CLIENT_ID'),
                    string(credentialsId: 'XRAY_CLIENT_SECRET', variable: 'XRAY_CLIENT_SECRET')
                ]) {
                    bat '''
                    powershell -Command "$body = @{client_id='%XRAY_CLIENT_ID%'; client_secret='%XRAY_CLIENT_SECRET%'} | ConvertTo-Json; $token = Invoke-RestMethod -Method Post -Uri 'https://xray.cloud.getxray.app/api/v2/authenticate' -ContentType 'application/json' -Body $body; Set-Content -Path xray_token.txt -Value $token"
                    '''
                }
            }
        }

        stage('Import Xray JSON Results') {
            steps {
                bat '''
                powershell -Command "$token = Get-Content xray_token.txt; $token = $token.Trim('\\"'); Invoke-RestMethod -Method Post -Uri 'https://xray.cloud.getxray.app/api/v2/import/execution' -Headers @{Authorization = 'Bearer ' + $token} -ContentType 'application/json' -InFile 'reports/xray_results.json'"
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/results.xml, reports/xray_results.json', fingerprint: true
        }

        success {
            emailext(
                to: 'parashar.harsh93@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Passed",
                replyTo: 'harsh.parashar0101@gmail.com'
            )
        }

        failure {
            emailext(
                to: 'parashar.harsh93@gmail.com',
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Build Failed",
                replyTo: 'harsh.parashar0101@gmail.com'
            )
        }
    }
}