from fastapi import FastAPI

app = FastAPI()


def build_hello_message(name: str = "World") -> dict:
    return {"message": f"Hello {name}"}


@app.get("/")
def read_root():
    return build_hello_message()
