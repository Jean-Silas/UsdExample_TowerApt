import bpy

def SetDataNameToObjectName():
    objects = bpy.data.objects
    
    for obj in objects:
        print(obj.name)
        
        if obj.data != None:
            print(f"    {obj.data.name}")
            if obj.data.users == 1:
                obj.data.name = obj.name


SetDataNameToObjectName()