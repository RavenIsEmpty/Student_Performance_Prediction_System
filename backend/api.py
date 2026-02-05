from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from model_service import predict, load_model


app = FastAPI(title="Student Performance Prediction API")

# allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    attendance: float = Field(ge=0, le=100)
    assignment: float = Field(ge=0, le=100)
    quiz: float = Field(ge=0, le=100)
    exam: float = Field(ge=0, le=100)

@app.get("/health")
def health():
    payload = load_model()
    return {"status": "ok", "accuracy": payload.get("accuracy", None)}

@app.post("/predict")
def do_predict(req: PredictRequest):
    return predict(req.attendance, req.assignment, req.quiz, req.exam)
