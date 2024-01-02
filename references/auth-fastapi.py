import os
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
API_KEYS = os.environ.get("XD_API_KEY")
if API_KEYS is None:
    raise ValueError("XD_API_KEY environment variable not set")


def validate_api_key(
    api_key: str = Security(APIKeyHeader(name="XD_API_KEY")),
) -> str:
    """Implement the API key authentication method."""
    if api_key in API_KEYS:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


app = FastAPI(dependencies=[Depends(validate_api_key)])


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
def home():  # request: Request
    """Sample endpoint (not secured)"""
    return "Hello World"


@app.get("/home")
def protected_route():
    """Implement a route that requires API key authentication."""
    return {"message": "Access granted!"}


@app.post("/items")
async def create_item(item: Item):
    """test post"""
    return item


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
