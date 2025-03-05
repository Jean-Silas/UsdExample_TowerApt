import bpy

from .usdhook import USDHookExample


def register():
    bpy.utils.register_class(USDHookExample)
    ...

def unregister():
    bpy.utils.unregister_class(USDHookExample)
    ...