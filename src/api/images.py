import shutil
from fastapi import APIRouter, UploadFile

router = APIRouter(prefix='/images', tags=['Изображение книги'])

@router.post("")
async def add_images(
        file: UploadFile
):
    with open(f"src/static/images{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    return {
        "status": "success",
        "data": "images"
    }
