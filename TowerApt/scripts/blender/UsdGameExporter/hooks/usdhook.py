import bpy
import bpy.types
import pxr.Gf as Gf
import pxr.Sdf as Sdf
import pxr.Usd as Usd
import pxr.UsdShade as UsdShade
import pxr.Kind as Kind
import pxr.Tf as Tf
from pxr import UsdSemantics

import textwrap

def get_kind(object_kind: str):
    # print(f"Retrieved Kind: {object_kind}")
    prim_kind = None
    match object_kind:
        case "assembly":
            prim_kind = Kind.Tokens.assembly
        case "group":
            prim_kind = Kind.Tokens.group
        case "component": 
            prim_kind = Kind.Tokens.component
        case "subcomponent":
            prim_kind = Kind.Tokens.subcomponent
        case _:
            prim_kind = None

    return prim_kind


def do_export(export_context):
    """ Include the Blender filepath in the root layer custom data.
    """
    
    if bpy.context.window_manager.USDGEState.run_hooks == False:
        print("Short Circuit")
        return False

    stage = export_context.get_stage()
    graph = export_context.get_depsgraph()

    if stage is None:
        print("Error: Null USD Stage")
        return False
    data = bpy.data
    if data is None:
        return False

    # Stuff I need to call:
    #  stage.SetDefaultPrim()
    # 
    #  stage.GetPrimAtPath()
    #  stage.GetPropertyAtPath()
    #  stage.GetObjectAtPath() <- returns a either a prim or a property, depending on the path
    #  stage.GetAttributeAtPath()
    # 
    #  stage.Traverse() <- 

    stack = stage.GetLayerStack()

    print(dir(Sdf.ValueTypeNames))

    for prim in stage.Traverse():        
        object_name = prim.GetAttribute("userProperties:blender:object_name").Get()
        if not object_name:
            continue

        source_object = bpy.data.objects[object_name]
        object_kind = source_object.USDGE.kind.lower()
        object_purpose = source_object.USDGE.purpose.lower()


        if prim_kind := get_kind(object_kind):
            prim.SetKind(prim_kind)

        prim_name: str = prim.GetName()
        if 'SCOPE' in prim_name:
            prim_type = prim.GetTypeName()
            # print(prim_name)
            # print(prim_type)
            prim.SetTypeName('Scope')
        
        # Semantics
        
        UsdSemantics.LabelsAPI.Apply(prim, "gameEntity")
        attr: Usd.Attribute = prim.CreateAttribute("semantics:labels:gameEntity", Sdf.ValueTypeNames.TokenArray)

        # if prim_purpose := prim.GetAttribute("purpose"):
        #     prim_purpose.Set(object_purpose)


    # layer = stage.GetEditTarget().GetLayer()
    # with Sdf.ChangeBlock():
    #     edit = Sdf.BatchNamespaceEdit()

    # if not layer.Apply(edit):
    #     raise Exception("Failed to apply layer edit!")

    # bpy.context.window_manager.USDGEState.run_hooks = False

    return True


class USDHookExample(bpy.types.USDHook):
    """Example implementation of USD IO hooks"""
    bl_idname = "usd_hook_example"
    bl_label = "Example"

    @staticmethod
    def on_export(export_context):
        do_export(export_context)
        # try:
        #     do_export(export_context)
        # except AttributeError:
        #     print("help")

