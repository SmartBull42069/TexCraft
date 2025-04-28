import bpy


def Register():
    bpy.types.Scene.Prefixes = {}
    bpy.types.Scene.Suffixes = {}
    bpy.types.Scene.inputNode = {"Subsurface IOR": "BSDF_PRINCIPLED", "Emission": "BSDF_PRINCIPLED", "Multires Displacement": "OUTPUT_MATERIAL", "Multires Normal": "BSDF_PRINCIPLED", "Cavity": "BSDF_PRINCIPLED", "Thickness": "BSDF_PRINCIPLED", "Combine": "OUTPUT_MATERIAL", "Thin Film IOR": "BSDF_PRINCIPLED", "Thin Film Thickness": "BSDF_PRINCIPLED", "Sheen Tint": "BSDF_PRINCIPLED", "Sheen Roughness": "BSDF_PRINCIPLED", "Sheen Weight": "BSDF_PRINCIPLED", "Coat Tint": "BSDF_PRINCIPLED", "Coat IOR": "BSDF_PRINCIPLED", "Coat Roughness": "BSDF_PRINCIPLED", "Coat Weight": "BSDF_PRINCIPLED", "Transmission Weight": "BSDF_PRINCIPLED", "Anisotropic Rotation": "BSDF_PRINCIPLED", "Anisotropic": "BSDF_PRINCIPLED", "Specular Tint": "BSDF_PRINCIPLED", "Specular IOR Level": "BSDF_PRINCIPLED", "Subsurface Anisotropy": "BSDF_PRINCIPLED", "Subsurface Scale": "BSDF_PRINCIPLED", "Subsurface Weight": "BSDF_PRINCIPLED", "Displacement Midlevel": "DISPLACEMENT", "Normal": "BSDF_PRINCIPLED", "Alpha": "BSDF_PRINCIPLED", "Base Color": "BSDF_PRINCIPLED",
                                 "Metallic": "BSDF_PRINCIPLED", "Emission Color": "BSDF_PRINCIPLED", "Roughness": "BSDF_PRINCIPLED", "Ambient Occlusion": "BSDF_PRINCIPLED", "Emission Strength": "BSDF_PRINCIPLED", "Displacement Height": "DISPLACEMENT", "Displacement Scale": "DISPLACEMENT",
                                 "Bump Strength": "BUMP",
                                 "Bump Height": "BUMP", "Bump Distance": "BUMP", "IOR": "BSDF_PRINCIPLED"}
    bpy.types.Scene.inputNodeNames = {"Subsurface IOR": "Subsurface IOR", "Emission": "Emission Color", "Multires Displacement": "Displacement", "Multires Normal": "Normal", "Cavity": "Base Color", "Thickness": "Base Color", "Combine": "Surface", "Thin Film IOR": "Thin Film IOR", "Thin Film Thickness": "Thin Film Thickness", "Sheen Tint": "Sheen Tint", "Sheen Roughness": "Sheen Roughness", "Sheen Weight": "Sheen Weight", "Coat Tint": "Coat Tint", "Coat IOR": "Coat IOR", "Coat Roughness": "Coat Roughness", "Coat Weight": "Coat Weight", "Transmission Weight": "Transmission Weight", "Anisotropic Rotation": "Anisotropic Rotation", "Anisotropic": "Anisotropic", "Specular Tint": "Specular Tint", "Specular IOR Level": "Specular IOR Level", "Subsurface Anisotropy": "Subsurface Anisotropy", "Subsurface Scale": "Subsurface Scale", "Subsurface Weight": "Subsurface Weight", "IOR": "IOR", "Bump Strength": "Strength",
                                      "Bump Height": "Height", "Bump Distance": "Distance", "Displacement Midlevel": "Midlevel", "Normal": "Normal", "Alpha": "Alpha", "Base Color": "Base Color",
                                      "Metallic": "Metallic", "Emission Color": "Emission Color", "Roughness": "Roughness", "Ambient Occlusion": "Base Color", "Emission Strength": "Emission Strength", "Displacement Height": "Height", "Displacement Scale": "Scale"}

    bpy.types.Scene.BakeTypes = {'Base Color': 'BaseColor', 'Metallic': 'Metallic', 'Roughness': 'Roughness', 'Normal': 'Normal', 'Emission': 'Emission', 'Emission Color': 'EmissionColor', 'Emission Strength': 'EmissionStrength', 'Alpha': 'Alpha',  'Ambient Occlusion': 'AmbientOcclusion', 'Bump Strength': 'BumpStrength', 'Bump Height': 'BumpHeight', 'Bump Distance': 'BumpDistance', 'Subsurface IOR': 'SubsurfaceIOR', 'Multires Displacement': 'MultiresDisplacement', 'Multires Normal': 'MultiresNormal', 'Cavity': 'Cavity', 'Thickness': 'Thickness', 'Combine': 'Combine', 'Thin Film IOR': 'ThinFilmIOR', 'Thin Film Thickness': 'ThinFilmThickness', 'Sheen Tint': 'SheenTint', 'Sheen Roughness': 'SheenRoughness', 'Sheen Weight': 'SheenWeight', 'Coat Tint': 'CoatTint', 'Coat IOR': 'CoatIOR', 'Coat Roughness': 'CoatRoughness', 'Coat Weight': 'CoatWeight', 'Transmission Weight': 'TransmissionWeight', 'Anisotropic Rotation': 'AnisotropicRotation', 'Anisotropic': 'Anisotropic', 'Specular Tint': 'SpecularTint',
                                 'Specular IOR Level': 'SpecularIORLevel', 'Subsurface Anisotropy': 'SubsurfaceAnisotropy', 'Subsurface Scale': 'SubsurfaceScale', 'Subsurface Weight': 'SubsurfaceWeight',  'Displacement Midlevel': 'DisplacementMidlevel',   'Displacement Height': 'DisplacementHeight', 'Displacement Scale': 'DisplacementScale', 'IOR': 'IOR'}
    bpy.types.Scene.packObject = []
    bpy.types.Scene.ColorMaps = [
        "Base Color", "Ambient Occlusion", "Emission", 'Specular Tint', 'Emission Color', 'Coat Tint', 'Sheen Tint']
    bpy.types.Scene.settingsNames = {"UVIslandMargin": "UV Island Margin", "margin": "Texture margin", "rayDistance": "Ray distance", "extrusion": "Extrusion", "height": "height", "width": "width", 'AntialiasingScale': 'Anti aliasing Scale',  "UseCustomFolderTree": "Use Custom Folder Tree", 'ShadeSmooth': 'Shade Smooth', 'ConvertRoughnessToSmoothness': 'Convert Roughness To Smoothness', 'FlipnormalY': 'Flip normal Y', 'BakeRegardless': 'Bake Regardless', 'BakeMulitpleSlots': 'Bake Mulitple Slots', 'CheckUVOverLap': 'Check UV OverLap', 'CheckUVOverBound': 'Check UV Over Bound', 'GenerateUvRegardLess': 'Generate Uv RegardLess',
                                     'BakeMultiple': 'Bake Multiple', 'UseUdims': 'Use Udims', 'CopyNodeGroup': 'Copy Node Group', 'ApplyMaterial': 'Apply Material', 'ApplyToCopiedAndHideOriginal': 'Apply To Copied And Hide Original', 'CopyMaterial': 'Copy Material', 'SpecifiedUv': 'Specified Uv', 'Device': 'Device', 'FileFormat': 'File format'}
    bpy.types.Scene.flippingInfo = {"Roughness": {0: True, 1: True, 2: True, 3: True}, "Normal": {
        0: False, 1: True, 2: False, 3: False}}
    bpy.types.Scene.propertyDependentInput = {"Subsurface IOR": {"PropertyAccept": ["RANDOM_WALKRANDOM_WALK_SKIN"], "Property": "subsurface_method", "NodeType": "BSDF_PRINCIPLED"}, "Subsurface Anisotropy": {
        "PropertyAccept": ["RANDOM_WALKRANDOM_WALK_SKIN", "RANDOM_WALK"], "Property": "subsurface_method", "NodeType": "BSDF_PRINCIPLED"}}
    bpy.types.Scene.baseNode = {
        "BUMP": {"Output": "Normal", "Give": "BSDF_PRINCIPLED"}}
    bpy.types.Scene.OneInvert=[".exr"]
    bpy.types.Scene.notRequireBakingWhenBakingAll = ["Emission"]
    bpy.types.Scene.flippingColorInfo = {"Roughness": "L", "Normal": "RGBA"}
    bpy.types.Scene.RequireAfterProcess = {
        "Emission": {"Emission Strength": 1}}
    bpy.types.Scene.BakingSelection = {"Subsurface IOR": "EMIT", "Emission": "EMIT", "Multires Displacement": "DISPLACEMENT", "Multires Normal": "NORMALS", "Cavity": "EMIT", "Thickness": "EMIT", "Combine": "COMBINED", "Thin Film IOR": "EMIT", "Thin Film Thickness": "EMIT", "Sheen Tint": "EMIT", "Sheen Roughness": "EMIT", "Sheen Weight": "EMIT", "Coat Tint": "EMIT", "Coat IOR": "EMIT", "Coat Roughness": "EMIT", "Coat Weight": "EMIT", "Transmission Weight": "EMIT", "Anisotropic Rotation": "EMIT", "Anisotropic": "EMIT", "Specular Tint": "EMIT", "Specular IOR Level": "EMIT", "Subsurface Anisotropy": "EMIT", "Subsurface Scale": "EMIT", "Subsurface Weight": "EMIT", "Bump Strength": "EMIT", "Bump Height": "EMIT", "Bump Distance": "EMIT", "Displacement Midlevel": "EMIT", "Normal": "NORMAL", "Alpha": "EMIT", "Base Color": "DIFFUSE",
                                       "Metallic": "EMIT", "Emission Color": "EMIT", "Roughness": "ROUGHNESS", "Ambient Occlusion": "AO", "Emission Strength": "EMIT", "Displacement Height": "EMIT", "Displacement Scale": "EMIT", "IOR": "EMIT"}
    bpy.types.Scene.alwaysRequireMultires = [
        "Multires Displacement", "Multires Normal"]
    bpy.types.Scene.miscBake = ["Ambient Occlusion",
                                "Combine", "Thickness", "Cavity", "Multires Normal", "Multires Displacement"]
    bpy.types.Scene.allwaysRequireBaking = ["Ambient Occlusion",
                                            "Combine", "Thickness", "Cavity", "Multires Normal", "Multires Displacement", "Emission"]
    bpy.types.Scene.multiResSetup = {"Multires Displacement": {
        "Node": "ShaderNodeDisplacement", "InputOutputName": "Height", "Output": "Displacement", "OriginInput": "Displacement"}, "Multires Normal": {
        "Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, "Normal": {
        "Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}}
    
    bpy.types.Scene.alwaysExcludedChannels = ["Alpha", "Thin Film IOR", "Thin Film Thickness", "Sheen Tint", "Sheen Roughness", "Sheen Weight", "Coat Tint", "Coat IOR", "Coat Roughness", "Coat Weight", "Transmission Weight", "Anisotropic Rotation", "Anisotropic", "Specular Tint", "Specular IOR Level", "Subsurface Anisotropy", "Subsurface Scale", "Subsurface Weight", "Metallic", "Displacement Scale", "Displacement Midlevel", "Displacement Height", "Bump Strength",
                                              "Bump Height", "Bump Distance", "IOR"]
    bpy.types.Scene.requiresMaterialOutPutConnection = [
        "Displacement Scale", "Displacement Midlevel", "Displacement Height", "Thickness", "Cavity"]
    bpy.types.Scene.requiresConnection = {"Subsurface IOR": "Strength", "Alpha": "Strength", "Thin Film IOR": "Strength", "Thin Film Thickness": "Strength", "Sheen Tint": "Color", "Sheen Roughness": "Strength", "Sheen Weight": "Strength", "Coat Tint": "Color", "Coat IOR": "Strength", "Coat Roughness": "Strength", "Coat Weight": "Strength", "Transmission Weight": "Strength", "Anisotropic Rotation": "Strength", "Anisotropic": "Strength", "Specular Tint": "Color", "Specular IOR Level": "Strength", "Subsurface Anisotropy": "Strength", "Subsurface Scale": "Strength", "Subsurface Weight": "Strength", "Bump Strength": "Strength",
                                          "Bump Height": "Strength", "Bump Distance": "Strength", "Metallic": "Strength", "IOR": "Strength"}
    bpy.types.Scene.requiresDefaultValue = {
        "Emission Color": {"Strength": 1}, "Specular Tint": {"Strength": 1},
        "Coat Tint": {"Strength": 1}, "Sheen Tint": {"Strength": 1}}
    bpy.types.Scene.propertyWithSpecialDefault = {
        "DISPLACEMENT": [{"Scale": 0}]}
    bpy.types.Scene.GreyScale = ["Metallic", "Roughness", "Ambient Occlusion", "Emission Strength", "Bump Strength", "Bump Height", "Bump Distance", "Displacement Midlevel",  "Displacement Height", "Displacement Scale", "Alpha", "Subsurface IOR", "Cavity", "Thickness", "Thin Film IOR", "Thin Film Thickness", "Sheen Roughness", "Sheen Weight", "Coat IOR", "Coat Roughness", "Coat Weight", "Transmission Weight", "Anisotropic Rotation", "Anisotropic", "Specular IOR Level", "Subsurface Anisotropy", "Subsurface Scale", "Subsurface Weight",
                                 "IOR", "Multires Displacement"]
    bpy.types.Scene.Blending = {"Ambient_occlusion_Base Color": {
        "Properties": {"blend_type": "MULTIPLY", "data_type": "RGBA"}, "Inputs": {"Factor": 1}, "Node": "ShaderNodeMix", "OutPutSocket": "Result", "Connection": {"A": "Base Color", "B": "Ambient Occlusion"}, "UsuallyAvailable": ["Base Color"], "requirements": True}, "Thickness_Base_Color": {
        "Properties": {"blend_type": "MULTIPLY", "data_type": "RGBA"}, "Inputs": {"Factor": 1}, "Node": "ShaderNodeMix", "OutPutSocket": "Result", "Connection": {"A": "Base Color", "B": "Thickness"}, "UsuallyAvailable": ["Base Color"], "requirements": True}, "Cavity_Base_Color": {
        "Properties": {"blend_type": "MULTIPLY", "data_type": "RGBA"}, "Inputs": {"Factor": 1}, "Node": "ShaderNodeMix", "OutPutSocket": "Result", "Connection": {"A": "Base Color", "B": "Cavity"}, "UsuallyAvailable": ["Base Color"], "requirements": True}}
    bpy.types.Scene.multipleNode = {"BSDF_PRINCIPLED": [True], "BUMP": [True], "DISPLACEMENT": [
        False, "Multiple displacement node detected"], "OUTPUT_MATERIAL": [False, "Multiple material output node detected"]}
    bpy.types.Scene.requireAdditionalNode = {"Thickness": {
        "Properties": {"inside": True}, "Inputs": {"Distance": 0.9}, "Node": "ShaderNodeAmbientOcclusion", "OutPutSocket": "AO"}, "Cavity": {
        "Properties": {}, "Inputs": {}, "Node": "ShaderNodeNewGeometry", "OutPutSocket": "Pointiness"}}
    bpy.types.Scene.bakeTypeColorRamp = {"Cavity": {"Positions": [0.4, 0.6]}}
    bpy.types.Scene.propertyWithDependants = {
        "BSDF_PRINCIPLED": {
            "Emission Color": [
                {"Emission Strength": 0},
                {"Emission Color": (0, 0, 0, 1)}
            ],
            "Emission Strength": [
                {"Emission Color": (0, 0, 0, 1)},
                {"Emission Strength": 0}
            ]
        },
        "NORMAL_MAP": {
            "Color": [
                {"Strength": 0},
                {"Color": (0.5, 0.5, 1, 1)}
            ],
            "Strength": [
                {"Color": (0.5, 0.5, 1, 1)},
                {"Strength": 0}
            ]
        },
        "BUMP": {
            "Height": [
                {"Strength": 0},
                {"Distance": 0}
            ]
        },
        "DISPLACEMENT": {
            "Height": [
                {"Scale": 0}
            ],
            "Midlevel": [
                {"Scale": 0}
            ]
        }
    }
    bpy.types.Scene.basePath = bpy.props.StringProperty(
        name="Base path", default=bpy.path.abspath('//'), description="Base path for saving textures")
    bpy.types.Scene.JsonExport = f"{bpy.context.scene.basePath}MappingFile/"
    bpy.types.Scene.giveInputSocket = {"NORMAL_MAP": "Color"}
    bpy.types.Scene.SavedSettingFolder = "./Setting"
    bpy.types.Scene.PrefixSavedFolder = "./Prefix"
    bpy.types.Scene.SuffixSavedFolder = "./Suffix"
    bpy.types.Scene.SelectedBakeSavedFolder = "./Bake"
    bpy.types.Scene.PackedSavedFolder = "./Packed"
    bpy.types.Scene.ShaderNodes=['ShaderNodeEmission', 'ShaderNodeBsdfDiffuse', 'ShaderNodeBsdfGlass', 'ShaderNodeBsdfAnisotropic', 'ShaderNodeBsdfHair', 'ShaderNodeMixShader', 'ShaderNodeBsdfPrincipled', 'ShaderNodeBsdfHairPrincipled', 'ShaderNodeVolumePrincipled',
        'ShaderNodeBsdfRayPortal', 'ShaderNodeBsdfRefraction', 'ShaderNodeBsdfSheen', 'ShaderNodeSubsurfaceScattering', 'ShaderNodeBsdfToon', 'ShaderNodeBsdfTranslucent', 'ShaderNodeBsdfTransparent', 'ShaderNodeVolumeAbsorption', 'ShaderNodeVolumeScatter']


def Unregister():
    del bpy.types.Scene.ShaderNodes
    del bpy.types.Scene.OneInvert
    del bpy.types.Scene.basePath
    del bpy.types.Scene.JsonExport
    del bpy.types.Scene.PackedSavedFolder
    del bpy.types.Scene.SelectedBakeSavedFolder
    del bpy.types.Scene.SavedSettingFolder
    del bpy.types.Scene.BakeNames
    del bpy.types.Scene.settingsNames
    del bpy.types.Scene.selectedBakePrefix
    del bpy.types.Scene.selectedBakeSuffix
    del bpy.types.Scene.flippingInfo
    del bpy.types.Scene.propertyDependentInput
    del bpy.types.Scene.baseNode
    del bpy.types.Scene.notRequireBakingWhenBakingAll
    del bpy.types.Scene.flippingColorInfo
    del bpy.types.Scene.RequireAfterProcess
    del bpy.types.Scene.BakingSelection
    del bpy.types.Scene.alwaysRequireMultires
    del bpy.types.Scene.miscBake
    del bpy.types.Scene.allwaysRequireBaking
    del bpy.types.Scene.multiResSetup
    del bpy.types.Scene.ColorMaps
    del bpy.types.Scene.alwaysExcludedChannels
    del bpy.types.Scene.requiresMaterialOutPutConnection
    del bpy.types.Scene.requiresConnection
    del bpy.types.Scene.requiresDefaultValue
    del bpy.types.Scene.inputNode
    del bpy.types.Scene.inputNodeNames
    del bpy.types.Scene.propertyWithSpecialDefault
    del bpy.types.Scene.GreyScale
    del bpy.types.Scene.Blending
    del bpy.types.Scene.multipleNode
    del bpy.types.Scene.requireAdditionalNode
    del bpy.types.Scene.bakeTypeColorRamp
    del bpy.types.Scene.propertyWithDependants
    del bpy.types.Scene.giveInputSocket


Register()
