
from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai

app = FastAPI()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_jesus(request: QuestionRequest):
    prompt = f"You are Jesus with a modern, humorous tone. Based on the Bible, answer the question: '{request.question}' in a casual and funny way."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
",
            messages=[
                {"role": "system", "content": "You are Jesus responding in a humorous but biblically-rooted tone."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        return {"answer": f"Oops. Even the Lord needs a stable API connection. Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
