from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "live",
        "project": "Faithfulord Vendor Due Diligence Agent",
        "message": "TPRM / Vendor Risk Intelligence API is running successfully."
    }
