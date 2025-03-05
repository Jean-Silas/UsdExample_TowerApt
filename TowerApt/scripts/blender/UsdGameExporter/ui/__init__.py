import bpy

from . import sidebar
from . import collection_tab
from . import outliner

def register():

    bpy.types.OUTLINER_MT_object.prepend(outliner.USDGE_Outliner_Menu_Mixin)
    for cls in sidebar.OUT:
        bpy.utils.register_class(cls)

    for cls in collection_tab.OUT:
        bpy.utils.register_class(cls)
    ...

def unregister():
    for cls in sidebar.OUT:
        bpy.utils.unregister_class(cls)

    for cls in collection_tab.OUT:
        bpy.utils.unregister_class(cls)
    
    bpy.types.OUTLINER_MT_object.remove(outliner.USDGE_Outliner_Menu_Mixin)