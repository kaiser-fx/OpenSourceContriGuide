from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Message" : "Hello Welcome to Open Source Contribution Guide"}