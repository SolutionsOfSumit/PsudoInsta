from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Sumit is a monster"} 

@app.get('/post')
def get_post():
    return { "data": "Your posts will be visible here"}

@app.post('/create_post')
def create_post(information: dict = Body(...)):
    print(information)
    # return {"data": f"{information['title']} and {information['content']}"}