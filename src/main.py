import uvicorn
from fastapi import FastAPI
from src.api.users import router as router_users

app = FastAPI()

app.include_router(router_users)

if __name__ == "__main__":
    uvicorn.run(app)

