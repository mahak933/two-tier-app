pipeline {
    agent { label 'slave' }

    stages {
        stage("Code Clone") {
            steps {
                git url: "https://github.com/Heyyprakhar1/two-tier-app.git", branch: "project"
                echo "Code cloned successfully!"
            }
        }

        stage("Docker Image Build") {
            steps {
                sh "docker build -t flask-image ."
                echo "Image built successfully!"
            }
        }

        stage("Image Tag & Push to DockerHub") {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhubcred',
                    usernameVariable: 'DockerHubUser',
                    passwordVariable: 'DockerHubPass'
                )]) {

                    sh '''
                      echo "$DockerHubPass" | docker login -u "$DockerHubUser" --password-stdin
                      docker tag flask-image $DockerHubUser/flask-image:latest
                      docker push $DockerHubUser/flask-image:latest
                    '''
                }
            }
        }
        stage("docker compose"){
            steps{
                sh "docker compose up -d"
                echo "docker container is Up & Running..!"
            }
        }
    }
}

