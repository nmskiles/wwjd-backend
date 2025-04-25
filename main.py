
from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai
import requests
import re

app = FastAPI()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QuestionRequest(BaseModel):
    question: str

def extract_reference(text):
    match = re.search(r'\[(.*?)\]', text)
    return match.group(1) if match else None

def fetch_bible_verse(reference):
    try:
        formatted_ref = reference.replace(" ", "%20")
        response = requests.get(f"https://bible-api.com/{formatted_ref}")
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "").strip()
        else:
            return "Verse not found."
    except Exception as e:
        return f"Error fetching verse: {str(e)}"

@app.post("/ask")
async def ask_jesus(request: QuestionRequest):
    prompt = f"You are Jesus with a modern, humorous tone. Based on the Bible, answer the question: '{request.question}' in a casual and funny way. Include the biblical verse that supports your response at the bottom, like: [Matthew 5:9]"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jesus responding in a humorous but biblically-rooted tone. Always include the reference to the supporting Bible verse at the bottom of your response."},
                {"role": "user", "content": prompt}
            ]
        )
        answer_text = response.choices[0].message.content
        reference = extract_reference(answer_text)
        verse_text = fetch_bible_verse(reference) if reference else "No verse reference found."
        return {
            "answer": answer_text,
            "reference": reference,
            "verse_text": verse_text
        }
    except Exception as e:
        return {"answer": f"Oops. Even the Lord needs a stable API connection. Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
