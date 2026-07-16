# TaskFlow System Architecture — Model Answer

## Overview

TaskFlow is a task management web application. Users manage tasks through a
single-page browser frontend that talks to a REST API, which persists data in
a relational database. It targets small teams (2-3 developers) that need a
simple, reliable place to track work, and it is built to comfortably handle
100+ concurrent users on a straightforward three-tier architecture.

## Components

### Frontend

**Technology choice:** Vue 3 (with Vite as the build tool)

**Why this choice:** Vue has the gentlest learning curve of the major
frontend frameworks, which matters for a small team that includes
early-career engineers. It ships first-party Router and Pinia (state
management) instead of forcing a search through third-party options, and its
single-file components keep the codebase approachable for people new to the
framework. React was considered, it has the largest ecosystem and hiring
pool, but that ecosystem also means more decisions (which state manager,
which routing library) for a small team to make and maintain. Angular was
considered too, its batteries-included framework is more structure than a
2-3 person team needs this early, and its steeper learning curve slows down
new contributors.

**Responsibilities:**
- Render task lists, forms, and dashboards
- Validate user input before sending requests
- Call the backend REST API and update the UI reactively

### Backend API

**Technology choice:** FastAPI (Python 3.11)

**Why this choice:** FastAPI generates interactive API documentation
automatically from the code (no separate docs to maintain), uses Pydantic
for request/response validation, and supports async request handling out of
the box, all of which keep the API contract clear for a small team as it
grows. Django REST Framework was considered, it bundles an ORM, admin site,
and authentication system TaskFlow does not need this early, that machinery
adds setup overhead without adding value yet. Flask was also considered, it
is simpler than Django but leaves validation, docs generation, and async
support to be assembled by hand, work FastAPI provides natively.

**Responsibilities:**
- Expose REST endpoints for task CRUD (planned for later weeks, see the
  Project Status note in this repo's README)
- Authenticate and authorize requests
- Validate input and enforce business rules
- Read and write data through the database

### Database

**Technology choice:** PostgreSQL

**Why this choice:** Task data is clearly relational, users, projects, and
tasks reference each other, and those relationships need to stay consistent.
PostgreSQL is ACID-compliant, mature, and adds strong JSON column support if
part of the schema ever needs flexibility later. MongoDB was considered, but
a document store fights the relational shape of this data rather than
matching it, foreign-key relationships and joins are exactly what a
relational database is built for. MySQL was also considered, it is a
reasonable relational choice too, but PostgreSQL's richer feature set (window
functions, JSON support, full-text search) gives more headroom to grow into
without changing databases later.

**Responsibilities:**
- Store tasks, users, and projects
- Enforce relational integrity between them
- Serve queries for the API

## How Components Communicate

Today, before any task-management features exist, the frontend can already
reach three real backend endpoints: `GET /` (a welcome message), `GET
/health` (used by container and orchestrator health checks), and `GET
/api/v1/status` (a status probe). Once task CRUD lands, the flow for
creating a task will work like this: the browser sends an HTTP POST to the
backend API, the API validates the request body, writes a new row to
PostgreSQL inside a transaction, and returns the created task as JSON. The
frontend then updates the task list reactively so the user sees the new task
immediately.

## Non-Functional Requirements

Pull these targets from Success Metrics → Platform Performance in your own
`PLATFORM_VISION.md` (Project 1.5). If your thinking has changed now that
you're designing the actual architecture, refine them here.

**Concurrent users target:** 100+
**Expected API response time:** under 200 ms (95th percentile)
**Uptime target:** 99.9%

## Architecture Principles

1. Stateless backend, no session state stored on the server (use JWT tokens).
2. API-first design, the frontend consumes the same REST API any client would.
3. Database as the source of truth, all persistent state lives in PostgreSQL.
4. Separation of concerns, frontend, backend, and database evolve independently.
5. Security in depth, validate input, authenticate, and authorize on every request.
