from fastapi import FastAPI, Form, HTTPException, status
from pydantic import BaseModel, EmailStr

# --- App Initialization ---
app = FastAPI()

# --- Dummy Database & Password Hashing ---
# In a real app, this would be a real database (like PostgreSQL or MongoDB).
# For now, we'll store users in a simple dictionary.
fake_users_db = {}

# --- Pydantic Models for Data Validation ---
# This ensures we receive a valid email and password.
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str

# --- API Endpoints ---

@app.get("/api")
def read_root():
    return {"message": "Welcome to the dkloud Backend API"}

# THIS IS THE CORRECTED LINE. The path is now "/register" instead of "/api/register"
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # In a real app, you would hash the password here. For now, we store it simply.
    # We are faking the hashing for this example.
    hashed_password = f"fake_hashed_{user.password}"
    
    user_in_db = UserInDB(email=user.email, hashed_password=hashed_password)
    fake_users_db[user.email] = user_in_db
    
    print(f"New user registered: {user.email}")
    print("Current DB:", fake_users_db) # This will print in your Netlify function logs.

    return {"email": user.email, "message": "User created successfully"}

# This is a catch-all for any other path to say hello
@app.get("/api/{full_path:path}")
def say_hello(full_path: str):
    return {"message": f"Hello from the API at path: {full_path}"}
