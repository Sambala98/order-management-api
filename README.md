![CI](https://github.com/Sambala98/order-management-api/actions/workflows/ci.yml/badge.svg)

# Order Management API

A production-style **FastAPI backend** demonstrating authentication, RBAC, database migrations, Dockerization, automated testing, and CI/CD integration.

This project demonstrates practical backend engineering patterns used in real-world API systems.

---

##  Features

- Health Check Endpoint
- User Registration
- User Login (JWT Authentication)
- Role-Based Access Control (RBAC)
- Protected Order APIs
- PostgreSQL Database
- Alembic Database Migrations
- Dockerized Setup
- Pytest Unit Tests
- GitHub Actions CI Pipeline
- Rate Limiting
- Structured Logging & Middleware

---

##  Example API Usage

### 1️ Register User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456"}'
```

### 2️ Login User

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456"}'
```

### 3️ Create Order (JWT Required)

```bash
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer <PASTE_YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Sudheer","item_name":"Keyboard","quantity":2}'
```

### 4️ Update Order Status

```bash
curl -X PATCH http://localhost:8000/orders/1 \
  -H "Authorization: Bearer <PASTE_YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"status":"SHIPPED"}'
```

---

##  Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (ORM)**
- **Pydantic**
- **Passlib (bcrypt hashing)**
- **Alembic**
- **Docker & Docker Compose**
- **Pytest**
- **GitHub Actions**

---

##  System Architecture

```mermaid
flowchart LR
    Client[Client] -->|HTTP Request| API[FastAPI]
    API -->|SQLAlchemy ORM| DB[(PostgreSQL)]
    API -->|JWT Auth| PR[Protected Routes]
```

---

##  Authentication Flow

### 1️ Registration Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>API: POST /auth/register
    API->>API: Hash password (bcrypt)
    API->>DB: Save user
    DB-->>API: Success
    API-->>Client: 201 Created
```

---

### 2️ Login Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant DB

    Client->>API: POST /auth/login
    API->>DB: Fetch user
    API->>API: Verify password
    API-->>Client: Return JWT token
```

---

### 3️ Access Protected Route

```mermaid
sequenceDiagram
    participant Client
    participant API

    Client->>API: GET /orders (Bearer Token)
    API->>API: Validate JWT
    API-->>Client: Return Orders Data
```

---

##  Project Structure

```
order-management-api/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       └── orders.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── models.py
│   │   └── session.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   └── orders.py
│   │
│   └── main.py
│
├── tests/
├── alembic/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── pytest.ini
```

---

##  Running Tests

### Local

```bash
pytest
```

### Docker

```bash
docker compose up -d --build
docker compose exec api pytest
```

---

##  Environment Setup

### 1️ Copy example environment file

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### 2️ Update `.env` values

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ordersdb
JWT_SECRET=supersecretkey
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## ▶ Run Application

### Local (without Docker)

```bash
uvicorn app.main:app --reload
```

Access Swagger UI:

http://localhost:8000/docs

---

##  CI Pipeline

GitHub Actions automatically:

- Spins up PostgreSQL service
- Installs dependencies
- Runs Alembic migrations
- Executes tests
- Validates pull requests

---

##  Roadmap

- Add Redis caching
- Add full Order status lifecycle
- Add async background tasks (Celery / RQ)
- Add Kubernetes deployment
- Deploy to cloud (Render / Railway / AWS)

---

##  Production Considerations

This project incorporates backend engineering best practices:

- Stateless JWT-based authentication
- Role-Based Access Control (RBAC)
- Search and pagination for scalable queries
- Rate limiting to prevent brute-force login attacks
- Environment-based configuration management
- Version-controlled database schema migrations (Alembic)
- Containerized deployment using Docker Compose
- Automated test validation through CI pipeline

These patterns reflect real-world backend systems used in production environments.

---

## AWS EC2 Deployment

This project was deployed on an AWS EC2 Amazon Linux 2023 instance using a cost-conscious AWS setup.

### Deployment Architecture

Browser or API Client -> Nginx on port 80 -> FastAPI with Uvicorn on port 8000 -> PostgreSQL on EC2

### AWS Deployment Components

- EC2: Hosted the backend application on Amazon Linux 2023
- Nginx: Reverse proxy forwarding public HTTP traffic from port 80 to FastAPI on port 8000
- systemd: Managed FastAPI as a background service with automatic restart
- PostgreSQL: Installed locally on the EC2 instance for a cost-conscious database setup
- Alembic: Applied database migrations and created users, orders, and alembic_version tables
- Environment Variables: Used .env for DATABASE_URL and JWT_SECRET

### EC2 Service Checks

sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status fastapi

### Health Check

curl http://127.0.0.1:8000/health

Expected response:

{"status":"ok"}

### Swagger UI

http://<EC2_PUBLIC_IP>/docs

### Verified API Flow

1. GET /health returned 200 OK
2. POST /auth/register created a user
3. POST /auth/login returned a JWT access token
4. POST /orders created an order using Bearer token authorization
5. GET /orders returned the saved order from PostgreSQL

### Deployment Notes

This deployment demonstrates a cost-conscious AWS backend deployment using EC2, Nginx, systemd, PostgreSQL, and Alembic migrations. The setup validates a complete API workflow including authentication, JWT authorization, order creation, and database persistence. Future improvements include HTTPS, domain configuration, centralized secrets management, automated deployment, and expanded monitoring.
