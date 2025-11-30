from fastapi import FastAPI
from pydantic import BaseModel
from answer_checker.compare import answers_match
from fastapi.middleware.cors import CORSMiddleware

class CheckRequest(BaseModel):
    original: str
    user_answer: str

app = FastAPI()

# Allow Flutter (or any localhost front-end) to call
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check")
def check_answer(req: CheckRequest):
    result = answers_match(req.original, req.user_answer)
    return {"match": result}
