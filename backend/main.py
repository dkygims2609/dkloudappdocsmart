from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware # Import the CORS middleware

# --- App Initialization ---
app = FastAPI()

# --- CORS Middleware Setup ---
# This is the new section that adds the "permission" headers.
origins = [
    "*"  # For development, we allow all origins. In production, we'd restrict this.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dummy Database ---
fake_users_db = {}

# --- Pydantic Models for Data Validation ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str

# --- API Endpoints ---
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = f"fake_hashed_{user.password}"
    user_in_db = UserInDB(email=user.email, hashed_password=hashed_password)
    fake_users_db[user.email] = user_in_db
    
    print(f"New user registered: {user.email}") # This will print in your Netlify function logs.
    return {"email": user.email, "message": "User created successfully"}

# This is the 'handler' function that Netlify will use to run our app
handler = Mangum(app)
