from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://xdream:sima5654@192.168.50.17/")
db = client["test_file_server"]
fs = GridFS(db)  # type: ignore


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Read the file content
    contents = await file.read()

    # Store the file in GridFS
    file_id = fs.put(contents, filename=file.filename)

    return {
        "file_id": str(file_id),
        "file_url": f"/file/{file_id}",
        "show_image": f"/show_image/{file_id}",
    }


@app.get("/download/{file_id}")
async def get_file(file_id: str):
    # Retrieve the file from GridFS
    file = fs.get(ObjectId(file_id))
    if file:
        # Return the file contents as a streaming response
        return StreamingResponse(
            iter([file.read()]),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file.filename}"},
        )
    else:
        return {"error": "File not found"}


@app.get("/image/{file_id}")
async def get_image_data(file_id: str):
    # Retrieve the file from GridFS
    file = fs.get(ObjectId(file_id))
    if file:
        # Return the file contents as a streaming response with the appropriate content type
        return StreamingResponse(
            iter([file.read()]), media_type="application/octet-stream"
        )
    else:
        return {"error": "File not found"}


@app.get("/show_image/{file_id}")
async def show_image(file_id: str):
    # Retrieve the file from GridFS
    file = fs.get(ObjectId(file_id))
    if file:
        # Return an HTML page with the image embedded
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Image</title>
        </head>
        <body>
            <h1>Image</h1>
            <img src="/image/{file_id}" alt="Uploaded Image" style="max-width:100%">
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    else:
        return HTMLResponse(content="File not found", status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
