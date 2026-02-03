# Todo Full-Stack Application

A full-stack todo application with user authentication built using FastAPI (backend) and Next.js (frontend).

## Features
- ✅ User Registration & Login
- ✅ JWT Authentication
- ✅ Task CRUD Operations
- ✅ Responsive UI with Tailwind CSS

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL/SQLite
- JWT Authentication

### Frontend
- Next.js 16
- TypeScript
- Tailwind CSS
- React Context API

## Setup Instructions

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./test.db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=your-jwt-algorithm-here
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
