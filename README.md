![CI](https://github.com/Sambala98/order-management-api/actions/workflows/ci.yml/badge.svg)

# Order Management API

A production-ready backend API built using **FastAPI** and **PostgreSQL** with JWT authentication, Docker containerization, automated testing, and CI pipeline integration.

This project demonstrates real-world backend engineering practices including authentication, database integration, containerization, testing, and continuous integration.

---

##  Features

- Health Check Endpoint
- User Registration
- User Login (JWT Authentication)
- Protected Order APIs
- PostgreSQL Database
- Dockerized Setup
- Pytest Unit Tests
- GitHub Actions CI Pipeline

---
##  Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (ORM)**
- **Pydantic**
- **Passlib (bcrypt hashing)**
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

##  CI Pipeline

GitHub Actions automatically:

- Spins up PostgreSQL service
- Installs dependencies
- Runs tests
- Validates pull requests

---

## Roadmap


- Add Redis caching
- Add Order status lifecycle (PENDING → SHIPPED → DELIVERED)
- Add async background tasks (Celery / RQ)
- Add Kubernetes deployment


## Production Considerations

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