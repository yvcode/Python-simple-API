from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running on OpenShift!"}

if __name__ == "__main__":
    # Binding to 0.0.0.0 is critical for containers to receive outside traffic
    uvicorn.run(app, host="0.0.0.0", port=8080)
