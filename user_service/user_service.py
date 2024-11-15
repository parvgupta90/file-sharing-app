from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# JWT configuration
SECRET_KEY = "jtUHX6TPf9se0wtbd5fkEjG5oK7wcyGdO-d11LnA-zg"
ALGORITHM = "HS256"

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory "database" for demonstration (use a real database in production)
users_db = {
    "exampleUser": {
        "username": "exampleUser",
        "hashed_password": pwd_context.hash("examplePassword") ,
        "full_name": "Example User" # Store hashed password
    },
    "exampleUser2": {
        "username": "exampleUser2",
        "hashed_password": pwd_context.hash("12345") ,
          "full_name": "Example User 2" # Store hashed password
    }
}

# User data model for login
class UserLogin(BaseModel):
    username: str
    password: str

# User data model for registration
class UserRegister(BaseModel):
    username: str
    password: str
    full_name: str

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to generate JWT token
def generate_jwt_token(username: str):
    payload = {
        "sub": username,
        "username": username,
        "role": "user",
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expiration time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Endpoint to handle user registration
@app.post("/register/")
async def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)
    users_db[user.username] = {
        "username": user.username,
        "full_name": user.full_name,
        "hashed_password": hashed_password
    }
    return {"message": "User registered successfully"}

# Endpoint to handle user login and generate JWT token
@app.post("/login/")
async def login(user: UserLogin):
    if user.username in users_db and verify_password(user.password, users_db[user.username]["hashed_password"]):
 
        # Generate JWT token
        full_name = users_db[user.username].get("full_name", "User")

        token = generate_jwt_token(user.username)
        return {"token": token , "full_name": full_name}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
