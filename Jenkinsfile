pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = "docker.io"
        IMAGE_NAME = credentials('docker_username')
        DOCKER_CREDENTIALS = credentials('docker_credentials')
GITHUB_REPO = 'https://github.com/AVISRJ062002/new-project-flask.git'
        CONTAINER_NAME = "cicd-app-container"
        CONTAINER_PORT = "5000"
        HOST_PORT = "5000"
    }
    
    stages {
        stage('Clone GitHub Repository') {
            steps {
                script {
                    echo "🔄 Cloning GitHub repository..."
                    try {
                        if (fileExists('app/Dockerfile') || fileExists('Dockerfile')) {
                            echo "✅ Using existing workspace checkout"
                        } else {
                            git branch: 'main',
                                url: "${GITHUB_REPO}"
                            echo "✅ Repository cloned successfully"
                        }
                    } catch (Exception e) {
                        echo "⚠️ Using local repository for this demo: ${e.message}"
                    }
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "🐳 Building Docker image..."
                    try {
                        def buildDir = fileExists('app/Dockerfile') ? 'app' : '.'
                        dir(buildDir) {
                            if (isUnix()) {
                                sh '''
                                    docker build -t ${IMAGE_NAME}/cicd-app:${BUILD_NUMBER} .
                                    docker tag ${IMAGE_NAME}/cicd-app:${BUILD_NUMBER} ${IMAGE_NAME}/cicd-app:latest
                                '''
                            } else {
                                bat '''
                                    docker build -t %IMAGE_NAME%/cicd-app:%BUILD_NUMBER% .
                                    docker tag %IMAGE_NAME%/cicd-app:%BUILD_NUMBER% %IMAGE_NAME%/cicd-app:latest
                                '''
                            }
                            echo "✅ Docker image built successfully: ${IMAGE_NAME}/cicd-app:${BUILD_NUMBER}"
                        }
                    } catch (Exception e) {
                        echo "❌ Docker build failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Docker build failed")
                    }
                }
            }
        }
        
        stage('Login to Docker Hub') {
            steps {
                script {
                    echo "🔐 Authenticating with Docker Hub..."
                    try {
                        if (isUnix()) {
                            sh '''
                                echo ${DOCKER_CREDENTIALS_PSW} | docker login -u ${DOCKER_CREDENTIALS_USR} --password-stdin
                            '''
                        } else {
                            bat '''
                                @echo %DOCKER_CREDENTIALS_PSW%| docker login -u %DOCKER_CREDENTIALS_USR% --password-stdin
                            '''
                        }
                        echo "✅ Successfully authenticated with Docker Hub"
                    } catch (Exception e) {
                        echo "⚠️ Docker Hub login failed (may use local registry): ${e.message}"
                    }
                }
            }
        }
        
        stage('Push Docker Image to Registry') {
            steps {
                script {
                    echo "📤 Pushing Docker image to registry..."
                    try {
                        if (isUnix()) {
                            sh '''
                                docker push ${IMAGE_NAME}/cicd-app:${BUILD_NUMBER}
                                docker push ${IMAGE_NAME}/cicd-app:latest
                                echo "✅ Image pushed successfully"
                            '''
                        } else {
                            bat '''
                                docker push %IMAGE_NAME%/cicd-app:%BUILD_NUMBER%
                                docker push %IMAGE_NAME%/cicd-app:latest
                                echo Image pushed successfully
                            '''
                        }
                    } catch (Exception e) {
                        echo "⚠️ Docker push skipped (registry not available): ${e.message}"
                    }
                }
            }
        }
        
        stage('Deploy Container') {
            steps {
                script {
                    echo "🚀 Deploying container..."
                    if (isUnix()) {
                        sh '''
                            # Stop and remove old container if exists
                            docker stop ${CONTAINER_NAME} 2>/dev/null || true
                            docker rm ${CONTAINER_NAME} 2>/dev/null || true

                            # Run new container
                            docker run -d \
                                --name ${CONTAINER_NAME} \
                                -p ${HOST_PORT}:${CONTAINER_PORT} \
                                ${IMAGE_NAME}/cicd-app:latest

                            # Wait for container to be ready
                            sleep 3

                            # Check if container is running
                            if docker inspect -f '{{.State.Running}}' ${CONTAINER_NAME} | grep -Fxq true; then
                                echo "✅ Container deployed successfully"
                            else
                                echo "❌ Container failed to start"
                                docker logs ${CONTAINER_NAME}
                                exit 1
                            fi
                        '''
                    } else {
                        bat '''
                            docker stop %CONTAINER_NAME% 2>NUL
                            docker rm %CONTAINER_NAME% 2>NUL

                            docker run -d ^
                                --name %CONTAINER_NAME% ^
                                -p %HOST_PORT%:%CONTAINER_PORT% ^
                                %IMAGE_NAME%/cicd-app:latest

                            timeout /t 3 /nobreak >NUL

                            docker inspect -f "{{.State.Running}}" %CONTAINER_NAME% | findstr /C:"true" >NUL
                            if errorlevel 1 (
                                echo Container failed to start
                                docker logs %CONTAINER_NAME%
                                exit /b 1
                            ) else (
                                echo Container deployed successfully
                            )
                        '''
                    }
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "🏥 Running health check..."
                    if (isUnix()) {
                        sh '''
                            for i in {1..10}; do
                                if curl -f http://localhost:${HOST_PORT}/ > /dev/null 2>&1; then
                                    echo "✅ Application is healthy and responding"
                                    exit 0
                                fi
                                echo "Waiting for application to be ready... (attempt $i/10)"
                                sleep 2
                            done
                            echo "❌ Health check failed"
                            exit 1
                        '''
                    } else {
                        bat '''
                            powershell -NoProfile -Command "$max = 10; for ($i = 1; $i -le $max; $i++) { try { $response = Invoke-WebRequest -Uri ('http://localhost:' + $env:HOST_PORT + '/') -UseBasicParsing -TimeoutSec 5; if ($response.StatusCode -eq 200) { Write-Host 'Application is healthy and responding'; exit 0 } } catch { } Write-Host ('Waiting for application to be ready... (attempt ' + $i + '/10)'); Start-Sleep -Seconds 2 }; Write-Host 'Health check failed'; exit 1"
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "🔧 Cleaning up workspace..."
// cleanWs()  // Disabled for container compatibility
            }
        }
        success {
            echo "✅ Pipeline completed successfully!"
            // Add notifications here (email, Slack, etc.)
        }
        failure {
            echo "❌ Pipeline failed! Check logs above for details."
            // Add notifications here
        }
    }
}
