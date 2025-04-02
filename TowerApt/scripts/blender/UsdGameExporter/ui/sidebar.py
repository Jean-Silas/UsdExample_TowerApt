import bpy
from bpy.types import (
    Panel
)
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)

def active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)

class VIEW3D_PT_usdgeexport_panel(Panel):
    bl_idname = "VIEW3D_PT_usdgeexport_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "USD GE"
    bl_label = "USDGE Export Panel"
    bl_options = { 'HEADER_LAYOUT_EXPAND',  }

    bl_ui_units_x = 12

    @classmethod
    def poll(cls, context):
        if context.view_layer.objects.active:
            return True
        
    def draw(self, context):
        # USDGE_props = context.workspace.USDGE

        # Aliased Stuff
        scene = context.scene
        active_obj = context.view_layer.objects.active
        wm = context.window_manager

        active_collection = context.collection

        debug = True

        layout = self.layout
        root = layout.column(align=False)

        if (debug):
            root.prop(context.window_manager.USDGEState, "run_hooks")
        
        box = root.box()
        
        bcol = box.column(align=True)
        bcol.use_property_split = True
        bcol.label(text="Active Object Info")

        bcol.prop(
            active_obj,
            "name",
            text="Object Name"
        )
        if (active_obj.data):
            bcol.prop(
                active_obj.data,
                "name",
                text="Data Block Name"
            )
        #  Deprecated after workflow change     
        # bcol.separator()
        # bcol.prop(
        #     active_obj.USDGE,
        #     "status"
        # )

        if active_obj.USDGE.status != "EXCLUDE":
            box = root.box()
            bcol = box.column(align=True)
            bcol.label(text="Export Settings")

        # if active_obj.USDGE.status in ("EXPORT", "EXPORT_RECURSIVE"):
        bcol.use_property_split = True

        bcol.prop(
            active_obj.USDGE,
            "kind"
        )
        if active_obj.USDGE.kind == 'ASSEMBLY':
            bcol.prop(active_obj.USDGE, "assembly_subkind")
        bcol.prop(
            active_obj.USDGE,
            "purpose"
        )
        bcol.separator()

        bcol.prop(
            active_obj.USDGE,
            "convert_to"
        )

        #  Deprecated after workflow change
        # bcol.prop(
        #     active_obj.USDGE,
        #     "flatten"
        # )

        # bcol.separator()
        # bcol.prop(
        #     active_obj.USDGE,
        #     "auto_exclude_pattern"
        # )

        # bcol.separator()
        # bcol.prop(
        #     active_obj.USDGE,
        #     "auto_exclude_types"
        # )

        # TODO: Replace with task-specific exporters — Export Layout, Export Props, Export Assemblies, etc.
        # root.operator("USDGE.export")

# bpy.data.meshes["Cube"].name
OUT = [
    VIEW3D_PT_usdgeexport_panel
]