
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
#     "https://todo-full-stack-hak-phase-ii.vercel.app",  # ← exact Vercel URL (no trailing /, no *)
#     "http://localhost:3000",  # local ke liye
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PATCH", "DELETE","OPTIONS"],
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




from app.api.endpoints import health, users, auth, protected, tasks
from fastapi import FastAPI
from app.core.db import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Todo Fullstack Backend",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI on /docs
    redoc_url=None,    # Optional: hide ReDoc if not needed
)


@app.on_event("startup")
def on_startup():
    # Ensure database tables (and missing columns) exist before handling requests
    create_db_and_tables()


# CORS config - improved for preflight & credentials
origins = [
    "https://todo-full-stack-hak-phase-ii.vercel.app",          # Exact production frontend (no trailing slash!)
    "https://todo-full-stack-hak-phase-ii-git-*.vercel.app",    # For Vercel preview/deploy branches (wildcard for git branches)
    "http://localhost:3000",                                    # Local dev
    "http://127.0.0.1:3000",                                    # Extra local variant
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,                # Must for cookies / access_token
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],  # Explicit headers for preflight safety (instead of "*")
    expose_headers=["Set-Cookie"],         # If you set cookies in responses
    max_age=86400,                         # Cache preflight for 24 hours (reduces OPTIONS calls)
)

# Include routers AFTER middleware
app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(tasks.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}