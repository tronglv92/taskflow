# TaskFlow Technology Stack Decisions — Model Answer

This is the real, already-decided TaskFlow stack. Every lab from Week 5
onward clones the same repository and builds directly on these choices, so
this isn't a personal preference exercise, it's the trade-off reasoning
behind the stack you'll actually be working in for the rest of the bootcamp.

## Frontend Framework

**Options considered:** Vue.js 3 | React | Angular

**Choice:** Vue.js 3.4 (with Vite)

**Why this choice over the alternatives:** Vue has the gentlest learning
curve for an early-career team, ships first-party Router and Pinia, and its
single-file components keep the codebase approachable. React has the larger
ecosystem and hiring pool, but that ecosystem means more third-party
decisions (state management, routing) for a small team to own. Angular is
more structure and a steeper learning curve than a 2-3 person team needs
this early.

**Trade-offs accepted:** A smaller hiring pool than React and fewer
enterprise-grade component libraries than Angular.

---

## Backend Framework

**Options considered:** FastAPI (Python) | Django REST Framework (Python) | Flask (Python)

**Choice:** FastAPI 0.109 (Python 3.11)

**Why this choice over the alternatives:** FastAPI gives automatic OpenAPI
docs, Pydantic validation, and async support out of the box. Django REST
Framework brings an ORM, admin site, and auth system this project doesn't
need yet, machinery that adds setup overhead before it adds value. Flask is
simpler than Django but would require assembling validation and docs
generation by hand, work FastAPI already does.

**Trade-offs accepted:** No built-in admin site or ORM (SQLAlchemy is added
separately, see `backend/requirements.txt`), and a younger ecosystem than
Django's.

---

## Database

**Options considered:** PostgreSQL | MySQL | MongoDB

**Choice:** PostgreSQL 15

**Why this choice over the alternatives:** TaskFlow data is clearly
relational (users, projects, tasks reference each other), and PostgreSQL
offers strong consistency plus JSON column support if the schema needs
flexibility later. MongoDB would fight the relational shape of the data
instead of matching it. MySQL is a reasonable relational alternative, but
PostgreSQL's feature set (window functions, JSON support, full-text search)
gives more headroom without a future database migration.

**Trade-offs accepted:** Slightly more operational care than a managed
document store, and a steeper tuning curve than MySQL for some workloads.

---

## Summary

| Layer | Choice | Primary Reason |
|-------|--------|-----------------|
| Frontend | Vue.js 3.4 | Easiest for a small early-career team |
| Backend | FastAPI 0.109 | Auto docs + validation + async, without extra machinery |
| Database | PostgreSQL 15 | Relational data with strong consistency |

Pinned versions come straight from the canonical repo: see
`backend/requirements.txt` for the backend and `frontend/package.json` for
the frontend.
