import bpy

from . export import OUT as exp_out

from . viewport import OUT as vp_out


def register():
    for cls in exp_out:
        bpy.utils.register_class(cls)
    for cls in vp_out:
        bpy.utils.register_class(cls)

def unregister():
    for cls in exp_out:
        bpy.utils.unregister_class(cls)
    for cls in vp_out:
        bpy.utils.unregister_class(cls)