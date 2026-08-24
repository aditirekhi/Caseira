import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database.session import create_database_and_tables
from routes import (
    bookmarked_favorites_recipes,
    cart,
    category,
    helpful_reviews,
    recipe_review,
    recipes,
    regions,
    security,
    user,
    user_calendar_plan_details,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("-------------------------------- Entering lifespan")
    await create_database_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(security.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(regions.router)
app.include_router(recipes.router)
app.include_router(recipe_review.router)
app.include_router(cart.router)
app.include_router(bookmarked_favorites_recipes.router)
app.include_router(user_calendar_plan_details.router)
app.include_router(helpful_reviews.router)

origins = ["http://localhost:4200", "https://yourproductionapp.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        print(
            f"----------------------------------Entering catch_exceptions_middleware for path: {request.url.path}"
        )
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": traceback.format_exc()},
        )
