import bpy
from bpy_extras.io_utils import ExportHelper


# TODO: Implement name and type filtering here
def recursively_select_children(obj):
    for child in obj.children:
        if child.USDGE.status in ('INHERIT'):
            child.select_set(True)
            recursively_select_children(child)

        elif child.USDGE.status in ('EXPORT'):
            child.select_set(True)

        elif child.USDGE.status in ('PASSTHROUGH'):
            recursively_select_children(child)

class USDGE_OT_Export(bpy.types.Operator):
    """Export the tagged assets as USD Files"""
    bl_idname = "usdge.export"
    bl_label = "USDGE USD Export"
    bl_options = {'REGISTER', 'PRESET'}

    # TL;DR: where the staged functions from USDGEExportStateProps end up.
    # pre_hooks:  list[function] = []
    # post_hooks: list[function] = []

    # ExportHelper mix-in class uses this.
    filename_ext = ".usd"

    filter_glob: bpy.props.StringProperty(
        default="*.usd",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )  # type: ignore

    directory: bpy.props.StringProperty(
        subtype='DIR_PATH')  # type: ignore

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Filepath used for importing the file",
        maxlen=1024,
        subtype='FILE_PATH',
    )  # type: ignore


    filter_by_viewlayer: bpy.props.BoolProperty(
        name = "Filter by View Layer",
        description = "Ignore tagged assets that aren't in the current view layer",
        default = False
    )  # type: ignore


    base_kind: bpy.props.EnumProperty(
        name="Root Prim Model Kind",
        description="The Kind applied to the root object in the exported scene",
        items = [
            # Core model kinds that match the USD spec
            ('ASSEMBLY', "Assembly", "A group that defines a Primary Asset", 'NONE', 1),
            ('GROUP', "Group", "A generic group", 'NONE', 2),
            ('COMPONENT', "Component", "a 'leaf model' that can contain no other models", 'NONE', 3),
            ('SUBCOMPONENT', "Subcomponent", "An important part of a component", 'NONE', 4),
            
            # Pixar doesn't really define what a scope is
            ('SCOPE', "Scope", "An abstract group that doesn't have a transform", 'NONE', 5),
            # ('OTHER', "Other", "Something Else", 'NONE', 4), 


            ('VARIANT', "Variant", "An Asset Variant", 'NONE', 6),
        ],
        options={'SKIP_SAVE'}
    ) # type: ignore


    splitting_rule: bpy.props.EnumProperty(
        name="Splitting Rule",
        description="Rule used for separating export into multiple files",
        items = [
            # Core model kinds that match the USD spec
            ('ASSEMBLY', "Split by Assembly", "Separate by Assembly", 'NONE', 1),
            ('GROUP', "Split by Group", "Separate by Group", 'NONE', 2),
            ('COMPONENT', "Split by Component", "Separate by Component", 'NONE', 3),
            ('COLLECTION', "Split by Collection", "Separate by Collection", 'NONE', 3),
            ('NO_SPLIT', "Don't Split", "", 'NONE', 4),
        ],
        options={'SKIP_SAVE'}
    ) # type: ignore


    auto_exclude_pattern: bpy.props.StringProperty(
        name="Auto-Exclude Pattern",
        description="Regex pattern for automatically excluding children by name",
        default="CUTTER",
        options={'SKIP_SAVE'}
    ) # type: ignore

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

    override_child_exclude_pattern: bpy.props.BoolProperty(
        name = "Override Child Exclude Patterns",
        description = "Ignore the override pattern settings of children",
        default = False
    ) # type: ignore

    override_child_exclude_types: bpy.props.BoolProperty(
        name = "Override Child Exclude Types",
        description = "Ignore the override pattern settings of children",
        default = False
    ) # type: ignore

    include_children_with_own_exporters: bpy.props.BoolProperty(
        name = "Include Children With Own Exporters",
        description = "Include child collections that have their own USDGE Exporter configurations",
        default = False
    ) # type: ignore



    def draw(self, context):
        layout = self.layout

        # SECTION: General

        header, body = layout.panel("USDGE_Exporter_General", default_closed=False)
        header.label(text="General")
        if body:
            body.use_property_split = True

            body.prop(
                self,
                "include_children_with_own_exporters"
            )
            body.prop(
                self,
                "splitting_rule"
            )

            body.prop(
                self,
                "auto_exclude_pattern"
            )

            body.prop(
                self,
                "auto_exclude_types"
            )

            body.prop(
                self,
                "filter_by_viewlayer"
            )
            body.prop(
                self,
                "override_child_exclude_pattern"
            )
            body.prop(
                self,
                "override_child_exclude_types"
            )

        # SECTION: Validation
        header, body = layout.panel("USDGE_Exporter_Validation", default_closed=False)
        header.label(text="Validation")
        if body:
            body.label(text="Put an operator here")

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')

        direct_export = []
        recursive_export = []

        for obj in context.scene.objects:
            if obj.USDGE.status == 'EXPORT':
                direct_export.append(obj)
                obj.select_set(True)
            elif obj.USDGE.status == 'EXPORT_RECURSIVE':
                recursive_export.append(obj)
                obj.select_set(True)
                recursively_select_children(obj)

        print(direct_export)
        print(recursive_export)

        context.window_manager.USDGEState.run_hooks = True

        result = bpy.ops.wm.usd_export(
            'INVOKE_SCREEN', True,
            selected_objects_only=True,
            root_prim_path="",
            evaluation_mode='RENDER'
        )

        return result
        # return {'FINISHED'}
        ...

class USDGE_FH_usd_export(bpy.types.FileHandler):
    bl_idname = "USDGE_FH_usd_export"
    bl_label = "USDGE Export"
    bl_export_operator = "USDGE.export"
    bl_file_extensions = ".usd"

    @classmethod
    def poll_drop(cls, context):
        return (context.area and context.area.type == 'VIEW_3D')


OUT = [
    USDGE_OT_Export,
    USDGE_FH_usd_export
]