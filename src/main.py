import uvicorn
from fastapi import FastAPI
from src.api.users import router as router_users
from src.api.books import router as router_books

app = FastAPI()

app.include_router(router_users)
app.include_router(router_books)

if __name__ == "__main__":
    uvicorn.run(app)

