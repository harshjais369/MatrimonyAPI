from fastapi import FastAPI
from app.configs.users_sql import addUser_sql, getUser_sql, getAllUsers_sql, deleteUser_sql

app = FastAPI(title="Matrimony API Service", description="API for matrimonial app", version="1.0.0")

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Hello World"
    }

@app.get("/profile/all")
async def getAllUsers():
    users = getAllUsers_sql()
    if not users:
        return {
            "status": "failed",
            "message": "No profiles/users found in database",
            "data": []
        }
    for user in users:
        del user.password
    return {
        "status": "success",
        "data": users
    }

@app.get("/profile/search/{mobile}")
async def getUser(mobile: int):
    user = getUser_sql(str(mobile))
    if not user:
        return {
            "status": "failed",
            "message": "Profile/user not found",
            "data": {}
        }
    return {
            "status": "success",
            "data": user
        }

@app.post("profile/create")
async def register(mobile: str, name: str, age: str, gender: str, location: str, password: str):
    if getUser_sql(mobile):
        return {
            "status": "failed",
            "message": "Mobile number is registered already with another user!"
        }
    if not addUser_sql(mobile, name, age, gender, location, password):
        return {
            "status": "failed",
            "message": "Failed to add profile!"
        }
    return {
        "status": "success",
        "message": "User profile created successfully!"
    }

@app.post("profile/login")
async def login(mobile: str, password: str):
    user = getUser_sql(mobile)
    if not user:
        return {
            "status": "failed",
            "message": "Mobile number is not valid/found on server. Please register first!"
        }
    if user.password != password:
        return {
            "status": "failed",
            "message": "Incorrect password!"
        }
    del user.password # Don't send password to client
    return {
        "status": "success",
        "message": "Login successful!",
        "data": user
    }

@app.post("profile/delete")
async def delete(mobile: str):
    if not getUser_sql(mobile):
        return {
            "status": "failed",
            "message": "Mobile number is not valid/found on server. Please register first!"
        }
    if not deleteUser_sql(mobile):
        return {
            "status": "failed",
            "message": "Failed to delete profile!"
        }
    return {
        "status": "success",
        "message": "User profile deleted successfully!"
    }
