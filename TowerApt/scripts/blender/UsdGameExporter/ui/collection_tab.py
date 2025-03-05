import bpy
from bpy.types import (
    Panel
)
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)

def active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)

class VIEW3D_PT_usdgeexport_collection_panel(Panel):
    bl_idname = "VIEW3D_PT_usdgeexport_collection_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_category = "USD GE"
    bl_context = "collection"
    
    bl_label = "USDGEExport Collection Settings"
    # bl_options = { 'HEADER_LAYOUT_EXPAND',  }


    @classmethod
    def poll(cls, context):
        # TODO: Is this view layer dependent?
        if context.collection:
            return True
        
    def draw(self, context):
        scene = context.scene
        active_collection = context.collection
        settings = active_collection.USDGE
        wm = context.window_manager

        layout = self.layout
        root = layout.column(align=False)
        
        box = root.box()

        bcol = box.column(align=True)
        bcol.use_property_split = True
        bcol.label(text="Active Collection Info")

        bcol.prop(
            settings,
            "kind"
        )


OUT = [
    VIEW3D_PT_usdgeexport_collection_panel
]