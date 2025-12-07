from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from process_audio import full_audio_edit

app = FastAPI()


# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads/"

@app.get("/")
def home():
    return {"message": "Audio API is working!"}

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    
    input_path = UPLOAD_FOLDER + f"input_{uuid.uuid4()}.mp3"
    output_path = UPLOAD_FOLDER + f"output_{uuid.uuid4()}.mp3"

    # Save file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Process audio
    full_audio_edit(input_path, output_path)

    # Return processed file
    return FileResponse(output_path, media_type="audio/mpeg", filename="final_output.mp3")
