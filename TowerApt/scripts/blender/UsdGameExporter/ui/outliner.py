# OUTLINER_MT_context_menu

import bpy

class USDGE_Outliner_Submenu(bpy.types.Menu):
    ...


def USDGE_Outliner_Menu_Mixin(self, context):
    active_object = context.active_object
    layout = self.layout
    if active_object:
        layout.prop_menu_enum(active_object.USDGE, "kind", text=active_object.USDGE.kind)
        layout.prop_menu_enum(active_object.USDGE, "purpose")
