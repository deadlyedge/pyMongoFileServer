import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

app = FastAPI()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client[os.getenv("MONGO_DB_NAME", "myFiles")]
fs = GridFS(db)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Read the file content
    contents = await file.read()

    # Store the file in GridFS
    file_id = fs.put(contents, filename=file.filename)

    return {
        "file_id": str(file_id),
        "file_url": f"{BASE_URL}/file/{file_id}/",
        "show_image": f"{BASE_URL}/file/{file_id}/?output=html",
    }


@app.get("/file/{file_id}/")
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
                    <img src="/file/{file_id}/" alt="Uploaded Image" style="max-width:100%">
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


# @app.get("/download/{file_id}")
# async def get_file(file_id: str):
#     # Retrieve the file from GridFS
#     file = fs.get(ObjectId(file_id))
#     if file:
#         # Return the file contents as a streaming response
#         return StreamingResponse(
#             iter([file.read()]),
#             media_type="application/octet-stream",
#             headers={"Content-Disposition": f"attachment; filename={file.filename}"},
#         )
#     else:
#         return {"error": "File not found"}


# @app.get("/image/{file_id}")
# async def get_image_data(file_id: str):
#     # Retrieve the file from GridFS
#     file = fs.get(ObjectId(file_id))
#     if file:
#         # Return the file contents as a streaming response with the appropriate content type
#         return StreamingResponse(
#             iter([file.read()]), media_type="application/octet-stream"
#         )
#     else:
#         return {"error": "File not found"}


# @app.get("/show_image/{file_id}")
# async def show_image(file_id: str):
#     # Retrieve the file from GridFS
#     file = fs.get(ObjectId(file_id))
#     if file:
#         # Return an HTML page with the image embedded
#         html_content = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>Image</title>
#         </head>
#         <body>
#             <h1>Image{file.name}</h1>
#             <img src="/image/{file_id}" alt="Uploaded Image" style="max-width:100%">
#         </body>
#         </html>
#         """
#         return HTMLResponse(content=html_content, status_code=200)
#     else:
#         return HTMLResponse(content="File not found", status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
