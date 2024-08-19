from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv

app = FastAPI()

# Load bad words from dataset
def load_bad_words():
    bad_words = set()
    try:
        # Load English bad words
        with open('datasets/english.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                bad_words.add(row[0].strip().lower())

        # Load French bad words
        with open('datasets/french.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                bad_words.add(row[0].strip().lower())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading bad words dataset: {e}")
    return bad_words

bad_words_set = load_bad_words()

# Define input model
class TextInput(BaseModel):
    title: str
    content: str

# Check if the input text contains any bad words
def contains_bad_words(text):
    words = text.lower().split()
    return any(word in bad_words_set for word in words)

@app.post("/detect")
async def detect_bad_words(input: TextInput):
    title_has_bad_words = contains_bad_words(input.title)
    content_has_bad_words = contains_bad_words(input.content)

    return {
        "title_contains_bad_words": title_has_bad_words,
        "content_contains_bad_words": content_has_bad_words
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)

