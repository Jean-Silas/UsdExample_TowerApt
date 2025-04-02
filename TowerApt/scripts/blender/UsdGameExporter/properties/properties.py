import bpy
from bpy.types import PropertyGroup

class USDGEExportCollectionProps(PropertyGroup):
    process: bpy.props.BoolProperty(
        name="Process Collection",
        description="Perform collection-level processing when performing a USD export",
        default=False,
        options={'SKIP_SAVE'}
    ) # type: ignore

    # TODO: Add pointer to base prim
    is_variant_set: bpy.props.BoolProperty(
        name="Is Variant Set",
        description="Treat the collection contents as a variant set",
        default=False,
        options={'SKIP_SAVE'}
    ) # type: ignore

    kind: bpy.props.EnumProperty(
        name="Model Kind",
        description="The Kind of the object in the USD hierarchy",
        items = [
            ('NOKIND', "None", "No", 'NONE', 1),
            # Core model kinds that match the USD spec
            ('ASSEMBLY', "Assembly", "A group that defines a Primary Asset", 'NONE', 2),
            ('GROUP', "Group", "A generic group", 'NONE', 3),
            ('COMPONENT', "Component", "a 'leaf model' that can contain no other models", 'NONE', 4),
            ('SUBCOMPONENT', "Subcomponent", "An important part of a component", 'NONE', 5),
            
            # Pixar doesn't really define what a scope is
            # ('SCOPE', "Scope", "An abstract group that doesn't have a transform", 'NONE', 5),
            # ('OTHER', "Other", "Something Else", 'NONE', 4), 


            # ('VARIANT', "Variant", "An Asset Variant", 'NONE', 6),
        ],
        options={'SKIP_SAVE'},
        default='COMPONENT'
    ) # type: ignore


class USDGEExportObjectProps(PropertyGroup):

    status: bpy.props.EnumProperty(
        name="Export Status",
        description="How the exporter will treat this object",
        items = [
            ('INHERIT',          "Inherit", "Inherit from parent", 'NONE', 1),
            
            ('EXPORT',           "Export", "This object, but not its children, will be exported", 'NONE', 2),
            ('EXPORT_RECURSIVE', "Export Recursive", "This object, and it's children, will be exported", 'NONE', 3),

            ('EXCLUDE',          "Exclude", "This object will not be exported", 'NONE', 4),
            ('PASSTHROUGH',      "Passthrough", "This object's children will be exported, but it will not", 'NONE', 5)
        ],
        options={'SKIP_SAVE'}
    ) # type: ignore

    kind: bpy.props.EnumProperty(
        name="Model Kind",
        description="The Kind of the object in the USD hierarchy",
        items = [
            ('NOKIND', "None", "No", 'NONE', 1),
            # Core model kinds that match the USD spec
            ('ASSEMBLY', "Assembly", "A group that defines a Primary Asset", 'NONE', 2),
            ('GROUP', "Group", "A generic group", 'NONE', 3),
            ('COMPONENT', "Component", "a 'leaf model' that can contain no other models", 'NONE', 4),
            ('SUBCOMPONENT', "Subcomponent", "An important part of a component", 'NONE', 5),
            
            # Pixar doesn't really define what a scope is
            # ('SCOPE', "Scope", "An abstract group that doesn't have a transform", 'NONE', 5),
            # ('OTHER', "Other", "Something Else", 'NONE', 4), 


            # ('VARIANT', "Variant", "An Asset Variant", 'NONE', 6),
        ],
        options={'SKIP_SAVE'}
    ) # type: ignore

    # Inspired by https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html#annotated-asset-structures
    # Assemblies seem to be where studios like to express structural sub-kinds
    assembly_subkind: bpy.props.EnumProperty(
        name="Assembly Subkind",
        description="The rendering role of the object in the USD hierarchy",
        items = [
            ('NONE', "None", "Just an assembly", 'NONE', 1),
            # https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html#atomic-model-structure-flowerpot
            ('ATOMIC', "Atomic", "An assembly with no external dependencies", 'NONE', 2),
            # https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html#package-model-structure-apartmentbuilding-pkg
            ('BUNDLE', "Bundle", "An assembly 'adorned' with additional imagable prims", 'NONE', 3),
            # https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html#aggregate-model-structure-neighborhood
            ('AGGREGATE', "Aggregate", "A 'pure' assembly ", 'NONE', 4),

        ],
        options={'SKIP_SAVE'}
    ) # type: ignore

    purpose: bpy.props.EnumProperty(
        name="Purpose",
        description="The rendering role of the object in the USD hierarchy",
        items = [
            ('INHERIT', "Inherit", "Inherit purpose from parent", 'NONE', 1),
            ('RENDER', "Render", "High quality render mesh", 'NONE', 2),
            ('PROXY', "Proxy", "Low quality preview mesh", 'NONE', 3),
            ('GUIDE', "Guide", "Editor-only visualization mesh", 'NONE', 4)
        ],
        options={'SKIP_SAVE'}
    ) # type: ignore

    convert_to: bpy.props.EnumProperty(
        name="Convert To",
        description="The prim type to convert this object into after export",
        items = [
            ('NONE', "None", "Do not convert", 'NONE', 1),
            ('SCOPE', "Scope", "Convert prim to scope after export", 'NONE', 2),
            ('SOCKET', "Constraint Target", "Prune the prim and convert its transform into a constraint target on its parent", 'NONE', 3),
            ('SUBSET', "Geometry Subset", "Merge with siblings and convert to GeomSubset", 'NONE', 2),
        ],
        options={'SKIP_SAVE'}
    ) # type: ignore

    # Deprecated
    # flatten: bpy.props.BoolProperty(
    #     name="Flatten Object Transform",
    #     description="Flatten the object transform onto the object data block in the USD hierarchy",
    #     default=True,
    #     options={'SKIP_SAVE'}
    # ) # type: ignore

    # Deprecated
    # Probably a bad idea
    # swizzle_as_layer: bpy.props.BoolProperty(
    #     name="Apply Swizzle As Layer",
    #     description="Apply the swizzle transform as a separate layer",
    #     default=False,
    #     options={'SKIP_SAVE'}
    # ) # type: ignore

    # Deprecated
    # auto_exclude_pattern: bpy.props.StringProperty(
    #     name="Auto-Exclude Pattern",
    #     description="Regex pattern for automatically excluding children by name",
    #     default="CUTTER",
    #     options={'SKIP_SAVE'}
    # ) # type: ignore

    auto_exclude_types: bpy.props.EnumProperty(
        name="Auto-Exclude Types",
        description="Object types to automatically exlude",
        items = [
            ('MESH',   "Mesh",   "", 'NONE',  1),
            ('CURVE',  "Curve",  "", 'NONE',  2),
            ('LIGHT',  "Light",  "", 'NONE',  4),
            ('CAMERA', "Camera", "", 'NONE',  8),
            ('TEXT',   "Text",   "", 'NONE', 16),
        ],
        options={ 'ENUM_FLAG'}
    ) # type: ignore

    # Deprecated
    # name_override: bpy.props.StringProperty(
    #     name="Name Override",
    #     description="Optional name override, use to circumvent Blender's lack of namespacing",
    #     default="",
    #     options={'SKIP_SAVE'}
    # ) # type: ignore

    # Deprecated
    # path_override: bpy.props.StringProperty(
    #     name="Path Override",
    #     description="Optional path override, use to manually position the object in the USD hierarchy",
    #     default="",
    #     options={'SKIP_SAVE'}
    # ) # type: ignore

# Deprecated
# class USDGEExportFileProps(PropertyGroup):
#     split: bpy.props.BoolProperty(
#         name="Split Components",
#         description="Export Components as separate files",
#         default=False,
#         options={'SKIP_SAVE'}
#     ) # type: ignore


class USDGEExportStateProps(PropertyGroup):
    run_hooks: bpy.props.BoolProperty(
        name="Run Hooks",
        description="The USD hooks poll this variable to see if they should run",
        default=False,
        options={'SKIP_SAVE'}
    ) # type: ignore

    # TL;DR: A very rudimentary staging location for pre/post functions.
    #        While I could technically monkey patch them into the operator itself,
    #        that approach is too brittle, and does a poor job of demonstrating the
    #        core premise. Longterm, I'll build out a proper callgroup manager.
    # pre_hooks:  list[function] = []
    # post_hooks: list[function] = []


OUT = [
    USDGEExportCollectionProps,
    USDGEExportObjectProps,
    USDGEExportStateProps
]