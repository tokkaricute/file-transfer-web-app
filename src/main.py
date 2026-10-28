import os
import argparse
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Request, Response, Form
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add project root to sys.path to allow running src/main.py directly
import sys
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.file_manager import FileManager
from src.auth import verify_password

app = FastAPI()

# Config
BASE_DIR = os.getcwd()
PASSWORD = os.getenv("FILE_TRANSFER_PASSWORD", None)

file_manager = FileManager(BASE_DIR)
templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content)

@app.post("/auth")
async def authenticate(password: str = Form(...)):
    if verify_password(password, PASSWORD):
        return {"status": "ok"}
    raise HTTPException(status_code=401, detail="Invalid password")

@app.get("/list")
async def list_files(rel_path: str = "."):
    try:
        entries = file_manager.list_directory(rel_path)
        return {"entries": entries, "current_path": rel_path}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except NotADirectoryError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(rel_path: str = Form("."), files: List[UploadFile] = File(...)):
    try:
        target_dir = file_manager.safe_resolve(rel_path)
        for file in files:
            file_path = target_dir / file.filename
            with file_path.open("wb") as buffer:
                while True:
                    chunk = await file.read(1024 * 1024) # 1MB chunks
                    if not chunk:
                        break
                    buffer.write(chunk)
        return {"status": "success"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/download")
async def bulk_download(file_names: List[str] = Form(...), rel_path: str = Form(".")):
    try:
        target_dir = file_manager.safe_resolve(rel_path)
        file_paths = []
        for name in file_names:
            p = target_dir / name
            if p.is_file():
                file_paths.append(p)
            else:
                raise HTTPException(status_code=404, detail=f"{name} is not a file.")
        
        if not file_paths:
            raise HTTPException(status_code=400, detail="No files selected")

        zip_content = file_manager.create_zip(file_paths)
        return Response(
            content=zip_content,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=download.zip"}
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    import uvicorn
    import sys

    parser = argparse.ArgumentParser(description="File Transfer Web App")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to share")
    parser.add_argument("-p", "--password", default=None, help="Password for access")

    args = parser.parse_args()

    global BASE_DIR, PASSWORD
    BASE_DIR = os.path.abspath(args.directory)
    PASSWORD = args.password

    file_manager.__init__(BASE_DIR)

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
