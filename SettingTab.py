import bpy
from bpy_extras.io_utils import ImportHelper
import os
import json
from pathlib import Path


def ApplyCurrentSetting(self, context):
    if (context.scene.SavedSettings=="None"):
        return
    try:
        with open(context.scene.SavedSettings, "r+") as file:
            tempObj = json.load(file)
            for property in tempObj:
                setattr(context.scene, property, tempObj[property])
            setattr(context.scene, "settingName", Path(file).stem)
    except:
        pass


def getSavedSetting(self, context):
    createdEnums = [("None","None","None")]
    folder = context.scene.SavedSettingFolder
    os.makedirs(folder, exist_ok=True)
    files = [f for f in os.listdir(folder)]
    for file in files:
        createdEnums.append(
            (f"{folder}\\{file}", Path(file).stem, f"Current setting is {file}"))
    return createdEnums


def SetFolderTreeDefault(self, context):
    if (not context.scene.UseCustomFolderTree):
        context.scene.FolderTree = "[bakeType]"


def SetCopiedMaterialDefault(self, context):
    if (not context.scene.CopyMaterial):
        context.scene.CopiedMaterialName = ""




class SETTING_PT_PANEL(bpy.types.Panel):
    bl_label = "Settings"
    bl_idname = "SCENE_PT_Setting_Manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Manager"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        column = layout.column()
        numOfItem = list(scene.settingsNames.keys())
        for i in range(0, len(numOfItem), 3):
            settingNames = numOfItem[i:i+3]
            row = column.row()
            for names in settingNames:
                row.prop(
                    scene, names, toggle=True, text=scene.settingsNames[names])
        column.separator()
        currentSettingRow = column.row()
        currentSettingRow.prop(scene, "settingName", text="preset")
        currentSettingRow.prop(scene, "SavedSettings", text="Current setting")
        filePathRow = column.row()
        filePathRow.operator("basepath.open_filebrowser",
                             text="Texture path", icon="FILEBROWSER")
        saveSetting = column.row()
        saveSetting.operator("setting.save", text="Save current setting")
        if (scene.UseCustomFolderTree):
            customFolderRow = column.row()
            customFolderRow.prop(
                scene, "FolderTree")
        if (scene.CopyMaterial):
            materialNameRow = column.row()
            materialNameRow.prop(
                scene, "CopiedMaterialName")


class Setting_OT_Save(bpy.types.Operator):
    bl_idname = "setting.save"
    bl_label = "Save setting"
    bl_description = f"Save current setting "

    def execute(self, context):

        scene = context.scene
        folder = scene.SavedSettingFolder
        tempDictionary = {}
        for setting in scene.settingsNames:
            settingValue = getattr(
                scene, setting)
            tempDictionary[setting] = settingValue
        os.makedirs("folder", exist_ok=True)
        with open(f"{folder}\\{scene.settingName}.json", "w") as jsonFile:
            json.dump(tempDictionary, jsonFile)
        scene.SavedSettings = f"{folder}\\{scene.settingName}.json"
        return {'FINISHED'}


class OT_BasePath(bpy.types.Operator, ImportHelper):
    bl_idname = "basepath.open_filebrowser"
    bl_label = "Select"
    filter_glob: bpy.props.StringProperty(
        default='',
        options={'HIDDEN'})
    bl_description = "Select the base folder for saving baked texture"

    def execute(self, context):
        context.scene.basePath = self.filepath
        return {'FINISHED'}


listOfClass = [SETTING_PT_PANEL, OT_BasePath, Setting_OT_Save]
class_register, class_unregister = bpy.utils.register_classes_factory(
    listOfClass)


def RegisterSettingTab():
    class_register()
    settingPropertyRegister()


def settingPropertyRegister():

    
    bpy.types.Scene.settingName = bpy.props.StringProperty(
        name="preset", default="Setting1", description="Enter the name of current setting to be saved")
    bpy.types.Scene.margin = bpy.props.IntProperty(
        name="Texture margin", default=16, description="Margin of texture", min=0, max=64)
    bpy.types.Scene.height = bpy.props.IntProperty(
        name="Texture Height", default=1024, description="Height of texture", min=1024)
    bpy.types.Scene.extrusion = bpy.props.IntProperty(
        name="Extrusion", default=0, description="Max extrusion to use for baking selected to active", min=0, max=1)
    bpy.types.Scene.rayDistance = bpy.props.IntProperty(
        name="Ray distance", default=0, description="Max raydistance to use for baking selected to active", min=0, max=1)
    bpy.types.Scene.SavedSettings = bpy.props.EnumProperty(
        name="Saved settings", description="Settings", items=getSavedSetting, update=ApplyCurrentSetting)

    bpy.types.Scene.width = bpy.props.IntProperty(
        name="Texture Width", default=1024, description="Width of texture", min=1024)
    bpy.types.Scene.ShadeSmooth = bpy.props.BoolProperty(
        name="Shade Smooth", default=False, description="Turn this on to shade smooth")
    bpy.types.Scene.CopiedMaterialName = bpy.props.StringProperty(
        name="Copied Material Name", default="", description="Specify the name and use the following notation for dynamic value\n[Object]=Object name\n[mat]=material name\n leaving this field empty will add a incrementing number for each copied material")

    bpy.types.Scene.UseCustomFolderTree = bpy.props.BoolProperty(
        name="Use custom folder tree", default=False, description="Turn this on to specify custom folder tree", update=SetFolderTreeDefault)
    bpy.types.Scene.FolderTree = bpy.props.StringProperty(
        name="folder tree", default="\\[mat]\\[bakeType]", description="Specify the node tree and use the following notation for dynamic value\n[Object]=Object name\n[bakeType]=name of bake type\n[mat]=material name \n \\=new folder")
    bpy.types.Scene.BakeRegardless = bpy.props.BoolProperty(
        name="Bake Regardless", default=False, description="Turn this on to bake texture even if it's not necessary")
    bpy.types.Scene.BakeMulitpleSlots = bpy.props.BoolProperty(
        name="Bake Mulitple Slots", default=False, description="Turn this on to bake multiple slots")
    bpy.types.Scene.CheckUVOverLap = bpy.props.BoolProperty(
        name="Check UV Over Lap", default=False, description="Turn this on to check if the uv is overlapping")
    bpy.types.Scene.CheckUVOverBound = bpy.props.BoolProperty(
        name="Check UV Over Bound", default=False, description="Turn this on to check if the uv is over bound(uv is not within 0-1 space)")
    bpy.types.Scene.GenerateUvRegardLess = bpy.props.BoolProperty(
        name="Generate Uv Regardless", default=False, description="Turn this on to generate uv even if it's not necessary")
    bpy.types.Scene.BakeMultiple = bpy.props.BoolProperty(
        name="Bake Multiple object", default=False, description="Turn this on to bake multiple object")
    bpy.types.Scene.UseUdims = bpy.props.BoolProperty(
        name="Use Udims", default=False, description="Turn this on to use udims automatically")
    bpy.types.Scene.FileFormat = bpy.props.EnumProperty(name="File format", description="What file formate to use", items={
        ("png", "png", "Save images as png"), ("tga", "tga", "Save images as tga"), ("exr", "exr", "Save images as exr"), ("jpg", "jpg", "Save images as jpg")})
    bpy.types.Scene.BakedImagesFilePath = "All Baked Images"
    bpy.types.Scene.PreBakedFilePath = "All Pre Baked Images"
    bpy.types.Scene.Device = bpy.props.EnumProperty(name="Device", description="Device to use for baking", items={
        ("GPU", "GPU", "Use gpu for baking"), ("CPU", "CPU", "Use cpu for baking")})
    bpy.types.Scene.CopyNodeGroup = bpy.props.BoolProperty(
        name="Copy Node Group", default=False, description="Turn this on to copy node group")
    bpy.types.Scene.ApplyMaterial = bpy.props.BoolProperty(
        name="Apply Material", default=False, description="Turn this on to apply the material")
    bpy.types.Scene.ApplyToCopiedAndHideOriginal = bpy.props.BoolProperty(
        name="Apply to copied object and hide original", default=False, description="Turn this on to copy the object, apply the copied material, and hide the original")
    bpy.types.Scene.CopyMaterial = bpy.props.BoolProperty(
        name="Copy material", default=True, description="turn this on to copy material before baking", update=SetCopiedMaterialDefault)

    bpy.types.Scene.AntialiasingScale = bpy.props.FloatProperty(
        name="Anti aliasing", description="Less then 1 does downscaling, greater then 1 does upscaling,and at 1 does nothing", default=1, min=0, max=2)
    bpy.types.Scene.UVIslandMargin = bpy.props.FloatProperty(
        name="UV Island Margin", description="Margin for uv island if generating", min=0)


def UnregisterSettingTab():
    class_unregister()
    del bpy.types.Scene.packObject

    settingPropertyUnregister()


def settingPropertyUnregister():
    del bpy.types.Scene.UVIslandMargin
    del bpy.types.Scene.extrusion
    del bpy.types.Scene.rayDistance
    del bpy.types.Scene.settingName
    del bpy.types.Scene.SavedSettings
    del bpy.types.Scene.UseCustomFolderTree
    del bpy.types.Scene.FolderTree
    del bpy.types.Scene.height
    del bpy.types.Scene.width
    del bpy.types.Scene.ShadeSmooth
    del bpy.types.Scene.BakeRegardless
    del bpy.types.Scene.BakeMulitpleSlots
    del bpy.types.Scene.CheckUVOverLap
    del bpy.types.Scene.CheckUVOverBound
    del bpy.types.Scene.GenerateUvRegardLess
    del bpy.types.Scene.Device
    del bpy.types.Scene.BakeMultiple
    del bpy.types.Scene.UseUdims
    del bpy.types.Scene.FileFormat
    del bpy.types.Scene.BakedImagesFilePath
    del bpy.types.Scene.PreBakedFilePath
    del bpy.types.Scene.CopyNodeGroup
    del bpy.types.Scene.ApplyMaterial
    del bpy.types.Scene.ApplyToCopiedAndHideOriginal
    del bpy.types.Scene.CopyMaterial
    del bpy.types.Scene.AntialiasingScale
