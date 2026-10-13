from fastapi import FastAPI

app = FastAPI(title="Testo app for K8s")

@app.get("/")
def root():
    return {"message": "Hello from FastAPI on K8s"}

@app.get("/health")
def health():
    return {"status":"ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)