from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from get_fund_data import get_fund_data_json

app = FastAPI()

# Allow all CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def run_main():
    result = get_fund_data_json()
    return {"response": result}