# TaskFlow Deployment Architecture — Model Answer

## Local Development

**How to start the environment:** Run `docker compose up` from the project
root. This is the real `docker-compose.yml` already committed at the root of
this repo, you'll build on it directly starting in Week 2.

**Where each component runs:**

| Component | How it runs locally |
|-----------|----------------------|
| Frontend | Vite dev server in a container on port 5173 |
| Backend API | FastAPI (Uvicorn) container on port 8000 |
| Database | PostgreSQL container on port 5432 (wired up starting Week 4; a Redis container joins the stack in Week 7 for caching and sessions) |

**Developer workflow (how code changes get picked up):** Source folders are
bind-mounted into the containers, so saving a file triggers hot reload for
both the frontend and the backend, no rebuild needed for day-to-day changes.

---

## Staging

**Purpose of this environment:** A production-like environment for
integration testing and review before release.

**Where each component runs:**

| Component | Deployment target |
|-----------|--------------------|
| Frontend | Static build served behind an ingress |
| Backend API | Kubernetes deployment |
| Database | Managed PostgreSQL service |

**How code gets deployed to staging:** Merging to the main branch triggers a
CI/CD pipeline that builds container images and deploys them automatically.

This part is genuinely future-tense right now, you haven't touched Docker or
Kubernetes yet, both show up starting around Week 7-8 of this bootcamp. The
important thing to internalize in Week 1 is the trajectory: local
development runs on Docker Compose, staging and production run on
Kubernetes. You don't need to know how yet, just that this is where the
architecture is headed.

---

## Production

**Where each component runs:**

| Component | Deployment target |
|-----------|--------------------|
| Frontend | Static build behind a CDN and ingress |
| Backend API | Kubernetes deployment with autoscaling |
| Database | Managed PostgreSQL with backups and high availability |

**How code gets deployed to production:** Creating a release tag triggers
the pipeline, which deploys after a manual approval gate.

**How a bad deployment gets rolled back:** Roll back to the previous
image/tag via the pipeline (or `kubectl rollout undo`), then restore the
database from a backup only if a migration caused the failure.
