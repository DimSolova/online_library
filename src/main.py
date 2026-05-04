import uvicorn
from fastapi import FastAPI

from src.api.books import router as router_books
from src.api.favorites import router as router_favorites
from src.api.reviews import router as router_reviews
from src.api.users import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_books)
app.include_router(router_reviews)
app.include_router(router_favorites)

if __name__ == "__main__":
    uvicorn.run(app)
