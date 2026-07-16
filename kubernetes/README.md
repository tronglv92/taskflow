# Kubernetes Manifests

Real, evolving Kubernetes deployment definitions for TaskFlow, the same way
`backend/` and `frontend/` are one evolving application codebase rather than
being split per-week. As the app grows across the bootcamp, these manifests
grow with it instead of being replaced by a new set each week.

```
kubernetes/
├── backend-deployment.yaml     # taskflow-backend Deployment (2 replicas)
├── backend-service.yaml        # ClusterIP Service, port 8000
├── backend-configmap.yaml      # non-secret backend env vars
├── backend-secret.yaml         # DATABASE_URL / SECRET_KEY (placeholder values)
├── postgres-statefulset.yaml   # postgres:15-alpine StatefulSet + headless Service
├── frontend-deployment.yaml    # taskflow-frontend Deployment (2 replicas)
└── frontend-service.yaml       # ClusterIP Service, port 80
```

## What's here today (Week 8: Kubernetes Fundamentals)

Deployments, Services, a ConfigMap, a Secret, and a Postgres StatefulSet for
the app as it exists today. Images are built locally (`taskflow-backend:1.0.0`,
`taskflow-frontend:1.0.0`) and loaded into Minikube (`imagePullPolicy: Never`)
- there's no registry push step yet.

The Postgres StatefulSet is provisioned ahead of any code that uses it, same
as the `db` service in `docker-compose.yml`. The backend has no database
client code yet (`/api/v1/status` reports `"database": {"status":
"not_configured"}`) - that's explicit future-week work.

`backend-secret.yaml` ships with obvious placeholder values. Every
environment (a student's Minikube, staging, prod) is expected to generate
and apply its own `DATABASE_URL` and `SECRET_KEY` rather than reuse what's
committed here.

## What's next

- **Week 9 (Kubernetes Intermediate)**: Ingress, HPA, and resource tuning
  beyond the flat requests/limits set here.
- **Week 16 (GitOps/ArgoCD)**: These manifests become the source an ArgoCD
  Application watches, instead of being applied by hand with `kubectl apply`.

## Applying locally

```
kubectl apply -f kubernetes/
```
