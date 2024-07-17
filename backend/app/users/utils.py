import os
import logging

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

import shutil

import users.crud as users_crud

# Define a loggger created on main.py
logger = logging.getLogger("myLogger")

async def save_user_image(user_id: int, file: UploadFile, db: Session):
    try:
        upload_dir = "user_images"
        os.makedirs(upload_dir, exist_ok=True)

        # Get file extension
        _, file_extension = os.path.splitext(file.filename)
        filename = f"{user_id}{file_extension}"

        file_path_to_save = os.path.join(upload_dir, filename)

        with open(file_path_to_save, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return users_crud.edit_user_photo_path(user_id, file_path_to_save, db)
    except Exception as err:
        # Log the exception
        logger.error(f"Error in save_user_image: {err}", exc_info=True)

        # Remove the file after processing
        if os.path.exists(file_path_to_save):
            os.remove(file_path_to_save)

        # Raise an HTTPException with a 500 Internal Server Error status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from err