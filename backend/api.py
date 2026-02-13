from fastapi import FastAPI
from pydantic import BaseModel
from backend.workflow import run_workflow

app = FastAPI(title="AI Home Maintenance API")


class EnquiryRequest(BaseModel):
    message: str


@app.post("/analyze")
def analyze_enquiry(request: EnquiryRequest):

    result = run_workflow(request.message)

    return {
        "intent": result["intent"],
        "entities": result["entities"],
        "validation": result["validation"],
        "response": result["response"]
    }