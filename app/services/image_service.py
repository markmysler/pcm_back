from fastapi import UploadFile, HTTPException
from pathlib import Path
import os
from PIL import Image, UnidentifiedImageError
import io
import unicodedata
import re
import glob
import uuid
from app.core.config import MAX_FILE_SIZE, TARGET_FILE_RES
import app.messages.images as msg

base_url = os.getenv("BASE_URL", "http://localhost/")

async def upload_image(file: UploadFile, save_path: str, save_as: str):
    try:
        # Generate a UUID for the file
        file_id = str(uuid.uuid4())
        
        # Create subdirectories based on the UUID
        subdir1 = file_id[0:2]
        subdir2 = file_id[2:4]
        
        # Create static root
        static_root =f"app/{save_path}"
        static_dir = Path(f"app/{save_path}/{subdir1}/{subdir2}")
        
        # Get the file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png', '.webp']:
            raise HTTPException(status_code=400, detail=msg.invalid_extension)
        
        # Check if the uploaded file is an image
        if file.content_type not in ["image/jpeg", "image/png", "image/jpg", "image/webp"]:
            raise HTTPException(status_code=400, detail=msg.invalid_file)
        
        # Check file size
        file_contents = await file.read()
        file_size = len(file_contents)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail=msg.invalid_size)
        
        # Sanitize the filename
        sanitized_name = sanitize_filename(save_as)
        file_name = f"{sanitized_name}{file_extension}"
        
        # Search for an existing file with the same name in the static root directory
        existing_files = glob.glob(f"{static_root}/**/{sanitized_name}.*", recursive=True)
        if existing_files:
            # If a file with the same name exists, remove it
            for existing_file in existing_files:
                os.remove(existing_file)
                # Use the directory of the removed file as the new save path
                static_dir = Path(existing_file).parent
                subdir1 = static_dir.parts[-2]  # Extract the second-to-last part of the path
                subdir2 = static_dir.parts[-1]  # Extract the last part of the path
        
        # Create the full save path with subdirectories
        static_dir.mkdir(parents=True, exist_ok=True)
        
        # Open the image using Pillow
        try:
            img = Image.open(io.BytesIO(file_contents))
        except UnidentifiedImageError:
            raise HTTPException(status_code=400, detail=msg.invalid_error)
        except Exception as e:
            raise HTTPException(status_code=400, detail=msg.opening_error)
        
        # Resize the image while maintaining aspect ratio
        img.thumbnail(TARGET_FILE_RES)
        
        # Create a new image with white background
        new_img = Image.new("RGB", TARGET_FILE_RES, (255, 255, 255))
        
        # Paste the resized image onto the center of the new image
        position = ((TARGET_FILE_RES[0] - img.size[0]) // 2, (TARGET_FILE_RES[1] - img.size[1]) // 2)
        new_img.paste(img, position)
        
        # Define the full file path
        file_path = static_dir / file_name
        
        # Save the file with compression
        new_img.save(file_path, optimize=True, quality=85)
        
        # Return the URL including the subdirectories
        return f"{base_url}{save_path}{subdir1}/{subdir2}/{file_name}"
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=msg.unexpected_error)


def sanitize_filename(filename):
    try:
        # Remove any non-ASCII characters
        filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
        
        # Replace spaces
        filename = filename.replace(' ', '_')
        
        # Remove any non-alphanumeric characters except for '.' and '_'
        filename = re.sub(r'[^\w\-_\.]', '', filename)
        
        # Remove any runs of dots (e.g., '..', '...', etc.)
        filename = re.sub(r'\.+', '.', filename)
        
        # Ensure the filename isn't empty and doesn't start with a dot
        if not filename or filename.startswith('.'):
            filename = 'unnamed_file'
        
        return filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=msg.sanitizing_error)