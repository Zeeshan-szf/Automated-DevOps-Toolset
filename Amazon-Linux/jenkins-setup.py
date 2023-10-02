import platform
import subprocess

# Function to install Java for Amazon Linux 2023
def install_java_amazon_linux_2023():
    print("Detected Amazon Linux 2023")
    try:
        subprocess.run(["sudo", "dnf", "install", "java-17-amazon-corretto", "-y"], check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Java: {e}")
        exit(1)

# Function to install Java for Amazon Linux 2
def install_java_amazon_linux_2():
    print("Detected Amazon Linux 2")
    try:
        subprocess.run(["sudo", "amazon-linux-extras", "install", "java-openjdk11", "-y"], check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Java: {e}")
        exit(1)

# Check the Linux distribution and version
linux_distribution = platform.linux_distribution()
if "Amazon Linux" not in linux_distribution[0]:
    print("This script is intended for Amazon Linux. Aborting.")
    exit(1)

# Check the Amazon Linux version and install Java accordingly
if "2023" in linux_distribution[1]:
    install_java_amazon_linux_2023()
elif "2" in linux_distribution[1]:
    install_java_amazon_linux_2()
else:
    print("Unsupported Amazon Linux version. Please install Java manually.")
    exit(1)

# Update the system and install Jenkins
try:
    subprocess.run(["sudo", "yum", "update", "-y"], check=True, text=True)
    subprocess.run(["sudo", "wget", "-O", "/etc/yum.repos.d/jenkins.repo", "https://pkg.jenkins.io/redhat-stable/jenkins.repo"], check=True, text=True)
    subprocess.run(["sudo", "rpm", "--import", "https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key"], check=True, text=True)
    subprocess.run(["sudo", "yum", "upgrade", "-y"], check=True, text=True)
    subprocess.run(["sudo", "yum", "install", "jenkins", "-y"], check=True, text=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while updating or installing Jenkins: {e}")
    exit(1)

# Reload systemd manager configuration and start Jenkins
try:
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True, text=True)
    subprocess.run(["sudo", "systemctl", "enable", "jenkins"], check=True, text=True)
    subprocess.run(["sudo", "systemctl", "start", "jenkins"], check=True, text=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while configuring or starting Jenkins: {e}")
    exit(1)

# Print the initial admin password
try:
    initial_password = subprocess.check_output(["sudo", "cat", "/var/lib/jenkins/secrets/initialAdminPassword"], text=True)
    print("Initial admin password:")
    print(initial_password)
except subprocess.CalledProcessError as e:
    print(f"Failed to retrieve the initial admin password: {e}")