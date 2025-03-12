import bpy
import numpy
from collections import namedtuple
from typing import NamedTuple

# Expressing USD Kinds as a subset of a broader system comprised of three ints
# and a conceptual compromise:
# 
# 1. Model kinds are linearized to a 3bit integer axis.
# 2. Subcomponents are simply the first element in a second 3bit integer axis.
# 3. Additional information on encapsulation/unrolling can be stored in a third 
#    2-bit integer.
# 
# There isn't a good set of names for the two axes here, I could call them kiki
# and bouba and the meaning would be the same. 
# 
# The first axis describes a kind of height -- an assembly is tall, a group is 
# shorter, a component is shortest. In a gaming context, it might make sense to
# have an Entity kind on this axis as well. This height could also be seen as a
# form of concrete-ness.
# 
# The second axis describes a kind of roughness. A subcomponent is rougher than
# anything that isn't a subcomponent, but smoother than things farther along
# the axis.
# 
# I realize that none of this makes sense.

class ObjectKind(NamedTuple):
    flag: int   # encapsulation flags
    model_axis: int
    entity_axis: int
    
    def __lt__(self, other):
        # print(f"{self.model_axis} | {other.model_axis}")
        return ObjectKind(
            numpy.sign(self.flag - other.flag),
            numpy.sign(self.model_axis - other.model_axis),
            numpy.sign(self.entity_axis - other.entity_axis)
        )

KindMap = {
    'NOKIND':        ObjectKind(0b00, 0b000, 0b000),

    # Yes, these two are identical; we're going to cheat with math.
    'MODEL':         ObjectKind(0b00, 0b001, 0b000),
    'COMPONENT':     ObjectKind(0b00, 0b001, 0b000),

    'GROUP':         ObjectKind(0b00, 0b010, 0b000),
    'ASSEMBLY':      ObjectKind(0b00, 0b011, 0b000),
    
    'SUBCOMPONENT':  ObjectKind(0b00, 0b000, 0b001),
}

def compare_kind(kind_a_name:str, kind_b_name):
    return KindMap[kind_a_name] < KindMap[kind_b_name]


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
        return self.execute(context)
        
       
    def execute(self, context):
        def traverse_upwards(obj: bpy.types.Object, kind: str):
            comparison = compare_kind(kind, obj.USDGE.kind)
            # print(f"Comparison for {obj.name}: {comparison.model_axis}")
            match comparison.model_axis:
                case -1:
                    obj.select_set(True)
                    # print(f"-1: Traversing Downwards from {obj.name}")
                    traverse_downwards(obj)
                    ...
                case 0:
                    obj.select_set(True)
                    # print(f"0: Traversing Downwards from {obj.name}")
                    traverse_downwards(obj)
                case 1:
                    obj.select_set(True)
                    # print(f"1: Traversing Upwards from {obj.name}")
                    if obj.parent != None: 
                        traverse_upwards(obj.parent, kind)


        def traverse_downwards(obj: bpy.types.Object):
            for child in obj.children:
                child.select_set(True)
                traverse_downwards(child)


        for obj in context.selected_objects:
            traverse_upwards(obj, self.kind)

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