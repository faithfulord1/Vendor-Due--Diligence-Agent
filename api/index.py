from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Vendor Due Diligence Agent is live"}
