# 🚀 Flask Task Manager | Docker, AWS EC2 & CI/CD

A containerized Task Manager application built using **Python Flask and PostgreSQL**, deployed on **AWS EC2** using Docker Compose, Nginx and an automated CI/CD pipeline with GitHub Actions.

The project demonstrates containerization, infrastructure deployment, Docker image management, reverse proxy configuration and automated application deployment.

---

## 📌 Project Overview

This project demonstrates how to containerize and deploy a Flask application using a multi-container architecture.

The application uses PostgreSQL for persistent data storage, Nginx as a reverse proxy and Docker Compose to manage all application services.

A GitHub Actions CI/CD pipeline automates the build, push and deployment process whenever new code is pushed to the `main` branch.

## 🏗️ Architecture

```text
                 Developer
                     |
                     | Git Push
                     v
              GitHub Repository
                     |
                     v
             GitHub Actions CI/CD
                     |
             +-------+-------+
             |       |       |
             v       v       v
           Build    Push   Deploy
                     |
                     v
                 Docker Hub
                     |
                     v
                  AWS EC2
                     |
                     v
                Nginx :80
                     |
                     v
                Flask :5000
                     |
                     v
              PostgreSQL :5432
                     |
                     v
               Docker Volume
```

## 🛠️ Technologies Used

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Application development            |
| Flask          | Backend web framework              |
| PostgreSQL     | Relational database                |
| Gunicorn       | Python WSGI application server     |
| Docker         | Application containerization       |
| Docker Compose | Multi-container orchestration      |
| Nginx          | Reverse proxy                      |
| Git & GitHub   | Version control                    |
| GitHub Actions | CI/CD automation                   |
| Docker Hub     | Docker image registry              |
| AWS EC2        | Cloud deployment                   |
| Ubuntu         | Server operating system            |
| Ansible        | Infrastructure automation practice |

## 📂 Project Structure

```text
flask-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env.flask
├── .env.postgres
│
├── nginx/
│   └── nginx.conf
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── about.html
│
├── static/
│   └── style.css
│
└── .github/
    └── workflows/
        └── cicd.yaml
```

**Note:** Environment files containing actual credentials are excluded from Git using `.gitignore`.

## 🐳 Docker Implementation

The application is divided into three independent containers.

### 1. Flask Container

- Runs the Flask application using Gunicorn.
- Uses a custom Docker image based on Python Alpine.
- Runs as a non-root user for improved container security.
- Exposes port `5000` internally.

### 2. PostgreSQL Container

- Uses the official PostgreSQL Docker image.
- Stores application data in a named Docker volume.
- Uses environment variables for database configuration.
- Includes a health check using `pg_isready`.

### 3. Nginx Container

- Acts as a reverse proxy.
- Receives incoming HTTP requests on port `80`.
- Forwards requests to the Flask application on port `5000`.

## 🔐 Container Security

Implemented basic container security practices:

- Created a dedicated non-root user inside the Flask container.
- Used `USER appuser` to avoid running the application as root.
- Used `.dockerignore` to exclude unnecessary files from the Docker build context.
- Excluded environment files containing credentials from Git.
- Kept PostgreSQL inaccessible directly from the public internet.

## 🔄 CI/CD Pipeline

Implemented an automated CI/CD pipeline using GitHub Actions with three jobs.

### 1. Build Stage

Triggered when code is pushed or a pull request is created against the `main` branch.

- Checks out the source code.
- Sets up Python 3.10.
- Installs application dependencies.
- Performs Python syntax validation using `py_compile`.

### 2. Push Stage

Runs after a successful build and only for push events.

- Authenticates with Docker Hub using GitHub Secrets.
- Sets up Docker Buildx.
- Builds the Flask Docker image.
- Pushes the image to Docker Hub.
- Uses the Git commit SHA as the Docker image tag.

Example:

```text
deanalemao/flask-task:<commit-sha>
```

### 3. Deploy Stage

Runs after the successful image push.

- Connects to AWS EC2 using SSH.
- Fetches the latest repository updates.
- Synchronizes the EC2 working directory with `origin/main`.
- Sets the Docker image tag using the Git commit SHA.
- Pulls the updated Docker image.
- Deploys the application using Docker Compose.
- Verifies running containers.

### CI/CD Workflow

```text
Developer pushes code
         |
         v
   GitHub Actions
         |
         v
    Build Stage
         |
         v
    Push Stage
         |
         v
     Docker Hub
         |
         v
    Deploy Stage
         |
         v
      AWS EC2
         |
         v
  Docker Compose Pull
         |
         v
  Docker Compose Up
         |
         v
 Application Updated
```

## ☁️ AWS EC2 Deployment

The application is deployed on an Ubuntu EC2 instance.

### Deployment Configuration

- EC2 instance running Ubuntu.
- Docker Engine installed.
- Docker Compose plugin installed.
- Git installed.
- Nginx exposed through port `80`.
- SSH access configured for deployment.

### Security Group Configuration

| Type | Port | Purpose                   |
| ---- | ---: | ------------------------- |
| SSH  |   22 | Remote server access      |
| HTTP |   80 | Public application access |

PostgreSQL port `5432` and Flask port `5000` are not exposed publicly.

## 🚀 Running the Project Locally

### Prerequisites

- Docker
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Deanalemao/flask-app.git

cd flask-app
```

### 2. Configure environment variables

Create `.env.flask` and `.env.postgres`.

### 3. Build and start containers

```bash
docker compose up -d --build
```

### 4. Check running containers

```bash
docker compose ps
```

### 5. View application logs

```bash
docker compose logs -f
```

### 6. Access the application

Open your browser:

```text
http://localhost
```

## 🧪 Verification and Testing

The following commands were used to verify the deployment:

```bash
# Check running containers
docker ps

# Check Docker Compose services
docker compose ps

# View application logs
docker compose logs

# Check application response
curl -I http://localhost

# Check Docker images
docker images

# Check PostgreSQL health
docker compose exec postgres pg_isready -U taskuser -d taskmanager
```

The application was also tested through the EC2 public IP to verify external HTTP access and application functionality.

## 📈 Key Learnings

Through this project, I gained practical experience in:

- Containerizing Python applications using Docker.
- Creating and managing multi-container environments.
- Configuring Docker networks and persistent volumes.
- Running applications with non-root container users.
- Configuring Nginx as a reverse proxy.
- Managing environment variables and application secrets.
- Automating Docker image builds and deployments using GitHub Actions.
- Publishing versioned Docker images to Docker Hub.
- Deploying applications on AWS EC2.
- Using SSH for automated remote deployments.
- Understanding CI/CD workflows and deployment automation.

## 🔮 Future Improvements

- Implement HTTPS using Let's Encrypt and Certbot.
- Add automated application and integration tests.
- Introduce monitoring using Prometheus and Grafana.
- Implement automated backups for PostgreSQL.
- Use Ansible for repeatable EC2 provisioning.
- Store sensitive credentials using AWS Secrets Manager.

## 👨‍💻 Author

**Dean Alemao**

MSc Information Technology Student | DevOps & Cloud Enthusiast

- GitHub: [Deanalemao](https://github.com/Deanalemao)

---

⭐ If you found this project useful, feel free to explore the repository and provide feedback.
