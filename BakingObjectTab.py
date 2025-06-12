import bpy


def ChangeToNone(self, context):
    if (not self.useActiveToSelected):
        self.selected = None
        self.useCage = False
    if (not self.useCage):
        self.cage = None
def GetUv(self,context):
    uvList = []
    if (self.mesh and self.mesh.type == "MESH"):
        for uv in self.mesh.data.uv_layers:
            uvList.append((uv.name, uv.name, uv.name))
    return uvList

class MyItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Item Name", default="New Item")
    icon: bpy.props.StringProperty(name="Icon", default="OBJECT_DATAMODE")
    mesh: bpy.props.PointerProperty(type=bpy.types.Object)
    cage: bpy.props.PointerProperty(type=bpy.types.Object)
    selected: bpy.props.PointerProperty(type=bpy.types.Object)
    useActiveToSelected: bpy.props.BoolProperty(
        name="Selected To active", default=False, update=ChangeToNone)
    useCage: bpy.props.BoolProperty(
        name="Cage Object", default=False, update=ChangeToNone)
    uv:bpy.props.EnumProperty(name="UV Map",description="Uv To use for baking",items=GetUv)


class MY_UL_List(bpy.types.UIList):
    bl_idname = "MY_UL_List"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name, icon=item.icon)


class BAKING_PT_LIST(bpy.types.Panel):
    bl_label = "Baking Object List"
    bl_idname = "SCENE_PT_OBJECT_Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Manager"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.template_list("MY_UL_List", "", scene,
                             "my_items", scene, "my_items_index")
        column = layout.column()
        addRemoveRow = column.row()
        addRemoveRow.operator("my_list.add_item", text="Add Item", icon="ADD")
        addRemoveRow.operator("my_list.remove_item",
                              text="Remove Item", icon="REMOVE")
        selectionCheckBox = column.row()
        uvRow = column.row()
        if scene.my_items and scene.my_items_index < len(scene.my_items):
            uvRow.prop(scene.my_items[scene.my_items_index], 'uv', text="UV Map")
            selectionCheckBox.prop(scene.my_items[scene.my_items_index], 'useActiveToSelected',
                                   text="Use Active to Selected")
            if (scene.my_items[scene.my_items_index].useActiveToSelected):
                selectObject = column.row()
                selectObject.prop(
                    scene.my_items[scene.my_items_index], 'selected')
                cageCheckBox = column.row()
                cageCheckBox.prop(scene.my_items[scene.my_items_index], 'useCage',
                                  text="Use Cage")
                if (scene.my_items[scene.my_items_index].useCage):
                    cageObject = column.row()
                    cageObject.prop(
                        scene.my_items[scene.my_items_index], 'cage')


class Baking_OT_AddObject(bpy.types.Operator):
    bl_idname = "my_list.add_item"
    bl_label = "Add Item"

    def execute(self, context):
        scene = context.scene
        for mesh in bpy.context.selected_objects:
            if ((mesh.type == "MESH" and (len(mesh.data.materials) > 0)) and not any(mesh == exisitingMesh.mesh for exisitingMesh in scene.my_items)):
                new_item = scene.my_items.add()
                new_item.name = mesh.name
                new_item.icon = "MESH_CUBE"
                new_item.mesh = mesh
                new_item.selected = None
                new_item.cage = None
                new_item.uv=mesh.data.uv_layers.active.name
        scene.my_items_index = len(scene.my_items)-1
        return {'FINISHED'}


class Baking_OT_RemoveObject(bpy.types.Operator):
    bl_idname = "my_list.remove_item"
    bl_label = "Remove Item"

    def execute(self, context):
        scene = context.scene
        if scene.my_items:
            scene.my_items.remove(scene.my_items_index)
            scene.my_items_index = max(0, scene.my_items_index - 1)
        return {'FINISHED'}


listOfClass = [MyItem, MY_UL_List, BAKING_PT_LIST,
               Baking_OT_AddObject, Baking_OT_RemoveObject]
class_register, class_unregister = bpy.utils.register_classes_factory(
    listOfClass)

def ObjectExist(scene):
    if (scene.my_items and len(scene.my_items) > 0):
        idexes = len(scene.my_items)
        for index in range(idexes):
            if (scene.my_items[index].mesh.name not in scene.objects):
                scene.my_items_index=index
                bpy.ops.my_list.remove_item()
            if (scene.my_items[index].useActiveToSelected and scene.my_items[index].selected.name not in scene.objects):
                scene.my_items[index].selected=None
            if (scene.my_items[index].useCage and scene.my_items[index].cage.name not in scene.objects):
                scene.my_items[index].cage=None
    
def Register():
    class_register()
    bpy.types.Scene.my_items = bpy.props.CollectionProperty(type=MyItem)
    bpy.types.Scene.my_items_index = bpy.props.IntProperty(default=0)
    if ObjectExist not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(ObjectExist)


def Unregister():
    class_unregister()
    del bpy.types.Scene.my_items
    del bpy.types.Scene.my_items_index
    if ObjectExist in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(ObjectExist)


Register()
