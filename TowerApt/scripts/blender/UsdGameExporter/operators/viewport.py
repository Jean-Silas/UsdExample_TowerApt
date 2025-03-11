import bpy
import numpy


def compare_kind(kind_a: str, kind_b: str) -> int:
    kind_weights = {
        'ASSEMBLY': 4,
        'GROUP': 3,
        'COMPONENT': 2,
        'SUBCOMPONENT': 1,
        'NOKIND': 0
    }
    return numpy.sign(kind_weights[kind_a] - kind_weights[kind_b]) 


def extend_selection_to_parents(context: bpy.types.Context, obj: bpy.types.Object, kind: str, mode: str, select_untagged: bool):
    if obj.parent:
        
        comparison = compare_kind(kind, obj.parent.USDGE.kind)
        #  print(f"Object: {obj.name} | Parent: {obj.parent.name} | Comparison: {comparison}")
        match comparison:
            case -1:
                extend_selection_to_children(context, obj, kind, mode, select_untagged)
                # match mode:
                #     case 'MODEL_IMMEDIATE':
                #         ...
                #     case 'MODEL_IMMEDIATE_SATURATE':
                #         extend_selection_to_children(obj.parent, kind, mode, select_untagged)
                #     case _:
                #         extend_selection_to_parents(obj.parent, kind, mode, select_untagged)
                #         ...
            case 0:
                obj.parent.select_set(True)
                match mode:
                    case 'MODEL_IMMEDIATE':
                        ...
                    case 'MODEL_IMMEDIATE_SATURATE':
                        # print(f"Current Object: {obj.name} | Parent: {obj.parent.name} | Selecting Children")
                        extend_selection_to_children(context, obj.parent, kind, mode, select_untagged)
                    case _:
                        extend_selection_to_parents(context, obj.parent, kind, mode, select_untagged)
                        ...
            case 1:
                obj.parent.select_set(True)
                extend_selection_to_parents(context, obj.parent, kind, mode, select_untagged)
            case _:
                print(f"Impossible math: {comparison}")
    else:
        # extend_selection_to_children(obj, kind, mode, select_untagged)a
        ...

    if context.space_data.local_view != None:
        obj.local_view_set(context.space_data, True)

def extend_selection_to_children(context: bpy.types.Context, obj: bpy.types.Object, kind: str, mode:str, select_untagged: bool):
    if obj == None:
        return
    for child in obj.children:
        if select_untagged == False and child.USDGE.kind == 'NOKIND':
            continue

        comparison = compare_kind(kind, child.USDGE.kind)
        # print(f"Descending: {obj.name} {child.name}:  {comparison}")
        match comparison:
            case -1:
                continue
            case 0:
                child.select_set(True)
                extend_selection_to_children(context, child, kind, mode, select_untagged)
            case 1:
                child.select_set(True)
                extend_selection_to_children(context, child, kind, mode, select_untagged)
            case _:
                print(f"Impossible math: {comparison}")
    
    if context.space_data.local_view != None:
        obj.local_view_set(context.space_data, True)

# Building a selection hierarchy around Model Kinds reveals some interesting issues with the hierarchy as-implemented
# TL;DR: Everything becomes an assembly.
class USDGE_OT_SelectByKind(bpy.types.Operator):
    """Uses the ModelKind to drive recursive selection expansion"""
    bl_idname = "usdge.select_by_kind"
    bl_label = "Select By Kind"
    bl_options = {'REGISTER'}

    kind: bpy.props.EnumProperty(
        name="Model Kind",
        description="The Kind of the object in the USD hierarchy",
        items = [
            ('NOKIND', "None", "No", 'NONE', 1),
            ('ASSEMBLY', "Assembly", "A group that defines a Primary Asset", 'NONE', 2),
            ('GROUP', "Group", "A generic group", 'NONE', 3),
            ('COMPONENT', "Component", "a 'leaf model' that can contain no other models", 'NONE', 4),
            ('SUBCOMPONENT', "Subcomponent", "An important part of a component", 'NONE', 5),
        ]
    ) # type: ignore

    select_untagged: bpy.props.BoolProperty(
        name="Select Untagged",
        description="Include objects that do not have a model kind",
        default=False
    ) # type: ignore


    mode: bpy.props.EnumProperty(
        name="Selection Mode",
        description="The Kind of the object in the USD hierarchy",
        items = [
            ('PRIM', "Primitives", "Select individual primitives", 'NONE', 1),
            ('MODEL', "Models", "Select the full hierarchy bound by the model kind", 'NONE', 2),
            ('MODEL_IMMEDIATE', "Immediate Models", "Select the immediate hierarchy bound by the model kind", 'NONE', 3),
            ('MODEL_IMMEDIATE_SATURATE', "Saturate Models", "Select the immediate hierarchy bound by the model kind", 'NONE', 4),
        ]
    ) # type: ignore
    
    override_click_location: bpy.props.BoolProperty(
        name="Override Location",
        description="Manually set the click location",
        default=False
    ) # type: ignore

    click_location: bpy.props.IntVectorProperty(
        name="Click Location",
        description="Manual click location",
        size=2,
        default=(0,0)
    ) # type: ignore


    def invoke(self, context, event):
        if self.override_click_location:
            location = self.click_location
        else:
            location = (event.mouse_region_x, event.mouse_region_y)

        # print(f"Click Location: {location} | Raw: {(event.mouse_region_x, event.mouse_region_y)}")
        bpy.ops.view3d.select('EXEC_DEFAULT', True, extend=False, location=location)
        if self.mode != 'PRIM':
            return self.execute(context)
        return {'FINISHED'}
        
       
    def execute(self, context):
        for obj in context.selected_objects:
            # extend_selection_to_children(obj, self.kind)
            extend_selection_to_parents(context, obj, self.kind, self.mode, self.select_untagged)
        return {'FINISHED'}

class USDGE_OT_SelectionPie(bpy.types.Operator):
    bl_idname = "usdge.selection_pie"
    bl_label = "USDGE Selection Pie"
    bl_description = "A combined select operator and selection-refinement pie menu for USD Objects"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        mouse_loc = (event.mouse_region_x, event.mouse_region_y)

        def draw_pie(self, context):
            pie = self.layout.menu_pie()
            pie.operator_context = 'EXEC_DEFAULT'

            # LEFT
            op = pie.operator("view3d.select", text="Deselect")
            op.location = mouse_loc
            op.deselect = True


            # RIGHT
            op = pie.operator("view3d.select", text="Select")
            op.location = mouse_loc
            op.extend = False


            # BOTTOM
            # pie.label(text="BOTTOM")
            pie.operator_context = 'INVOKE_DEFAULT'
            wm = context.window_manager
            tool = context.workspace.tools["usdgeexport.usdselection"]
            tool_props = tool.operator_properties("USDGE.select_by_kind")

            op = pie.operator("USDGE.select_by_kind", text="USD Select")
            op.override_click_location = True
            op.click_location = mouse_loc
            op.kind = tool_props.kind
            op.select_untagged = tool_props.select_untagged
            op.mode = tool_props.mode

            # TOP
            pie.operator_context = 'EXEC_DEFAULT'
            op = pie.operator("view3d.select", text="Extend Select")
            op.location = mouse_loc
            op.extend = True

            # TOP LEFT


            # TOP RIGHT
            # BOTTOM LEFT
            # BOTTOM RIGHT

        context.window_manager.popup_menu_pie(event, draw_func=draw_pie, title="USD PIE")
        return {'FINISHED'}
    


OUT = [
    USDGE_OT_SelectByKind,
    USDGE_OT_SelectionPie,
]