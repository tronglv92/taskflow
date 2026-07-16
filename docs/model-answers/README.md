# Model Answers

Reference artifacts for TaskFlow labs that ask students to produce something
with no natural home elsewhere in this repo (a vision doc, a planning doc,
and similar). Organized one folder per lab:

```
docs/model-answers/week-NN-lab-slug/
```

A lab's setup script clones this repo and copies the model-answer folders
for every week up to and including its own, so a student on week N can see
every model answer published through week N.

This is for comparison artifacts only. Real application/infrastructure code
that a lab teaches students to write (Dockerfiles, Kubernetes manifests,
Terraform, etc.) lives at its natural path in this repo instead (`backend/`,
`frontend/`, `kubernetes/`, ...) and uses a stash-and-reveal pattern in the
lab's own setup script rather than living under `docs/model-answers/`.
