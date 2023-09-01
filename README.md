# Dockerized Flask Malware Scanner Demo

This is a simple Flask web application that demonstrates how to scan uploaded files for malware using Trend Micro's CloudOne Antivirus as a Service (VSaaS). It allows you to upload files for scanning, and if malware is detected, it will display the scan results.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Docker**: You must have Docker installed on your system. If not, you can download it [here](https://docs.docker.com/get-docker/).

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/jmlake569/AMaaS_demo_app.git
cd AMaaS_demo_app
```

### 2. Build the container

```bash
docker build -t flask-malware-scanner .
```

### 3. Run the contianer

```bash
docker run -p 5000:5000 flask-malware-scanner
```

### 4. Access the application

Open your web browser and navigate to http://localhost:5000 to access the application.

![Alt text](images/malewareoneUI.png)