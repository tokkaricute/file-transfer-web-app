import os
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Union


class FileEntry:
    def __init__(self, name: str, size: int, is_dir: bool, last_modified: str):
        self.name = name
        self.size = size
        self.is_dir = is_dir
        self.last_modified = last_modified

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "size": self.size,
            "is_dir": self.is_dir,
            "last_modified": self.last_modified,
        }


class FileManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir).resolve()

    def safe_resolve(self, rel_path: str) -> Path:
        """
        Resolves the relative path against the base directory,
        ensuring the resulting path is within the base directory.
        """
        target_path = (self.base_dir / rel_path).resolve()
        if not str(target_path).startswith(str(self.base_dir)):
            raise PermissionError("Access denied: path is outside the base directory.")
        return target_path

    def list_directory(self, rel_path: str) -> List[Dict[str, Any]]:
        """
        Lists the contents of the directory specified by rel_path.
        """
        target_dir = self.safe_resolve(rel_path)
        if not target_dir.is_dir():
            raise NotADirectoryError(f"{target_dir} is not a directory.")

        entries = []
        for item in target_dir.iterdir():
            stat = item.stat()
            entry = FileEntry(
                name=item.name,
                size=stat.st_size,
                is_dir=item.is_dir(),
                last_modified=datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            )
            entries.append(entry.to_dict())
        
        # Sort entries: directories first, then files by name
        entries.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return entries

    def create_zip(self, file_paths: List[Path]) -> bytes:
        """
        Creates a ZIP archive from the given file paths and returns its bytes.
        """
        import io
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in file_paths:
                # Use only the name of the file in the ZIP archive
                zip_file.write(file_path, arcname=file_path.name)
        return zip_buffer.getvalue()

