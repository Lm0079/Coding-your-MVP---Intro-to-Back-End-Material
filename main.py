from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import random

app = FastAPI()

# Define a joke model
class Joke(BaseModel):
    id: int
    content: str

# In-memory storage for jokes
jokes: List[Joke] = [
    Joke(id=1, content="Why don't scientists trust atoms? Because they make up everything!"),
    Joke(id=2, content="What do you get when you cross a snowman and a vampire? Frostbite."),
    Joke(id=3, content="Why was the math book sad? Because it had too many problems.")
]

# GET endpoint to retrieve a random joke
@app.get("/api/joke", response_model=Joke)
async def get_joke():
    # Your code here
    return joke

# POST endpoint to add a new joke
@app.post("/api/add-joke", response_model=Joke)
async def add_joke(joke: str):
    # Your code here
    return new_joke

# DELETE endpoint to delete a joke by ID
@app.delete("/api/delete-joke/{joke_id}", response_model=Joke)
async def delete_joke(joke_id: int):
    # Your code here
    return joke
