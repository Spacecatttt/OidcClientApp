# OIDC Client

## About the Project
This app is an application for testing OIDC providers. You can modify all necessary settings: CLIENT_ID, CLIENT_SECRET, ISSUER_URL, SCOPES, through a minimalistic UI.

## Features
* Configure OIDC provider settings through the UI
* Test authentication flows
* View token information and claims

## Getting Started
Follow these steps to get the project up and running on your local machine.

### Prerequisites
* [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose
* [Python](https://www.python.org/) 3.13+ (optional, for testing without Docker)

---

### Installation & Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Spacecatttt/OidcClientApp.git
cd OidcClientApp
```

#### 2. Build and Run Docker Container
```bash
docker build -t oidc-client .
docker run -p 5000:5000 --add-host localhost:host-gateway oidc-client
```

#### 3. Access the Application
Open your browser and navigate to:
```
https://localhost:5000
```
