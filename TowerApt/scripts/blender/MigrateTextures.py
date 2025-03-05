import bpy

def MoveTextureDirectory(from_dir: str, to_dir: str):
    for img in bpy.data.images:
        if img.filepath.startswith(f"//{from_dir}"):
            old_path = img.filepath
            new_path = old_path.replace(from_dir, to_dir)
            
            print(f"Found: {old_path} \n    Replacing with: {new_path}")
            
            img.filepath = new_path


MoveTextureDirectory("test\\", "")