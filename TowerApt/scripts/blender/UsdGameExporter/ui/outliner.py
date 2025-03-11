# OUTLINER_MT_context_menu

import bpy

class USDGE_Outliner_Submenu(bpy.types.Menu):
    ...


def USDGE_Outliner_Menu_Mixin(self, context):
    active_object = context.active_object
    layout = self.layout
    if active_object:
        layout.label(text="USD")
        layout.prop_menu_enum(
            active_object.USDGE, "kind", 
            text="Kind: " + layout.enum_item_name(active_object.USDGE, "kind", active_object.USDGE.kind)
        )
        layout.prop_menu_enum(
            active_object.USDGE, "purpose",
            text="Purpose: " + layout.enum_item_name(active_object.USDGE, "purpose", active_object.USDGE.purpose)
        )
        layout.separator()
