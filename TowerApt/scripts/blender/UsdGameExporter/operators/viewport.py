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


def extend_selection_to_parents(obj: bpy.types.Object, kind: str, mode: str, select_untagged: bool):
    if obj.parent:
        comparison = compare_kind(kind, obj.parent.USDGE.kind)
        match comparison:
            case -1:
                extend_selection_to_children(obj, kind, mode, select_untagged)
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
                        extend_selection_to_children(obj.parent, kind, mode, select_untagged)
                    case _:
                        extend_selection_to_parents(obj.parent, kind, mode, select_untagged)
                        ...
            case 1:
                obj.parent.select_set(True)
                extend_selection_to_parents(obj.parent, kind, mode, select_untagged)
            case _:
                print(f"Impossible math: {comparison}")
    else:
        # extend_selection_to_children(obj, kind, mode, select_untagged)a
        ...

def extend_selection_to_children(obj: bpy.types.Object, kind: str, mode:str, select_untagged: bool):
    if obj == None:
        return
    for child in obj.children:
        if select_untagged == False and child.USDGE.kind == 'NOKIND':
            continue

        comparison = compare_kind(kind, child.USDGE.kind)
        print(f"{child.name}:  {comparison}")
        match comparison:
            case -1:
                continue
            case 0:
                child.select_set(True)
            case 1:
                child.select_set(True)
                extend_selection_to_children(child, kind, mode, select_untagged)
            case _:
                print(f"Impossible math: {comparison}")

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
    

    def invoke(self, context, event):
        bpy.ops.view3d.select('EXEC_DEFAULT', True, extend=False, location=(event.mouse_region_x, event.mouse_region_y))
        if self.mode != 'PRIM':
            return self.execute(context)
        return {'FINISHED'}
        
       
    def execute(self, context):
        for obj in context.selected_objects:
            # extend_selection_to_children(obj, self.kind)
            extend_selection_to_parents(obj, self.kind, self.mode, self.select_untagged)
        return {'FINISHED'}
        

OUT = [
    USDGE_OT_SelectByKind
]