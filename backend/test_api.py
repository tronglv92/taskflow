from fastapi import FastAPI

app = FastAPI(title="TaskFlow Test API")

@app.get("/")
def read_root():
    return {"message": "TaskFlow backend is working!", "status": "success"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "taskflow-backend"}

