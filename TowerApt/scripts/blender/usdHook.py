import bpy
import bpy.types
from pixar import (
    Kind,
    UsdSemantics
)

RUN_HOOK = False

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


class TowerAptUSDHook(bpy.types.USDHook):
    """Example implementation of USD IO hooks"""
    bl_idname = "tower_apt_usd_hook"
    bl_label = "TowerApt USD Hook"

    @staticmethod
    def on_export(export_context):
        if RUN_HOOK == False:
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

        stack = stage.GetLayerStack()

        for prim in stage.Traverse():
            UsdSemantics.LabelsAPI.Apply(prim, "gameEntity")
            print(UsdSemantics.LabelsAPI.GetDirectTaxonomies(prim))
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
                print(prim_name)
                print(prim_type)
                prim.SetTypeName('Scope')

        return True


def register():
    bpy.utils.register_class(TowerAptUSDHook)


def unregister():
    bpy.utils.unregister_class(TowerAptUSDHook)


if __name__ == "__main__":
    register()