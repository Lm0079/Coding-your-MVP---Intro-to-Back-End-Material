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
    Joke(id=3, content="If Bill Gates had a dime for every time Windows crashed ... Oh wait, he does.")
]

# GET endpoint to retrieve a random joke
@app.get("/api/joke", response_model=Joke)
async def get_joke():
    if not jokes:
        raise HTTPException(status_code=404, detail="No jokes available")
    joke = random.choice(jokes)
    return joke

# POST endpoint to add a new joke
@app.post("/api/add-joke", response_model=Joke)
async def add_joke(joke: str):
    joke_id = len(jokes) + 1  # Simple ID generation
    new_joke = Joke(content=joke,id=joke_id)
    jokes.append(new_joke)
    return new_joke

# DELETE endpoint to delete a joke by ID
@app.delete("/api/delete-joke/{joke_id}", response_model=Joke)
async def delete_joke(joke_id: int):
    joke = next((j for j in jokes if j.id == joke_id), None)
    if joke is None:
        raise HTTPException(status_code=404, detail="Joke not found")
    jokes.remove(joke)
    return joke
