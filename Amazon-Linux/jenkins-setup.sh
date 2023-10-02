#!/bin/bash

# Function to install Java
install_java() {
    # Check if Amazon Linux 2023
    if [[ -f /etc/system-release && $(cat /etc/system-release) == *"Amazon Linux release 2023"* ]]; then
        echo "Detected Amazon Linux 2023"
        sudo dnf install java-17-amazon-corretto -y
    else
        echo "Not Amazon Linux 2023, checking for Amazon Linux 2"
        
        # Check if Amazon Linux 2
        if [[ -f /etc/system-release && $(cat /etc/system-release) == *"Amazon Linux release 2"* ]]; then
            echo "Detected Amazon Linux 2"
            sudo amazon-linux-extras install java-openjdk11 -y
        else
            echo "Unsupported Amazon Linux version. Please install Java manually."
            exit 1
        fi
    fi
}

# Update the system
sudo yum update -y

# Add the Jenkins repository
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo

# Import the Jenkins GPG key
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

# Upgrade packages
sudo yum upgrade -y
sudo dnf upgrade -y

# Install Java
install_java

# Install Jenkins through yum
sudo yum install jenkins -y

# Reload systemd manager configuration
sudo systemctl daemon-reload

# Enable and start Jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Print the status of Jenkins
sudo systemctl status jenkins

# Print the initial admin password
echo "Initial admin password:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword