import bpy
from pathlib import Path
import os
import json


def GetSavedBaking(self, context):
    createdEnums = [("None", "None", "None")]
    folder = context.scene.SelectedBakeSavedFolder
    os.makedirs(folder, exist_ok=True)
    files = [f for f in os.listdir(folder)]
    for file in files:
        createdEnums.append(
            (f"{folder}/{file}", Path(file).stem, f"Current baking preset is {file}"))
    return createdEnums


def ApplyCurrentBakingPreset(self, context):
    if (context.scene.SelectedBakeSavedFolder == "None"):
        return
    try:
        with open(context.scene.SelectedBakeSavedFolder, "r+") as file:
            tempObj = json.load(file)
            context.scene.bakingList.clear()
            for property in tempObj:
                new_item = context.scene.bakingList.add()
                new_item.enabled = tempObj[property]["enabled"]
                new_item.Name = property
                new_item.Naming = tempObj[property]["Naming"]
                new_item.space = tempObj[property]["space"]
                new_item.float = tempObj[property]["float"]
                new_item.DName = tempObj[property]["DName"]
                new_item.Red=tempObj[property]["Red"]
                new_item.Green=tempObj[property]["Green"]
                new_item.Blue=tempObj[property]["Blue"]
                new_item.Invert=tempObj[property]["Invert"]
                new_item.shaderNode = tempObj[property]["shaderNode"]
                context.scene.bakingList_index = len(
                    context.scene.bakingList)-1
            setattr(context.scene, "BakePresetName", Path(file).stem)
    except:
        pass


class BAKE_PT_PANEL(bpy.types.Panel):
    bl_label = "Bake Type"
    bl_idname = "SCENE_PT_Bake_Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Manager"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.template_list("BAKING_UL_List", "", scene,
                             "bakingList", scene, "bakingListIndex")
        column = layout.column()
        presetRow = column.row()
        presetRow.prop(scene, "BakePresetName",
                       text="Baking preset name")
        presetRow.prop(scene, "SavedBakePreset",
                       text="Current packing preset")
        presetRow.operator("bake.save",
                           text="Save current baking as preset")

        channelRow = column.row()
        namingRow = column.row()
        itemList = scene.bakingList
        indexList = scene.bakingListIndex
        if itemList and indexList < len(scene.bakingList):
            channelRow.prop(
                itemList[indexList], "enabled", text="Enable", toggle=True)
            namingRow.prop(
                itemList[indexList], "naming", text="Naming convention")
            namingRow.prop(
                itemList[indexList], "space", text="color space")
            channelRow.prop(
                itemList[indexList], "float", text="32 bit texture", toggle=True)
            if(itemList[indexList].name in scene.greyScale):
                channelRow.prop(
                itemList[indexList], "Invert", text="Invert", toggle=True)
            else:
                channelRow.prop(
                itemList[indexList], "Red", text="Invert Red", toggle=True)
                channelRow.prop(
                itemList[indexList], "Green", text="Invert Green", toggle=True)
                channelRow.prop(
                itemList[indexList], "Blue", text="Invert Blue", toggle=True)


class BAKE_OT_Save(bpy.types.Operator):
    bl_idname = "bake.save"
    bl_label = "Save baking"
    bl_description = f"Save current Baking"

    def execute(self, context):

        scene = context.scene
        folder = scene.SelectedBakeSavedFolder
        tempDictionary = {}
        for bake in scene.bakingList:
            tempDictionary[bake.name] = {
                "Naming": bake.naming, "enabled": bake.enabled, "space": bake.space, "float": bake.float, "shaderNode": bake.shaderNode,"DName": bake.DName,"Red":bake.Red,"Green":bake.Green,"Blue":bake.Blue,"Invert":bake.Invert}
        os.makedirs("folder", exist_ok=True)
        with open(f"./{folder}/{scene.BakePresetName}.json", "w") as jsonFile:
            json.dump(tempDictionary, jsonFile)
        return {'FINISHED'}


class CREATE_OT_BAKE(bpy.types.Operator):
    bl_idname = "create.bake"
    bl_label = "Create bake"

    def execute(self, context):

        scene = context.scene
        for name in scene.BakeTypes:
            new_item = scene.bakingList.add()
            new_item.name = name
            new_item.naming = f"[Object]_{new_item.name}"
            new_item.DName = scene.BakeTypes[name]
            new_item.shaderNode = scene.inputNodeNamesUi[name]
            scene.bakingListIndex = len(scene.bakingList)-1
            if (name in scene.ColorMaps):
                new_item.space = "sRGB"
            else:
                new_item.space = "Non-Color"
        return {'FINISHED'}


class BAKING_UL_List(bpy.types.UIList):
    bl_idname = "BAKING_UL_List"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.DName, icon=item.icon)
        layout.label(text=item.shaderNode)


class BakeObject(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Item Name", default="New Item")
    icon: bpy.props.StringProperty(name="Icon", default="TEXTURE")
    space: bpy.props.EnumProperty(name="Color Space", description="Color space of the texture", items=[('ACES2065-1', 'ACES2065-1', 'Color space ACES2065-1'), ('ACEScg', 'ACEScg', 'Color space ACEScg'), ('AgX Base Display P3', 'AgX Base Display P3', 'Color space AgX Base Display P3'), ('AgX Base Rec.1886', 'AgX Base Rec.1886', 'Color space AgX Base Rec.1886'), ('AgX Base Rec.2020', 'AgX Base Rec.2020', 'Color space AgX Base Rec.2020'), ('AgX Base sRGB', 'AgX Base sRGB', 'Color space AgX Base sRGB'), ('AgX Log', 'AgX Log', 'Color space AgX Log'), ('Display P3', 'Display P3', 'Color space Display P3'), ('Filmic Log', 'Filmic Log', 'Color space Filmic Log'), ('Filmic sRGB', 'Filmic sRGB', 'Color space Filmic sRGB'), (
        'Khronos PBR Neutral sRGB', 'Khronos PBR Neutral sRGB', 'Color space Khronos PBR Neutral sRGB'), ('Linear CIE-XYZ D65', 'Linear CIE-XYZ D65', 'Color space Linear CIE-XYZ D65'), ('Linear CIE-XYZ E', 'Linear CIE-XYZ E', 'Color space Linear CIE-XYZ E'), ('Linear DCI-P3 D65', 'Linear DCI-P3 D65', 'Color space Linear DCI-P3 D65'), ('Linear FilmLight E-Gamut', 'Linear FilmLight E-Gamut', 'Color space Linear FilmLight E-Gamut'), ('Linear Rec.2020', 'Linear Rec.2020', 'Color space Linear Rec.2020'), ('Linear Rec.709', 'Linear Rec.709', 'Color space Linear Rec.709'), ('Non-Color', 'Non-Color', 'Color space Non-Color'), ('Rec.1886', 'Rec.1886', 'Color space Rec.1886'), ('Rec.2020', 'Rec.2020', 'Color space Rec.2020'), ('sRGB', 'sRGB', 'Color space sRGB')])
    naming: bpy.props.StringProperty(name="Item Name", default="[Object]_Bake",
                                     description="Specify the name and use the following notation for dynamic value\n[Object]=Object name\n[mat]=material name\n[Num]=A number generated if a image with the same name exist(if not specified and a image with the same name exist, then a number would added at the end)")
    enabled: bpy.props.BoolProperty(
        name="Enable Bake", default=False, description="Click to enable baking this")
    float: bpy.props.BoolProperty(
        name="32 bit", default=False, description="32 bit texture")
    shaderNode: bpy.props.StringProperty(
        name="Shader Node", default="BSDF_PRINCIPLED", description="Shader node type")
    DName: bpy.props.StringProperty(
        name="Display name", default="BSDF_PRINCIPLED", description="Display name of bake type")
    Red:bpy.props.BoolProperty(name="Invert Red",default=False,description="Invert red channel")
    Green:bpy.props.BoolProperty(name="Invert Green",default=False,description="Invert red channel")
    Blue:bpy.props.BoolProperty(name="Invert Blue",default=False,description="Invert red channel")
    Invert:bpy.props.BoolProperty(name="Invert",default=False,description="Invert the texture")
listOfClassSecond = [BAKE_OT_Save, BAKE_PT_PANEL,
                     BAKING_UL_List, CREATE_OT_BAKE]
class_register_second, class_unregister_second = bpy.utils.register_classes_factory(
    listOfClassSecond)
listOfClassfFirst = [BakeObject]
class_register_first,  class_unregister_first = bpy.utils.register_classes_factory(
    listOfClassfFirst)


def Register():
    class_register_first()
    bpy.types.Scene.bakingList = bpy.props.CollectionProperty(
        type=BakeObject)
    bpy.types.Scene.bakingListIndex = bpy.props.IntProperty(default=0)

    bpy.types.Scene.SavedBakePreset = bpy.props.EnumProperty(
        name="prefix preset", description="current baking preset", items=GetSavedBaking, update=ApplyCurrentBakingPreset)
    bpy.types.Scene.BakePresetName = bpy.props.StringProperty(
        name="", default="", description="Enter the name of current baking preset to be saved")
    class_register_second()
    bpy.ops.create.bake()

    ApplyCurrentBakingPreset(None, bpy.context)


def Unregister():
    del bpy.types.Scene.BakePresetName
    del bpy.types.Scene.SavedBakePreset
    del bpy.types.Scene.bakingList
    del bpy.types.Scene.bakingListIndex
    class_unregister_first()
    class_unregister_second()


Register()
