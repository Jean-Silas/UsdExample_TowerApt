import bpy
from . import properties

def register():
    for cls in properties.OUT:
        bpy.utils.register_class(cls)

    bpy.types.Object.USDGE = bpy.props.PointerProperty(type=properties.USDGEExportObjectProps)
    bpy.types.Collection.USDGE = bpy.props.PointerProperty(type=properties.USDGEExportCollectionProps)
    bpy.types.WindowManager.USDGEState = bpy.props.PointerProperty(type=properties.USDGEExportStateProps)


def unregister():

    del bpy.types.Object.USDGE
    del bpy.types.Collection.USDGE
    del bpy.types.WindowManager.USDGEState

    for cls in properties.OUT:
        bpy.utils.unregister_class(cls)
