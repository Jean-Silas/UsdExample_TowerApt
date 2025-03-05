import bpy
from bpy.types import WorkSpaceTool

class USDSelectionTool(WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'OBJECT'
    bl_idname = 'usdgeexport.usdselection'
    bl_label = "USD Select"
    bl_description = (
        "A custom selection mode that uses USD Model Kinds.\n"
    )
    bl_icon = "ops.generic.select_circle"
    bl_widget = None

    bl_options = {'KEYMAP_FALLBACK'}

    bl_keymap = (
        ("USDGE.select_by_kind", {"type": 'LEFTMOUSE', "value": 'CLICK'}, None),
        # ("transform.translate", {"type": 'RIGHTMOUSE', "value": 'PRESS'}, None),
    )

    def draw_settings(context, layout, tool):
        props = tool.operator_properties("USDGE.select_by_kind")
        layout.prop(props, "kind")
        layout.prop(props, "mode")
        layout.prop(props, "select_untagged")
        