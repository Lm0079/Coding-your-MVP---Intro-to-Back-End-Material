from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import random

app = FastAPI()

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('jokes.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table for jokes
cursor.execute('''
CREATE TABLE IF NOT EXISTS jokes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL
)
''')
conn.commit()

# Define a joke model
class Joke(BaseModel):
    id: int
    content: str

# Helper function to fetch a random joke
def get_random_joke():
    cursor.execute('SELECT id, content FROM jokes')
    jokes = cursor.fetchall()
    if not jokes:
        return None
    return random.choice(jokes)

# GET endpoint to retrieve a random joke
@app.get("/api/joke", response_model=Joke)
async def get_joke():
    joke = get_random_joke()
    if not joke:
        raise HTTPException(status_code=404, detail="No jokes available")
    return {"id": joke[0], "content": joke[1]}

# POST endpoint to add a new joke
@app.post("/api/add-joke", response_model=Joke)
async def add_joke(joke: str):
    cursor.execute('INSERT INTO jokes (content) VALUES (?)', (joke,))
    conn.commit()
    joke_id = cursor.lastrowid
    return {"id": joke_id, "content": joke}

# DELETE endpoint to delete a joke by ID
@app.delete("/api/delete-joke/{joke_id}", response_model=Joke)
async def delete_joke(joke_id: int):
    cursor.execute('SELECT id, content FROM jokes WHERE id = ?', (joke_id,))
    joke = cursor.fetchone()
    if joke is None:
        raise HTTPException(status_code=404, detail="Joke not found")
    cursor.execute('DELETE FROM jokes WHERE id = ?', (joke_id,))
    conn.commit()
    return {"id": joke[0], "content": joke[1]}

# Make sure to close the database connection when the app shuts down
@app.on_event("shutdown")
def shutdown_event():
    conn.close()
