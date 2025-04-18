from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    '''
    Sample python function
    '''
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    '''
    Sample python function
    '''
    return {"item_id": item_id, "q": q}
