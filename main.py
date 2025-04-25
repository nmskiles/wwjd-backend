
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import uvicorn

app = FastAPI()

# Replace this with your real OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_jesus(request: QuestionRequest):
    prompt = f"You are Jesus with a modern, humorous tone. Based on the Bible, answer the question: '{request.question}' in a casual and funny way."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Jesus responding in a humorous but biblically-rooted tone."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return {"answer": response['choices'][0]['message']['content']}
    except Exception as e:
        return {"answer": f"Oops. Even the Lord needs a stable API connection. Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
