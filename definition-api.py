import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
#for saving the history of words and their meanings
from typing import List, Optional
from datetime import datetime
import json

app = FastAPI(title="Local LLM Word Definition API",
    description="Returns the meaning of a word using a locally running LLM"
)

#mounting the static folder (attaching static items to the API)
app.mount("/static", StaticFiles(directory="static"), name="static")

SAVED_FILE = "words_history.json"

# Load at startup
try:
    with open(SAVED_FILE, "r") as f:
        savedWordsList = json.load(f)
except FileNotFoundError:
    savedWordsList = []

def persist_words():
    with open(SAVED_FILE, "w") as f:
        json.dump(savedWordsList, f, indent=4)



OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

savedWordsList = []

class WordRequest(BaseModel):
    word:str

class MeaningRequest(BaseModel):
    word:str
    meaning: str
    usage: str

class SavedWords(BaseModel):
    word: str
    meaning: str
    usage: str
    saved_at: Optional[str] = None
    
# Redirect root to the HTML interface
@app.get("/")
async def root():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/static/index.html" />
    </head>
    <body>
        <p>Redirecting to <a href="/static/index.html">Word Definition Interface</a>...</p>
    </body>
    </html>
    """)    
    

@app.post("/meaning", response_model= MeaningRequest)
def get_word_meaning(request: WordRequest):
    """
    Get the meaning of a word with an example usage sentence.
    """
    # prompt tfor output
    prompt = (
        f"Provide the meaning of the word '{request.word}' in a clear, concise way. "
        f"Then give a short example sentence showing how to use this word. "
        f"Format your response exactly like this:\n"
        f"Meaning: [definition]\n"
        f"Example: [sentence]"
    )
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.3,  # Lower temperature = more focused, deterministic output
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        output = result.get("response", "").strip()
        
        # Parse the structured response
        meaning = ""
        usage = ""
        lines = output.split("\n")
        for line in lines:
            if line.lower().startswith("meaning:"):
                meaning = line.replace("Meaning:", "").strip()
            elif line.lower().startswith("example:"):
                usage = line.replace("Example:", "").strip()
        
        # Fallback: if parsing fails, use the entire response
        if not meaning:
            meaning = output
        
        return MeaningRequest(
            word=request.word,
            meaning=meaning,
            usage=usage
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama is not running. Please start it with: ollama serve"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/health")
def health_check():
    """Check if OLLAMA is still running."""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        return {"status": "healthy", "ollama": response.status_code == 200}
    except:
        return {"status": "unhealthy", "ollama": False}
        

@app.post("/save_word") 
def save_word(request: MeaningRequest):
    """
    Save the word, its meaning, and usage to a local JSON file.
    """
    # Check if word already exists
    for existing in savedWordsList:
        if existing["word"].lower() == request.word.lower():
            raise HTTPException(
                status_code=400,
                detail=f"Word '{request.word}' is already saved!"
            )
    
    word_entry = {
        "word": request.word,
        "meaning": request.meaning,
        "usage": request.usage,
        "timestamp": datetime.now().isoformat()
    }
    savedWordsList.append(word_entry)
    persist_words()
    return {
        "message": f"Word '{request.word}' saved successfully!",
        "word": word_entry
    }
    
@app.get("/saved_words", response_model=List[SavedWords])
async def get_all_words():
    """
    Retrieve all words in the database.
    """
    return savedWordsList

# Delete a saved word
@app.delete("/delete_word/{word}")
def delete_word(word: str):
    """
    Delete a saved word.
    """
    global savedWordsList
    # Find and remove the word (case-insensitive)
    original_length = len(savedWordsList)
    savedWordsList = [w for w in savedWordsList if w["word"].lower() != word.lower()]
    if len(savedWordsList) == original_length:
        raise HTTPException(status_code=404, detail=f"Word '{word}' not found")
  
    return {"message": f"Word '{word}' deleted successfully!"}

# Clear all saved words
@app.delete("/clear_all")
def clear_all_words():
    """
    Clear all saved words.
    """
    global savedWordsList
    count = len(savedWordsList)
    savedWordsList = []
    return {"message": f"Cleared {count} saved words"}
    

    