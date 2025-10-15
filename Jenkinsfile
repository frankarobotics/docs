pipeline {
  agent { dockerfile true }
  triggers {
    pollSCM('H/5 * * * *')
  }
  stages {
    stage('Notify Stash') {
      steps {
        script {
            notifyBitbucket()
        }
      }
    }
    stage('Build & Check') {
      environment {
        HOME="${env.WORKSPACE}"
      }
      stages {
        stage('Install dependencies') {
          steps {
            sh 'npm install eclint@2.8.1'
            sh 'pip3 install --user --upgrade -r requirements.txt'
            sh 'make clean'
          }
        }
        stage('Build HTML') {
          steps {
            sh 'make html'
            publishHTML([allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'build/html',
                        reportFiles: 'index.html',
                        reportName: 'FCI Documentation'])
          }
        }
        stage('Run linter') {
          steps {
            sh 'node $(npm bin)/eclint check source/*.rst'
            sh 'make linkcheck'
          }
        }
      }
    }
  }
  post {
    always {
      cleanWs()
      script {
        notifyBitbucket()
      }
    }
  }
}
