# TaskFlow - Platform Engineering Bootcamp Reference Application

TaskFlow is a task management platform that students build throughout the 20-week Platform Engineering Bootcamp. This application evolves from a simple FastAPI backend to a fully deployed, production-ready system with CI/CD, monitoring, and GitOps.

## What is TaskFlow?

TaskFlow is a modern task management application designed to help teams organize, track, and complete work efficiently. Think of it as a simplified version of Jira or Asana, built specifically for learning platform engineering concepts.

### Core Features (Built Throughout Bootcamp)

**Weeks 1-6: Foundation**
- Basic task CRUD operations
- User authentication
- Simple REST API
- Local development environment

**Weeks 7-12: Infrastructure**
- Containerized deployment
- Database integration (PostgreSQL)
- Basic CI/CD pipeline
- Kubernetes deployment

**Weeks 13-18: Advanced Platform**
- Python automation scripts
- Infrastructure as Code (Terraform/Crossplane)
- Advanced CI/CD with GitOps
- Monitoring and observability

**Weeks 19-20: Production Ready**
- Multi-environment deployment
- Security hardening
- Performance optimization
- Complete platform engineering portfolio

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **ORM**: SQLAlchemy
- **API Documentation**: OpenAPI/Swagger

### Frontend
- **Framework**: Vue.js 3
- **State Management**: Pinia
- **Routing**: Vue Router
- **UI Components**: Tailwind CSS
- **Build Tool**: Vite

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions → ArgoCD (GitOps evolution)
- **IaC**: Terraform (Week 7-9), Crossplane (Week 10-12)
- **Monitoring**: Prometheus + Grafana
- **Service Mesh**: Consul (Week 8-9)

### Development Tools
- **Version Control**: Git + GitHub
- **Local Development**: Docker Compose
- **API Testing**: Postman/Thunder Client
- **Code Quality**: Ruff, Black, ESLint

## Project Structure

```
TaskFlow/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container image
│
├── frontend/               # Vue.js frontend application
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── stores/         # Pinia stores
│   │   └── router/         # Vue Router config
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container image
│
├── infrastructure/         # Infrastructure as Code
│   ├── terraform/          # Terraform configurations
│   ├── kubernetes/         # K8s manifests
│   ├── crossplane/         # Crossplane compositions
│   └── helm/               # Helm charts
│
├── docs/                   # Project documentation
│   ├── architecture/       # Architecture diagrams
│   ├── api/                # API documentation
│   └── deployment/         # Deployment guides
│
├── .github/
│   └── workflows/          # CI/CD pipelines
│
├── docker-compose.yml      # Local development environment
└── README.md              # This file
```

## Learning Journey

### Week 1: Vision & Planning
Students envision TaskFlow's features, create documentation, and plan the architecture.

**Projects**:
- 1.5: Envision TaskFlow Platform
- 1.6: TaskFlow Documentation
- 1.7: TaskFlow Architecture
- 1.8: TaskFlow Planning

### Week 2: Development Environment
Students set up their local development environment and create the initial codebase.

**Projects**:
- 2.3: TaskFlow Dev Environment
- 2.4: TaskFlow Git Setup
- 2.5: FastAPI Scaffold

### Week 3: First Deployment
Students create their first CI/CD pipeline and deploy to a development environment.

**Projects**:
- 3.4: TaskFlow CI/CD Pipeline
- 3.5: TaskFlow First Deployment

### Weeks 4-18: Progressive Enhancement
Each week adds new platform engineering capabilities to TaskFlow, building a complete production system.

### Weeks 19-20: Capstone
Students deploy TaskFlow as a production-ready platform with all enterprise features.

## Getting Started (Week 2)

### Prerequisites
- Linux environment (Ubuntu 22.04+)
- Docker and Docker Compose
- Git
- Python 3.11+
- Node.js 18+

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/taskflow.git
cd taskflow

# Start development environment
docker-compose up -d

# Backend will be available at http://localhost:8000
# Frontend will be available at http://localhost:5173
# API docs at http://localhost:8000/docs
```

### Development Setup

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

## Core Entities

### Task
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "status": "todo|in_progress|done",
  "priority": "low|medium|high",
  "assignee_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime",
  "due_date": "datetime"
}
```

### User
```json
{
  "id": "uuid",
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "user|admin",
  "created_at": "datetime"
}
```

## API Endpoints (Initial Version)

### Health & Status
- `GET /health` - Health check
- `GET /api/v1/status` - API status

### Authentication (Week 4+)
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Tasks
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get task details
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

### Users (Week 4+)
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user

## Platform Engineering Skills Learned

By building TaskFlow, students will master:

1. **Application Development**: FastAPI, Vue.js, RESTful APIs
2. **Containerization**: Docker, Docker Compose, multi-stage builds
3. **Orchestration**: Kubernetes, Helm, service mesh
4. **CI/CD**: GitHub Actions, GitOps, ArgoCD
5. **Infrastructure as Code**: Terraform, Crossplane
6. **Monitoring**: Prometheus, Grafana, logging
7. **Security**: Authentication, secrets management, RBAC
8. **Automation**: Python scripting, workflow automation
9. **Networking**: Load balancing, ingress, service discovery
10. **Production Operations**: Scaling, updates, rollbacks

## Portfolio Value

TaskFlow becomes the centerpiece of the student's GitHub portfolio, demonstrating:
- Full-stack development skills
- Modern DevOps practices
- Cloud-native architecture
- Production deployment experience
- Complete platform engineering lifecycle

## Contributing

This is a learning project. Students will fork this repository and build their own version of TaskFlow throughout the bootcamp.

## License

MIT License - Created for educational purposes by TeKanAid Academy

## Support

Questions? Join the bootcamp community or check the documentation in `/docs`.

---

**Start Building Your Platform Engineering Career with TaskFlow** 🚀
