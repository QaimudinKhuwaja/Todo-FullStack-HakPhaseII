# #backend/app/main.py
# from app.api.endpoints import health, users, auth, protected, tasks
# from fastapi import FastAPI
# from app.core.db import create_db_and_tables
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     # Ensure database tables (and missing columns) exist before handling requests
#     create_db_and_tables()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "https://todo-full-stack-hak-phase-ii.vercel.app",
    
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(health.router)
# app.include_router(users.router)
# app.include_router(auth.router)
# app.include_router(protected.router)
# app.include_router(tasks.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Todo API")

# CORS - MUST be BEFORE any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://todo-full-stack-hak-phase-ii.vercel.app",
        "https://*.vercel.app",
        "*",  # Temporary - for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Import and include routers AFTER middleware
from app.api.endpoints import health, users, auth, protected, tasks

app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(protected.router, tags=["Protected"])
app.include_router(users.router, tags=["Users"])
app.include_router(tasks.router, tags=["Tasks"])



@app.get("/")
async def root():
    return {"message": "Hello World"}
