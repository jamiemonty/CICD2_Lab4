# app/main.py
from fastapi import FastAPI, HTTPException, status
from .schemas import User

app = FastAPI()
users: list[User] = []

@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
           return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user

@app.put("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, updated_user: User):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users[i] = updated_user
            return updated_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, deleted_user: User):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users.pop(i)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {user_id} not found")

@app.get("/health")
def health_status():
    return {"status":"OK"}

#@app.get("/hello")
#def hello():
#    return {"message": "Hello World!"}

#Where do validation errors (422) come from in FastAPI + Pydantic?
#Validation errors come from pydantic automatically validating the request body sent, if variable is different it causes an error.

#Why is returning 201 for create (POST) and 404 for missing resources important?
#Because 201 is the official code for create, tells the client the POST req worked. Same with 404, it is the official code for 
#resource not found (valid request but something is not there)

#How will this project layout help when we add a database and tests later?
#The current layout has all the necessary app logic, schemas, database code, and tests organised and able
#for swapping.