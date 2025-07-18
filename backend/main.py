from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

# --- Configuration ---
SECRET_KEY = "a_very_secret_key_for_jwt" # In a real app, this comes from environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- App Initialization ---
app = FastAPI()

# --- Security & Hashing Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Dummy Database ---
# In a real app, this would be a real database connection.
fake_users_db = {
    "user@example.com": {
        "username": "user@example.com",
        "full_name": "Example User",
        "hashed_password": pwd_context.hash("password123"),
        "disabled": False,
    }
}

# --- Helper Functions ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    # In a real app, you would add an expiry time.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- API Endpoints ---
@app.get("/api")
def read_root():
    return {"message": "Welcome to the dkloud Backend API"}

# This endpoint is what the login form would call.
# NOTE: For Netlify deployment, this path might need to be /api/token
@app.post("/api/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Placeholder for getting user's documents
@app.get("/api/documents")
async def get_documents():
    # In a real app, we would get documents for the logged-in user.
    return [
        {"id": 1, "name": "PAN Card", "date": "Jul 19, 2025"},
        {"id": 2, "name": "Aadhaar Card", "date": "Jul 18, 2025"},
    ]

# This is a catch-all for any other path to say hello
@app.get("/api/{full_path:path}")
def say_hello(full_path: str):
    return {"message": f"Hello from the API at path: {full_path}"}
