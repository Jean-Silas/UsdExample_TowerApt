import bpy

def UpdateCollection(collection, new_root: str):
    exporter_index = collection.exporters.find("Universal Scene Description")
    if exporter_index > -1:
        exporter = collection.exporters[exporter_index]
        old_path = exporter.export_properties.filepath
        
        new_path = new_root + collection.name.replace("::", "/var/")
        print(collection.name, old_path, new_path)
        
        exporter.export_properties.filepath = new_path
    

def SetExportPaths(scene, new_root_path: str):
    scene = bpy.data.scenes[scene]
    root_collection = scene.collection
    print(root_collection.name)

    for child in root_collection.children_recursive:
        UpdateCollection(child, new_root_path)
    
    
    
SetExportPaths("Props", "//../usd/multifile/")
    