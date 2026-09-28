import os
import glob
from PIL import Image

def compress_image(file_path):
    # Only compress files over 150KB
    if os.path.getsize(file_path) < 150 * 1024:
        return
    try:
        with Image.open(file_path) as img:
            # Save original format if possible, otherwise webp or jpeg
            format = img.format
            if format not in ['JPEG', 'PNG', 'WEBP']:
                return
            
            # Reduce size slightly if width is > 1920
            if img.width > 1920:
                ratio = 1920.0 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1920, new_height), Image.Resampling.LANCZOS)
                
            # Compress and overwrite
            if format == 'PNG':
                # Convert PNG to WebP to save more space, and update HTML if needed, but to be safe keep it PNG but optimized, or just WEBP if it's too big?
                # Actually, saving PNG as optimized can be slow. Let's just compress it by reducing colors or saving it with optimize=True
                img.save(file_path, optimize=True)
            elif format == 'JPEG':
                img.save(file_path, 'JPEG', quality=75, optimize=True)
            elif format == 'WEBP':
                img.save(file_path, 'WEBP', quality=75)
            print(f"Compressed {file_path}")
    except Exception as e:
        print(f"Failed to compress {file_path}: {e}")

if __name__ == '__main__':
    images = glob.glob('assets/images/**/*', recursive=True)
    for img_path in images:
        if os.path.isfile(img_path):
            ext = os.path.splitext(img_path)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                compress_image(img_path)
