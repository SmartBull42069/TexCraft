import bpy
from bpy_extras.io_utils import ImportHelper
import os
import json
from pathlib import Path


def GetChannel(self, context):
    scene = context.scene
    tempList = [("None", "None", "None")]
    for texture in scene.BakeTypes:
        if(texture in scene.greyScale):
            tempList.append((f"{texture}", f"{texture}", f"Pack {texture}"))
    return tempList


class MyPackedObject(bpy.types.PropertyGroup):
    
    name: bpy.props.StringProperty(name="Item Name", default="New Item")
    icon: bpy.props.StringProperty(name="Icon", default="TEXTURE")
    Red: bpy.props.EnumProperty(name="Red", description="Red channel",
                                items=GetChannel, default=1,)
    Green: bpy.props.EnumProperty(name="Red", description="Green channel",
                                  items=GetChannel, default=1)
    Blue: bpy.props.EnumProperty(name="Red", description="Blue channel",
                                 items=GetChannel, default=1)
    Alpha: bpy.props.EnumProperty(name="Red", description="Alpha channel",
                                  items=GetChannel, default=1)
    naming: bpy.props.StringProperty(name="Item Name", default="[Object]_PackedTexture",
                                     description="Specify the name and use the following notation for dynamic value\n[Object]=Object name\n[mat]=material name\n[Num]=A number generated if a image with the same name exist(if not specified and a image with the same name exist, then a number would added at the end)")
    space : bpy.props.EnumProperty(name="Color Space", description="Color space of the texture", items=[('ACES2065-1', 'ACES2065-1', 'Color space ACES2065-1'), ('ACEScg', 'ACEScg', 'Color space ACEScg'), ('AgX Base Display P3', 'AgX Base Display P3', 'Color space AgX Base Display P3'), ('AgX Base Rec.1886', 'AgX Base Rec.1886', 'Color space AgX Base Rec.1886'), ('AgX Base Rec.2020', 'AgX Base Rec.2020', 'Color space AgX Base Rec.2020'), ('AgX Base sRGB', 'AgX Base sRGB', 'Color space AgX Base sRGB'), ('AgX Log', 'AgX Log', 'Color space AgX Log'), ('Display P3', 'Display P3', 'Color space Display P3'), ('Filmic Log', 'Filmic Log', 'Color space Filmic Log'), ('Filmic sRGB', 'Filmic sRGB', 'Color space Filmic sRGB'), (
        'Khronos PBR Neutral sRGB', 'Khronos PBR Neutral sRGB', 'Color space Khronos PBR Neutral sRGB'), ('Linear CIE-XYZ D65', 'Linear CIE-XYZ D65', 'Color space Linear CIE-XYZ D65'), ('Linear CIE-XYZ E', 'Linear CIE-XYZ E', 'Color space Linear CIE-XYZ E'), ('Linear DCI-P3 D65', 'Linear DCI-P3 D65', 'Color space Linear DCI-P3 D65'), ('Linear FilmLight E-Gamut', 'Linear FilmLight E-Gamut', 'Color space Linear FilmLight E-Gamut'), ('Linear Rec.2020', 'Linear Rec.2020', 'Color space Linear Rec.2020'), ('Linear Rec.709', 'Linear Rec.709', 'Color space Linear Rec.709'), ('Non-Color', 'Non-Color', 'Color space Non-Color'), ('Rec.1886', 'Rec.1886', 'Color space Rec.1886'), ('Rec.2020', 'Rec.2020', 'Color space Rec.2020'), ('sRGB', 'sRGB', 'Color space sRGB')], default="Non-Color")
    float:bpy.props.BoolProperty(name="32 bit",default=False,description="32 bit texture")

class PACKING_UL_List(bpy.types.UIList):
    bl_idname = "PACKING_UL_List"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # layout.prop(item, "name", icon=item.icon, text="")
        layout.label(text=item.name, icon=item.icon)


class PACKING_PT_LIST(bpy.types.Panel):
    bl_label = "Packing"
    bl_idname = "SCENE_PT_Packing_Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Manager"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.template_list("PACKING_UL_List", "", scene,
                             "my_Packed_Object", scene, "my_Packed_Object_index")
        column = layout.column()
        addRemoveRow = column.row()
        addRemoveRow.operator("packed.add_texture",
                              text="Add Texture", icon="ADD")
        addRemoveRow.operator("packed.remove_texture",
                              text="Remove Texture", icon="REMOVE")
        presetRow = column.row()
        presetRow.prop(scene, "current_packing_preset_name",
                       text="Packing preset name")
        presetRow.prop(scene, "current_packing_preset",
                       text="Current packing preset")
        presetRow.operator("packing.save",
                           text="Save current packing as preset")

        channelRow = column.row()
        namingRow = column.row()
        if scene.my_Packed_Object and scene.my_Packed_Object_index <= len(scene.my_Packed_Object):
            channelRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "Red", text="Red")
            channelRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "Green", text="Green")
            channelRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "Blue", text="Blue")
            channelRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "Alpha", text="Alpha")
            namingRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "naming", text="Naming convention")
            namingRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "name", text="Name")
            namingRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "space", text="Color space")
            namingRow.prop(
                scene.my_Packed_Object[scene.my_Packed_Object_index], "float", text="32 bit",toggle=True)
class Paking_OT_AddObject(bpy.types.Operator):
    bl_idname = "packed.add_texture"
    bl_label = "Add texture"

    def execute(self, context):
        scene = context.scene
        new_item = scene.my_Packed_Object.add()
        new_item.Red = "None"
        new_item.Green = "None"
        new_item.Blue = "None"
        new_item.Alpha = "None"
        scene.my_Packed_Object_index = len(scene.my_Packed_Object)-1
        return {'FINISHED'}


class Paking_OT_RemoveObject(bpy.types.Operator):
    bl_idname = "packed.remove_texture"
    bl_label = "Remove texture"

    def execute(self, context):
        scene = context.scene
        if scene.my_Packed_Object:
            scene.my_Packed_Object.remove(scene.my_Packed_Object_index)
            scene.my_Packed_Object_index = max(
                0, scene.my_Packed_Object_index - 1)
        return {'FINISHED'}


def GetSavedPackingPreset(self, context):
    createdEnums = [("None", "None", "None")]
    folder = context.scene.PackedSavedFolder
    os.makedirs(folder, exist_ok=True)
    files = [f for f in os.listdir(folder)]
    for file in files:
        createdEnums.append(
            (f"{folder}/{file}", Path(file).stem, f"Current setting is {file}"))
    return createdEnums


def ApplyCurrentPacking(self, context):
    if (context.scene.current_packing_preset == "None"):
        return
    try:
        with open(context.scene.current_packing_preset, "r+") as file:
            tempObj = json.load(file)
            context.scene.my_Packed_Object.clear()
            for property in tempObj:
                new_item = context.scene.my_Packed_Object.add()
                new_item.Red = tempObj[property]["Red"]
                new_item.Green = tempObj[property]["Green"]
                new_item.Blue = tempObj[property]["Blue"]
                new_item.Alpha = tempObj[property]["Alpha"]
                new_item.Name = property
                new_item.Naming = tempObj[property]["Naming"]
                new_item.space = tempObj[property]["space"]
                new_item.float = tempObj[property]["float"]
                context.scene.my_Packed_Object_index = len(
                    context.scene.my_Packed_Object)-1
            setattr(context.scene, "current_packing_preset_name", Path(file).stem)
    except:
        pass


class Packing_OT_Save(bpy.types.Operator):
    bl_idname = "packing.save"
    bl_label = "Save packing"
    bl_description = f"Save current packing "

    def execute(self, context):

        scene = context.scene
        folder = scene.PackedSavedFolder
        tempDict = {}
        for packedObject in scene.my_Packed_Object:
            tempDict[packedObject.name] = {
                "Red": packedObject.Red, "Green": packedObject.Green, "Blue": packedObject.Blue, "Alpha": packedObject.Alpha, "Naming": packedObject.Naming, "space": packedObject.space, "float": packedObject.float}
        os.makedirs("folder", exist_ok=True)
        with open(f"./{folder}/{scene.current_packing_preset_name}.json", "w") as jsonFile:
            json.dump(tempDict, jsonFile)
        scene.current_packing_preset = f"{folder}/{scene.current_packing_preset_name}.json"
        return {'FINISHED'}


listOfClass = [MyPackedObject, PACKING_UL_List, PACKING_PT_LIST,
               Paking_OT_AddObject, Paking_OT_RemoveObject, Packing_OT_Save]
class_register, class_unregister = bpy.utils.register_classes_factory(
    listOfClass)


def Register():
    class_register()
    bpy.types.Scene.current_packing_preset_name = bpy.props.StringProperty(
        name="Packing preset name", description="Enter the name of current packing preset to be saved")
    bpy.types.Scene.current_packing_preset = bpy.props.EnumProperty(
        name="Current packing preset", description="Current packing preset", update=ApplyCurrentPacking, items=GetSavedPackingPreset)
    bpy.types.Scene.my_Packed_Object = bpy.props.CollectionProperty(
        type=MyPackedObject)
    bpy.types.Scene.my_Packed_Object_index = bpy.props.IntProperty(default=0)
    ApplyCurrentPacking(None, bpy.context)


def Unregister():
    class_unregister()
    del bpy.types.Scene.current_packing_preset_name
    del bpy.types.Scene.my_Packed_Object
    del bpy.types.Scene.my_Packed_Object_index


Register()
