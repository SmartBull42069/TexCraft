
from .Data import RegisterData,UnregisterData
from .BakingObjectTab import RegisterObjectTab,UnregisterObjectTab
from .SelectedBake import RegisterBakeTab,UnregisterBakeTab
from .Packing import RegisterPackingTab,UnregisterPackingTab
from .SettingTab import RegisterSettingTab,UnregisterSettingTab
from .Core import registerStartTab,UnregisterStartTab
import os
import bpy
def register():
    RegisterData()
    RegisterObjectTab()
    RegisterBakeTab()
    RegisterPackingTab()
    RegisterSettingTab()
    registerStartTab()
def unregister():
    try:
        os.rmdir(bpy.context.scene.SavedSettingFolder)
        os.rmdir(bpy.context.scene.SelectedBakeSavedFolder)
        os.rmdir(bpy.context.scene.PackedSavedFolder)
    except:
        pass
    UnregisterData()
    UnregisterObjectTab()
    UnregisterBakeTab()
    UnregisterPackingTab()
    UnregisterSettingTab()
    UnregisterStartTab()
