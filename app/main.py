import os
import pendulum
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, status
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
API_KEYS = os.getenv("XD_API_KEY")
if API_KEYS is None:
    raise ValueError("XD_API_KEY environment variable not set")

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client[os.getenv("MONGO_DB_NAME", "myFiles")]
fs = GridFS(db)

# use token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload/", dependencies=[Depends(api_key_auth)])
async def upload_image(file: UploadFile = File(...)):
    # Read the file content
    contents = await file.read()

    # Store the file in GridFS
    file_id = fs.put(contents, filename=file.filename)
    logger.info(
        f"{file.filename}, {round((file.size or 1) / 1024 / 1024, 2)} MB, uploaded."
    )

    return JSONResponse(
        {
            "file_id": str(file_id),
            "file_url": f"{BASE_URL}/get/{file_id}/",
            "show_image": f"{BASE_URL}/get/{file_id}/?output=html",
        },
        status_code=200,
    )


class ToDeleteProps(BaseModel):
    file_ids: list[str]


@app.post("/delete/", dependencies=[Depends(api_key_auth)])
async def delete_image(to_be_delete: ToDeleteProps):
    # Delete the files from GridFS
    for file_id in to_be_delete.file_ids:
        fs.delete(ObjectId(file_id))
        logger.info(f"File {file_id} deleted.")

    return JSONResponse({"message": "Files deleted successfully."}, status_code=200)


@app.get("/list/", dependencies=[Depends(api_key_auth)])
async def list_files():
    # Retrieve all files from GridFS
    files = fs.find()

    files_list = [
        {
            "filename": file.filename,
            "id": str(file._id),
            "size": file.length,
            "delta_time": pendulum.instance(file.upload_date).diff().seconds,
        }
        for file in files
    ]

    logger.info(f"{len(files_list)} files in DATABASE")

    return JSONResponse(files_list, status_code=200)


@app.get("/get/{file_id}/")
async def get(file_id: str, output: str | None = "src"):
    # Retrieve the file from GridFS
    file = fs.get(ObjectId(file_id))
    if file:
        match output:
            case "download":
                # Return the file contents as a file
                return StreamingResponse(
                    iter([file.read()]),
                    media_type="application/octet-stream",
                    headers={
                        "Content-Disposition": f"attachment; filename={file.filename}"
                    },
                )
            case "html":
                # Return an HTML page with the image embedded
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Image</title>
                </head>
                <body>
                    <h1>Image{file.name}</h1>
                    <img src="/get/{file_id}/" alt="Uploaded Image" style="max-width:100%">
                </body>
                </html>
                """
                return HTMLResponse(content=html_content, status_code=200)
            case _:
                # Return the file contents as a streaming response
                return StreamingResponse(
                    iter([file.read()]),
                    media_type="application/octet-stream",
                )
    else:
        return {"error": "File not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
