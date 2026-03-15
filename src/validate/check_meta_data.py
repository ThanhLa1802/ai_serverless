from fastapi import UploadFile, HTTPException

ALLOWED_TYPES = ["application/pdf", "text/plain"]
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB

async def validate_file(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Định dạng file không hỗ trợ.")
    
    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File quá lớn (>10MB).")
    
    file.file.seek(0) # Reset con trỏ file sau khi đọc size