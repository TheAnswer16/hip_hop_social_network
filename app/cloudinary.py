import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

class Cloudinary:
    def upload(file, fileName):
        cloudinary.config(
,
            secure=True
        )
        print(file)
        
        uploaded_file = cloudinary.uploader.upload(file, public_id = fileName)
        
        print (uploaded_file)
        return uploaded_file['secure_url']
        
    
