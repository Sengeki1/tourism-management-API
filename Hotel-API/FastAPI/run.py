from app.main import app
from fastapi import FastAPI

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app , host="127.0.0.1", port=3000)
