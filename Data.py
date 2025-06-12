import bpy


def Register():
    bpy.types.Scene.Prefixes = {}
    bpy.types.Scene.Suffixes = {}
    bpy.types.Scene.requiredChannels={"Emission": ["Emission Color", "Emission Strength"],"Emission N":["Emission Strength N","Emission Color N"]}
    bpy.types.Scene.inputNodeNamesUi={"Coat Normal": "Principled Bsdf Shader","Diffuse Roughness": "Principled Bsdf Shader","Volume Scatter Diameter":"Volume Scatter Shader","Volume Scatter Alpha":"Volume Scatter Shader","Volume Scatter Backscatter":"Volume Scatter Shader","Volume Scatter IOR":"Volume Scatter Shader","Volume Scatter Anisotropy":"Volume Scatter Shader","Volume Scatter Density":"Volume Scatter Shader","Volume Scatter Color":"Volume Scatter Shader","Translucent Normal":"Translucent Shader","Translucent Color":"Translucent Shader","Transparent Color":"Transparent Shader","Volume Absorption Density":"Volume Absorption Shader","Volume Absorption Color N":"Volume Absorption Shader","Toon Normal":"Toon Shader","Toon Smooth":"Toon Shader","Toon Size":"Toon Shader","Toon Color":"Toon Shader","Sheen Normal":"Sheen Shader","Sheen Roughness N":"Sheen Shader","Sheen Color":"Sheen Shader","Ray Portal Direction":"Ray Portal Shader","Ray Portal Position":"Ray Portal Shader","Ray Portal Color":"Ray Portal Shader","Subsurface Scattering IOR":"Subsurface Scattering Shader","Subsurface Scattering Anisotropy":"Subsurface Scattering Shader","Subsurface Scattering Roughness":"Subsurface Scattering Shader","Subsurface Scattering Normal":"Subsurface Scattering Shader","Subsurface Scattering Radius":"Subsurface Scattering Shader","Subsurface Scattering Scale":"Subsurface Scattering Shader","Subsurface Scattering Color":"Subsurface Scattering Shader","Specular Clear Coat Normals":"Specular Shader","Specular Clear Coat Roughness":"Specular Shader","Specular Clear Coat":"Specular Shader","Specular Normal":"Specular Shader","Specular Transparency":"Specular Shader","Specular Emissive Color":"Specular Shader","Specular Roughness":"Specular Shader","Specular Specular":"Specular Shader","Specular Base Color":"Specular Shader","Refraction Normal":"Refraction Shader","Refraction IOR":"Refraction Shader","Refraction Roughness":"Refraction Shader","Refraction Color":"Refraction Shader","Volume Temperature":"Principled Volume Shader Shader","Volume Blackbody Tint":"Principled Volume Shader Shader","Volume Blackbody Intensity":"Principled Volume Shader Shader","Volume Emission Color":"Principled Volume Shader Shader","Volume Emission Strength":"Principled Volume Shader Shader","Volume Absorption Color":"Principled Volume Shader Shader","Volume Anisotropy":"Principled Volume Shader Shader","Volume Density":"Principled Volume Shader Shader","Volume Color":"Principled Volume Shader Shader","Hair Absorption Coefficient":"Principled Hair Bsdf Shader","Hair Coat":"Principled Hair Bsdf Shader","Hair Random Color":"Principled Hair Bsdf Shader","Hair Tint":"Principled Hair Bsdf Shader","Hair Melanin Redness":"Principled Hair Bsdf Shader","Hair Melanin":"Principled Hair Bsdf Shader","Hair Color":"Principled Hair Bsdf Shader","Hair Radial Roughness":"Principled Hair Bsdf Shader","Hair Aspect Ratio":"Principled Hair Bsdf Shader","Hair Secondary Reflection":"Principled Hair Bsdf Shader","Hair Random Roughness":"Principled Hair Bsdf Shader","Hair Transmission":"Principled Hair Bsdf Shader","Hair Reflection":"Principled Hair Bsdf Shader","Hair Random":"Principled Hair Bsdf Shader","Hair Offset":"Principled Hair Bsdf Shader","Hair Roughness":"Principled Hair Bsdf Shader","Hair IOR":"Principled Hair Bsdf Shader","Hair Tangent N":"Hair Shader","Hair RoughnessV N":"Hair Shader","Hair RoughnessU N":"Hair Shader","Hair Offset N":"Hair Shader","Hair Color N":"Hair Shader","Glossy Tangent":"Glossy Shader","Glossy Normal":"Glossy Shader","Glossy Rotation":"Glossy Shader","Glossy Anisotropy":"Glossy Shader","Glossy Roughness":"Glossy Shader","Glossy Color":"Glossy Shader","Glass Normal":"Glass Shader","Glass IOR":"Glass Shader","Glass Roughness":"Glass Shader","Glass Color":"Glass Shader","Emission N":"Emission Shader","Emission Strength N":"Emission Shader","Emission Color N":"Emission Shader","Metallic Extinction":"Metallic Shader","Metallic IOR":"Metallic Shader","Metallic Edge Tint":"Metallic Shader","Metallic Color":"Metallic Shader","Metallic Tangent":"Metallic Shader","Metallic Normal":"Metallic Shader","Metallic Rotation":"Metallic Shader","Metallic Anisotropy":"Metallic Shader","Metallic Roughness":"Metallic Shader","Diffuse Normal":"Diffuse Shader","Diffuse Roughness N":"Diffuse Shader","Diffuse Color":"Diffuse Shader","Tangent":"Principled Bsdf Shader","Subsurface Radius":"Principled Bsdf Shader","Subsurface IOR": "Principled Bsdf Shader", "Emission": "Principled Bsdf Shader", "Multires Displacement": "Multires Modifier", "Multires Normal": "Multires Modifier", "Cavity": "Misc Texture", "Thickness": "Misc Texture", "Combine": "Misc Texture", "Thin Film IOR": "Principled Bsdf Shader", "Thin Film Thickness": "Principled Bsdf Shader", "Sheen Tint": "Principled Bsdf Shader", "Sheen Roughness": "Principled Bsdf Shader", "Sheen Weight": "Principled Bsdf Shader", "Coat Tint": "Principled Bsdf Shader", "Coat IOR": "Principled Bsdf Shader", "Coat Roughness": "Principled Bsdf Shader", "Coat Weight": "Principled Bsdf Shader", "Transmission Weight": "Principled Bsdf Shader", "Anisotropic Rotation": "Principled Bsdf Shader", "Anisotropic": "Principled Bsdf Shader", "Specular Tint": "Principled Bsdf Shader", "Specular IOR Level": "Principled Bsdf Shader", "Subsurface Anisotropy": "Principled Bsdf Shader", "Subsurface Scale": "Principled Bsdf Shader", "Subsurface Weight": "Principled Bsdf Shader", "Displacement Midlevel": "Displacement Shader", "Normal": "Principled Bsdf Shader", "Alpha": "Principled Bsdf Shader", "Base Color": "Principled Bsdf Shader",
                                 "Metallic": "Principled Bsdf Shader", "Emission Color": "Principled Bsdf Shader", "Roughness": "Principled Bsdf Shader", "Ambient Occlusion": "Misc Texture", "Emission Strength": "Principled Bsdf Shader", "Displacement Height": "Displacement Shader", "Displacement Scale": "Displacement Shader",
                                 "Bump Strength": "Bump Shader","Filter Width":"Bump Shader",
                                 "Bump Height": "Bump Shader", "Bump Distance": "Bump Shader", "IOR": "Principled Bsdf Shader"}
    bpy.types.Scene.excludedChannels={"Filter Width":[],"Coat Normal":[],"Diffuse Roughness":[],"Volume Scatter Diameter":[],"Volume Scatter Alpha":[],"Volume Scatter Backscatter":[],"Volume Scatter IOR":[],"Volume Scatter Anisotropy":[],"Volume Scatter Density":[],"Volume Scatter Color":[],"Translucent Normal":[],"Translucent Color":[],"Transparent Color":[],"Volume Absorption Density":[],"Volume Absorption Color N":[],"Toon Normal":[],"Toon Smooth":[],"Toon Size":[],"Toon Color":[],"Sheen Normal":[],"Sheen Roughness N":[],"Sheen Color":[],"Ray Portal Direction":[],"Ray Portal Position":[],"Ray Portal Color":[],"Subsurface Scattering IOR":[],"Subsurface Scattering Anisotropy":[],"Subsurface Scattering Roughness":[],"Subsurface Scattering Normal":[],"Subsurface Scattering Radius":[],"Subsurface Scattering Scale":[],"Subsurface Scattering Color":[],"Specular Clear Coat Normals":[],"Specular Clear Coat Roughness":[],"Specular Clear Coat":[],"Specular Normal":[],"Specular Transparency":[],"Specular Emissive Color":[],"Specular Roughness":[],"Specular Specular":[],"Specular Base Color":[],"Refraction Normal":[],"Refraction IOR":[],"Refraction Roughness":[],"Refraction Color":[],"Volume Temperature":[],"Volume Blackbody Tint":[],"Volume Blackbody Intensity":[],"Volume Emission Color":[],"Volume Emission Strength":[],"Volume Absorption Color":[],"Volume Anisotropy":[],"Volume Density":[],"Volume Color":[],"Hair Absorption Coefficient":[],"Hair Coat":[],"Hair Random Color":[],"Hair Tint":[],"Hair Melanin Redness":[],"Hair Melanin":[],"Hair Color":[],"Hair Radial Roughness":[],"Hair Aspect Ratio":[],"Hair Secondary Reflection":[],"Hair Random Roughness":[],"Hair Transmission":[],"Hair Reflection":[],"Hair Random":[],"Hair Offset":[],"Hair Roughness":[],"Hair IOR":[],"Hair Tangent N":[],"Hair RoughnessV N":[],"Hair RoughnessU N":[],"Hair Offset N":[],"Hair Color N":[],"Glossy Tangent":[],"Glossy Normal":[],"Glossy Rotation":[],"Glossy Anisotropy":[],"Glossy Roughness":[],"Glossy Color":[],"Glass Normal":[],"Glass IOR":[],"Glass Roughness":[],"Glass Color":[],"Emission Strength N":[],"Emission Color N":[],"Metallic Extinction":[],"Metallic IOR":[],"Metallic Edge Tint":[],"Metallic Color":[],"Metallic Tangent":[],"Metallic Normal":[],"Metallic Rotation":[],"Metallic Anisotropy":[],"Metallic Roughness":[],"Diffuse Normal":[],"Diffuse Roughness N":[],"Diffuse Color":[],"Tangent":[],"Subsurface Radius":[],"Subsurface IOR": [], "Thin Film IOR": [], "Thin Film Thickness": [], "Sheen Tint": [], "Sheen Roughness": [], "Sheen Weight": [], "Coat Tint": [], "Coat IOR": [], "Coat Roughness": [], "Coat Weight": [], "Transmission Weight": [], "Anisotropic Rotation": [], "Anisotropic": [], "Specular Tint": [], "Specular IOR Level": [], "Subsurface Anisotropy": [], "Subsurface Scale": [], "Subsurface Weight": [], "Alpha": [], "Base Color": [],
                        "Metallic": [], "Emission Color": [], "Roughness": [], "Emission Strength": [], "Displacement Height": [], "Displacement Scale": [], "Displacement Midlevel": [], "Material Output": [], "IOR": [], "Normal": []}
    bpy.types.Scene.inputNode = { "Coat Normal": "BSDF_PRINCIPLED","Diffuse Roughness": "BSDF_PRINCIPLED","Volume Scatter Diameter":"VOLUME_SCATTER","Volume Scatter Alpha":"VOLUME_SCATTER","Volume Scatter Backscatter":"VOLUME_SCATTER","Volume Scatter IOR":"VOLUME_SCATTER","Volume Scatter Anisotropy":"VOLUME_SCATTER","Volume Scatter Density":"VOLUME_SCATTER","Volume Scatter Color":"VOLUME_SCATTER","Translucent Normal":"BSDF_TRANSLUCENT","Translucent Color":"BSDF_TRANSLUCENT","Transparent Color":"BSDF_TRANSPARENT","Volume Absorption Density":"VOLUME_ABSORPTION","Volume Absorption Color N":"VOLUME_ABSORPTION","Toon Normal":"BSDF_TOON","Toon Smooth":"BSDF_TOON","Toon Size":"BSDF_TOON","Toon Color":"BSDF_TOON","Sheen Normal":"BSDF_SHEEN","Sheen Roughness N":"BSDF_SHEEN","Sheen Color":"BSDF_SHEEN","Ray Portal Direction":"BSDF_RAY_PORTAL","Ray Portal Position":"BSDF_RAY_PORTAL","Ray Portal Color":"BSDF_RAY_PORTAL","Subsurface Scattering IOR":"SUBSURFACE_SCATTERING","Subsurface Scattering Anisotropy":"SUBSURFACE_SCATTERING","Subsurface Scattering Roughness":"SUBSURFACE_SCATTERING","Subsurface Scattering Normal":"SUBSURFACE_SCATTERING","Subsurface Scattering Radius":"SUBSURFACE_SCATTERING","Subsurface Scattering Scale":"SUBSURFACE_SCATTERING","Subsurface Scattering Color":"SUBSURFACE_SCATTERING","Specular Clear Coat Normals":"EEVEE_SPECULAR","Specular Clear Coat Roughness":"EEVEE_SPECULAR","Specular Clear Coat":"EEVEE_SPECULAR","Specular Normal":"EEVEE_SPECULAR","Specular Transparency":"EEVEE_SPECULAR","Specular Emissive Color":"EEVEE_SPECULAR","Specular Roughness":"EEVEE_SPECULAR","Specular Specular":"EEVEE_SPECULAR","Specular Base Color":"EEVEE_SPECULAR","Refraction Normal":"BSDF_REFRACTION","Refraction IOR":"BSDF_REFRACTION","Refraction Roughness":"BSDF_REFRACTION","Refraction Color":"BSDF_REFRACTION","Volume Temperature":"PRINCIPLED_VOLUME","Volume Blackbody Tint":"PRINCIPLED_VOLUME","Volume Blackbody Intensity":"PRINCIPLED_VOLUME","Volume Emission Color":"PRINCIPLED_VOLUME","Volume Emission Strength":"PRINCIPLED_VOLUME","Volume Absorption Color":"PRINCIPLED_VOLUME","Volume Anisotropy":"PRINCIPLED_VOLUME","Volume Density":"PRINCIPLED_VOLUME","Volume Color":"PRINCIPLED_VOLUME","Hair Absorption Coefficient":"BSDF_HAIR_PRINCIPLED","Hair Coat":"BSDF_HAIR_PRINCIPLED","Hair Random Color":"BSDF_HAIR_PRINCIPLED","Hair Tint":"BSDF_HAIR_PRINCIPLED","Hair Melanin Redness":"BSDF_HAIR_PRINCIPLED","Hair Melanin":"BSDF_HAIR_PRINCIPLED","Hair Color":"BSDF_HAIR_PRINCIPLED","Hair Radial Roughness":"BSDF_HAIR_PRINCIPLED","Hair Aspect Ratio":"BSDF_HAIR_PRINCIPLED","Hair Secondary Reflection":"BSDF_HAIR_PRINCIPLED","Hair Random Roughness":"BSDF_HAIR_PRINCIPLED","Hair Transmission":"BSDF_HAIR_PRINCIPLED","Hair Reflection":"BSDF_HAIR_PRINCIPLED","Hair Random":"BSDF_HAIR_PRINCIPLED","Hair Offset":"BSDF_HAIR_PRINCIPLED","Hair Roughness":"BSDF_HAIR_PRINCIPLED","Hair IOR":"BSDF_HAIR_PRINCIPLED","Hair Tangent N":"BSDF_HAIR","Hair RoughnessV N":"BSDF_HAIR","Hair RoughnessU N":"BSDF_HAIR","Hair Offset N":"BSDF_HAIR","Hair Color N":"BSDF_HAIR","Glossy Tangent":"BSDF_GLOSSY","Glossy Normal":"BSDF_GLOSSY","Glossy Rotation":"BSDF_GLOSSY","Glossy Anisotropy":"BSDF_GLOSSY","Glossy Roughness":"BSDF_GLOSSY","Glossy Color":"BSDF_GLOSSY","Glass Normal":"BSDF_GLASS","Glass IOR":"BSDF_GLASS","Glass Roughness":"BSDF_GLASS","Glass Color":"BSDF_GLASS","Emission N":"EMISSION","Emission Strength N":"EMISSION","Emission Color N":"EMISSION","Metallic Extinction":"BSDF_METALLIC","Metallic IOR":"BSDF_METALLIC","Metallic Edge Tint":"BSDF_METALLIC","Metallic Color":"BSDF_METALLIC","Metallic Tangent":"BSDF_METALLIC","Metallic Normal":"BSDF_METALLIC","Metallic Rotation":"BSDF_METALLIC","Metallic Anisotropy":"BSDF_METALLIC","Metallic Roughness":"BSDF_METALLIC","Diffuse Normal":"BSDF_DIFFUSE","Diffuse Roughness N":"BSDF_DIFFUSE","Diffuse Color":"BSDF_DIFFUSE","Tangent":"BSDF_PRINCIPLED","Subsurface Radius":"BSDF_PRINCIPLED","Subsurface IOR": "BSDF_PRINCIPLED", "Emission": "BSDF_PRINCIPLED", "Multires Displacement": "OUTPUT_MATERIAL", "Multires Normal": "BSDF_PRINCIPLED", "Cavity": "BSDF_PRINCIPLED", "Thickness": "BSDF_PRINCIPLED", "Combine": "OUTPUT_MATERIAL", "Thin Film IOR": "BSDF_PRINCIPLED", "Thin Film Thickness": "BSDF_PRINCIPLED", "Sheen Tint": "BSDF_PRINCIPLED", "Sheen Roughness": "BSDF_PRINCIPLED", "Sheen Weight": "BSDF_PRINCIPLED", "Coat Tint": "BSDF_PRINCIPLED", "Coat IOR": "BSDF_PRINCIPLED", "Coat Roughness": "BSDF_PRINCIPLED", "Coat Weight": "BSDF_PRINCIPLED", "Transmission Weight": "BSDF_PRINCIPLED", "Anisotropic Rotation": "BSDF_PRINCIPLED", "Anisotropic": "BSDF_PRINCIPLED", "Specular Tint": "BSDF_PRINCIPLED", "Specular IOR Level": "BSDF_PRINCIPLED", "Subsurface Anisotropy": "BSDF_PRINCIPLED", "Subsurface Scale": "BSDF_PRINCIPLED", "Subsurface Weight": "BSDF_PRINCIPLED", "Displacement Midlevel": "DISPLACEMENT", "Normal": "BSDF_PRINCIPLED", "Alpha": "BSDF_PRINCIPLED", "Base Color": "BSDF_PRINCIPLED",
                                 "Metallic": "BSDF_PRINCIPLED", "Emission Color": "BSDF_PRINCIPLED", "Roughness": "BSDF_PRINCIPLED", "Ambient Occlusion": "BSDF_PRINCIPLED", "Emission Strength": "BSDF_PRINCIPLED", "Displacement Height": "DISPLACEMENT", "Displacement Scale": "DISPLACEMENT",
                                 "Bump Strength": "BUMP","Filter Width": "BUMP",
                                 "Bump Height": "BUMP", "Bump Distance": "BUMP", "IOR": "BSDF_PRINCIPLED"}
    bpy.types.Scene.inputNodeNames = {"Filter Width":"Filter Width","Coat Normal":"Coat Normal","Diffuse Roughness":"Diffuse Roughness","Volume Scatter Diameter":"Diameter","Volume Scatter Alpha":"Alpha","Volume Scatter Backscatter":"Backscatter","Volume Scatter IOR":"IOR","Volume Scatter Anisotropy":"Anisotropy","Volume Scatter Density":"Density","Volume Scatter Color":"Color","Translucent Normal":"Normal","Translucent Color":"Color","Transparent Color":"Color","Volume Absorption Density":"Density","Volume Absorption Color N":"Color","Toon Normal":"Normal","Toon Smooth":"Smooth","Toon Size":"Size","Toon Color":"Color","Sheen Normal":"Normal","Sheen Roughness N":"Roughness","Sheen Color":"Color","Ray Portal Direction":"Direction","Ray Portal Position":"Position","Ray Portal Color":"Color","Subsurface Scattering IOR":"IOR","Subsurface Scattering Anisotropy":"Anisotropy","Subsurface Scattering Roughness":"Roughness","Subsurface Scattering Normal":"Normal","Subsurface Scattering Radius":"Radius","Subsurface Scattering Scale":"Scale","Subsurface Scattering Color":"Color","Specular Clear Coat Normals":"Clear Coat Normal","Specular Clear Coat Roughness":"Clear Coat Roughness","Specular Clear Coat":"Clear Coat","Specular Normal":"Normal","Specular Transparency":"Transparency","Specular Emissive Color":"Emissive Color","Specular Roughness":"Roughness","Specular Specular":"Specular","Specular Base Color":"Base Color","Refraction Normal":"Normal","Refraction IOR":"IOR","Refraction Roughness":"Roughness","Refraction Color":"Color","Volume Temperature":"Temperature","Volume Blackbody Tint":"Blackbody Tint","Volume Blackbody Intensity":"Blackbody Intensity","Volume Emission Color":"Emission Color","Volume Emission Strength":"Emission Strength","Volume Absorption Color":"Absorption Color","Volume Anisotropy":"Anisotropy","Volume Density":"Density","Volume Color":"Color","Hair Absorption Coefficient":"Absorption Coefficient","Hair Coat":"Coat","Hair Random Color":"Random Color","Hair Tint":"Tint","Hair Melanin Redness":"Melanin Redness","Hair Melanin":"Melanin","Hair Color":"Color","Hair Radial Roughness":"Radial Roughness","Hair Aspect Ratio":"Aspect Ratio","Hair Secondary Reflection":"Secondary Reflection","Hair Random Roughness":"Random Roughness","Hair Transmission":"Transmission","Hair Reflection":"Reflection","Hair Random":"Random","Hair Offset":"Offset","Hair Roughness":"Roughness","Hair IOR":"IOR","Hair Tangent N":"Tangent","Hair RoughnessV N":"RoughnessV","Hair RoughnessU N":"RoughnessU","Hair Offset N":"Offset","Hair Color N":"Color","Glossy Tangent":"Tangent","Glossy Normal":"Normal","Glossy Rotation":"Rotation","Glossy Anisotropy":"Anisotropy","Glossy Roughness":"Roughness","Glossy Color":"Color","Glass Normal":"Normal","Glass IOR":"IOR","Glass Roughness":"Roughness","Glass Color":"Color","Emission N":"Color","Emission Strength N":"Strength","Emission Color N":"Color","Metallic Extinction":"Extinction","Metallic IOR":"IOR","Metallic Edge Tint":"Edge Tint","Metallic Color":"Base Color","Metallic Tangent":"Tangent","Metallic Normal":"Normal","Metallic Rotation":"Rotation","Metallic Anisotropy":"Anisotropy","Metallic Roughness":"Roughness","Diffuse Normal":"Normal","Diffuse Roughness N":"Roughness","Diffuse Color":"Color","Material OutPut Surface":"Surface","Tangent":"Tangent","Subsurface Radius":"Subsurface Radius","Subsurface IOR": "Subsurface IOR", "Emission": "Emission Color", "Multires Displacement": "Displacement", "Multires Normal": "Normal", "Cavity": "Base Color", "Thickness": "Base Color", "Combine": "Surface", "Thin Film IOR": "Thin Film IOR", "Thin Film Thickness": "Thin Film Thickness", "Sheen Tint": "Sheen Tint", "Sheen Roughness": "Sheen Roughness", "Sheen Weight": "Sheen Weight", "Coat Tint": "Coat Tint", "Coat IOR": "Coat IOR", "Coat Roughness": "Coat Roughness", "Coat Weight": "Coat Weight", "Transmission Weight": "Transmission Weight", "Anisotropic Rotation": "Anisotropic Rotation", "Anisotropic": "Anisotropic", "Specular Tint": "Specular Tint", "Specular IOR Level": "Specular IOR Level", "Subsurface Anisotropy": "Subsurface Anisotropy", "Subsurface Scale": "Subsurface Scale", "Subsurface Weight": "Subsurface Weight", "IOR": "IOR", "Bump Strength": "Strength",
                                      "Bump Height": "Height", "Bump Distance": "Distance", "Displacement Midlevel": "Midlevel", "Normal": "Normal", "Alpha": "Alpha", "Base Color": "Base Color",
                                      "Metallic": "Metallic", "Emission Color": "Emission Color", "Roughness": "Roughness", "Ambient Occlusion": "Base Color", "Emission Strength": "Emission Strength", "Displacement Height": "Height", "Displacement Scale": "Scale"}
    bpy.types.Scene.BakingSelection = {"Volume Scatter Diameter":"EMIT","Filter Width":"EMIT","Coat Normal":"EMIT","Diffuse Roughness":"EMIT","Volume Scatter Alpha":"EMIT","Volume Scatter Backscatter":"EMIT","Volume Scatter IOR":"EMIT","Volume Scatter Anisotropy":"EMIT","Volume Scatter Density":"EMIT","Volume Scatter Color":"EMIT","Translucent Normal":"NORMAL","Translucent Color":"EMIT","Transparent Color":"EMIT","Volume Absorption Density":"EMIT","Volume Absorption Color N":"EMIT","Toon Normal":"NORMAL","Toon Smooth":"EMIT","Toon Size":"EMIT","Toon Color":"EMIT","Sheen Normal":"NORMAL","Sheen Roughness N":"EMIT","Sheen Color":"EMIT","Ray Portal Direction":"EMIT","Ray Portal Position":"EMIT","Ray Portal Color":"EMIT","Subsurface Scattering IOR":"EMIT","Subsurface Scattering Anisotropy":"EMIT","Subsurface Scattering Roughness":"EMIT","Subsurface Scattering Normal":"NORMAL","Subsurface Scattering Radius":"EMIT","Subsurface Scattering Scale":"EMIT","Subsurface Scattering Color":"EMIT","Specular Clear Coat Normals":"NORMAL","Specular Clear Coat Roughness":"EMIT","Specular Clear Coat":"EMIT","Specular Normal":"NORMAL","Specular Transparency":"EMIT","Specular Emissive Color":"EMIT","Specular Roughness":"EMIT","Specular Base Color":"EMIT","Refraction Normal":"NORMAL","Refraction IOR":"EMIT","Refraction Roughness":"EMIT","Refraction Color":"EMIT","Volume Temperature":"EMIT","Volume Blackbody Tint":"EMIT","Volume Blackbody Intensity":"EMIT","Volume Emission Color":"EMIT","Volume Emission Strength":"EMIT","Volume Absorption Color":"EMIT","Volume Anisotropy":"EMIT","Volume Density":"EMIT","Volume Color":"EMIT","Hair Absorption Coefficient":"EMIT","Hair Coat":"EMIT","Hair Random Color":"EMIT","Hair Tint":"EMIT","Hair Melanin Redness":"EMIT","Hair Melanin":"EMIT","Hair Color":"EMIT","Hair Radial Roughness":"EMIT","Hair Aspect Ratio":"EMIT","Hair Secondary Reflection":"EMIT","Hair Random Roughness":"EMIT","Hair Transmission":"EMIT","Hair Reflection":"EMIT","Hair Random":"EMIT","Hair Offset":"EMIT","Hair Roughness":"EMIT","Hair IOR":"EMIT","Hair Tangent N":"EMIT","Hair RoughnessV N":"EMIT","Hair RoughnessU N":"EMIT","Hair Offset N":"EMIT","Hair Color N":"EMIT","Glossy Tangent":"EMIT","Glossy Normal":"NORMAL","Glossy Rotation":"EMIT","Glossy Anisotropy":"EMIT","Glossy Roughness":"EMIT","Glossy Color":"EMIT","Glass Normal":"NORMAL","Glass IOR":"EMIT","Glass Roughness":"EMIT","Glass Color":"EMIT","Emission N":"EMIT","Emission Strength N":"EMIT","Emission Color N":"EMIT","Metallic Extinction":"EMIT","Metallic IOR":"EMIT","Metallic Edge Tint":"EMIT","Metallic Color":"EMIT","Metallic Tangent":"EMIT","Metallic Normal":"NORMAL","Metallic Rotation":"EMIT","Metallic Anisotropy":"EMIT","Tangent":"EMIT","Subsurface Radius":"EMIT","Subsurface IOR": "EMIT", "Emission": "EMIT", "Multires Displacement": "DISPLACEMENT", "Multires Normal": "NORMAL","Diffuse Normal":"NORMAL", "Cavity": "EMIT", "Thickness": "EMIT", "Combine": "COMBINED", "Thin Film IOR": "EMIT", "Thin Film Thickness": "EMIT", "Sheen Tint": "EMIT", "Sheen Roughness": "EMIT", "Sheen Weight": "EMIT", "Coat Tint": "EMIT", "Coat IOR": "EMIT", "Coat Roughness": "EMIT", "Coat Weight": "EMIT", "Transmission Weight": "EMIT", "Anisotropic Rotation": "EMIT", "Anisotropic": "EMIT", "Specular Tint": "EMIT", "Specular IOR Level": "EMIT", "Subsurface Anisotropy": "EMIT", "Subsurface Scale": "EMIT", "Subsurface Weight": "EMIT", "Bump Strength": "EMIT", "Bump Height": "EMIT", "Bump Distance": "EMIT", "Displacement Midlevel": "EMIT", "Normal": "NORMAL", "Alpha": "EMIT", "Base Color": "DIFFUSE","Diffuse Color":"DIFFUSE","Specular Specular":"EMIT",
                                       "Metallic": "EMIT", "Emission Color": "EMIT", "Roughness": "ROUGHNESS", "Ambient Occlusion": "AO", "Emission Strength": "EMIT", "Displacement Height": "EMIT", "Displacement Scale": "EMIT", "IOR": "EMIT","Diffuse Roughness N":"DIFFUSE","Metallic Roughness":"ROUGHNESS"}
    bpy.types.Scene.BakeTypes = {"Base Color": "Base Color", "Metallic": "Metallic", "Roughness": "Roughness","IOR": "IOR","Alpha": "Alpha", "Normal": "Normal","Diffuse Roughness": "Diffuse Roughness",
                                 "Subsurface Weight": "Subsurface Weight","Subsurface Radius": "Subsurface Radius","Subsurface Scale": "Subsurface Scale",
                                "Subsurface IOR": "Subsurface IOR","Subsurface Anisotropy": "Subsurface Anisotropy","Specular IOR Level": "Specular IOR Level","Specular Tint": "Specular Tint",
                                "Anisotropic": "Anisotropic","Anisotropic Rotation": "Anisotropic Rotation","Tangent": "Tangent", 
                                "Transmission Weight": "Transmission Weight","Coat Weight": "Coat Weight", "Coat Roughness": "Coat Roughness", 
                                "Coat IOR": "Coat IOR","Coat Tint": "Coat Tint","Coat Normal":"Coat Normal","Sheen Weight": "Sheen Weight","Sheen Roughness": "Sheen Roughness",
                                "Sheen Tint": "Sheen Tint","Emission Color": "Emission Color","Emission Strength": "Emission Strength","Emission": "Emission",  
                                "Thin Film Thickness": "Thin Film Thickness", "Thin Film IOR": "Thin Film IOR", 
                                
                                "Bump Strength": "Strength", "Bump Distance": "Distance","Filter Width": "Filter Width","Bump Height": "Height", 

                                "Multires Displacement": "Displacement", "Multires Normal": "Normal",

                                "Cavity": "Cavity", "Thickness": "Thickness", "Ambient Occlusion": "Ambient Occlusion","Combine": "Combine", 

                                "Displacement Height": "Height","Displacement Midlevel": "Midlevel", "Displacement Scale": "Scale",

                                "Diffuse Color": "Color", "Diffuse Roughness N": "Roughness","Diffuse Normal": "Normal", 
                                
                                "Metallic Color": "Base Color","Metallic Edge Tint": "Edge Tint","Metallic IOR": "IOR","Metallic Extinction": "Extinction",
                                "Metallic Roughness": "Roughness","Metallic Anisotropy": "Anisotropy","Metallic Rotation": "Rotation","Metallic Normal": "Normal",
                                "Metallic Tangent": "Tangent",  
                                 
                                "Emission N":"Emission","Emission Color N": "Color","Emission Strength N": "Strength",

                                "Glass Color": "Color", "Glass Roughness": "Roughness","Glass IOR": "IOR", "Glass Normal": "Normal",
                                 
                                "Glossy Color": "Color", "Glossy Roughness": "Roughness","Glossy Anisotropy": "Anisotropy", "Glossy Rotation": "Rotation",
                                "Glossy Normal": "Normal","Glossy Tangent": "Tangent",

                                "Hair Color N": "Color","Hair Offset N": "Offset","Hair RoughnessU N": "RoughnessU", "Hair RoughnessV N": "RoughnessV","Hair Tangent N": "Tangent",
                                
                                "Hair Color": "Color","Hair Roughness": "Roughness","Hair Radial Roughness": "Radial Roughness","Hair Coat": "Coat",
                                "Hair IOR": "IOR","Hair Offset": "Offset","Hair Random Roughness": "Random Roughness","Hair Random": "Random","Hair Aspect Ratio": "Aspect Ratio",
                                "Hair Reflection": "Reflection","Hair Transmission": "Transmission","Hair Secondary Reflection": "Secondary Reflection",
                                "Hair Melanin": "Melanin","Hair Melanin Redness": "Melanin Redness","Hair Tint": "Tint","Hair Random Color": "Random Color",
                                "Hair Absorption Coefficient": "Absorption Coefficient",
                
                                "Volume Color": "Color","Volume Density": "Density", "Volume Anisotropy": "Anisotropy","Volume Absorption Color": "Absorption Color", 
                                "Volume Emission Strength": "Emission Strength","Volume Emission Color": "Emission Color","Volume Blackbody Intensity": "Blackbody Intensity",
                                "Volume Blackbody Tint": "Blackbody Tint","Volume Temperature": "Temperature",
                                
                                
                                 
                                 "Refraction Color":"Color","Refraction Roughness":"Roughness","Refraction IOR":"IOR","Refraction Normal":"Normal",


                                "Specular Base Color":"Base Color","Specular Specular":"Specular","Specular Roughness":"Roughness",
                                "Specular Emissive Color":"Emissive Color","Specular Transparency":"Transparency","Specular Normal":"Normal",
                                "Specular Clear Coat":"Clear Coat","Specular Clear Coat Roughness":"Clear Coat Roughness","Specular Clear Coat Normals":"Clear Coat Normals",
                                
                                "Subsurface Scattering Color":"Color","Subsurface Scattering Scale":"Scale","Subsurface Scattering Radius":"Radius",
                                "Subsurface Scattering Normal":"Normal","Subsurface Scattering Roughness":"Roughness",
                                "Subsurface Scattering Anisotropy":"Anisotropy","Subsurface Scattering IOR":"IOR",

                                "Ray Portal Color":"Color","Ray Portal Position":"Position","Ray Portal Direction":"Direction",

                                "Sheen Color":"Color","Sheen Roughness N":"Roughness","Sheen Normal":"Normal",

                                "Toon Color":"Color","Toon Size":"Size","Toon Smooth":"Smooth","Toon Normal":"Normal",
                                
                                "Volume Absorption Color N":"Color","Volume Absorption Density":"Density",
                                
                                "Transparent Color":"Color","Translucent Color":"Color",

                                "Translucent Normal":"Normal",
                                
                                "Volume Scatter Color":"Color","Volume Scatter Density":"Density",
                                "Volume Scatter Anisotropy":"Anisotropy","Volume Scatter IOR":"IOR","Volume Scatter Backscatter":"Backscatter",
                                "Volume Scatter Alpha":"Alpha","Volume Scatter Diameter":"Diameter",}
    

    bpy.types.Scene.requiresConnection = {"Diffuse Normal": "Normal", "Metallic Normal": "Normal", "Glass Normal": "Normal", "Glossy Normal": "Normal", "Refraction Normal": "Normal", "Specular Normal": "Normal", "Specular Clear Coat Normals": "Normal", "Subsurface Scattering Normal": "Normal", "Sheen Normal": "Normal", "Toon Normal": "Normal", "Translucent Normal": "Normal","Translucent Color": "Emission Color", "Toon Color": "Emission Color", "Filter Width": "Emission Strength", "Coat Normal": "Emission Strength", "Diffuse Roughness": "Emission Strength", "Emission Strength": "Emission Strength", "Emission Color": "Emission Color", "Volume Scatter Diameter": "Emission Strength", "Volume Scatter Alpha": "Emission Strength", "Volume Scatter Backscatter": "Emission Strength", "Volume Scatter IOR": "Emission Strength", "Volume Scatter Anisotropy": "Emission Strength", "Volume Scatter Density": "Emission Strength", "Volume Scatter Color": "Emission Color", "Transparent Color": "Emission Color", "Volume Absorption Density": "Emission Strength", "Volume Absorption Color": "Emission Color", "Toon Smooth": "Emission Strength", "Toon Size": "Emission Strength", "Sheen Color": "Emission Color", "Ray Portal Roughness": "Emission Strength", "Ray Portal Direction": "Emission Color", "Ray Portal Position": "Emission Color", "Ray Portal Color": "Emission Color", "Subsurface Scattering IOR": "Emission Strength", "Subsurface Scattering Anisotropy": "Emission Strength", "Subsurface Scattering Roughness": "Emission Strength", "Subsurface Scattering Radius": "Emission Color", "Subsurface Scattering Scale": "Emission Strength", "Subsurface Scattering Color": "Emission Color", "Specular Clear Coat Roughness": "Emission Strength", "Specular Clear Coat": "Emission Strength", "Specular Transparency": "Emission Strength", "Specular Emissive Color": "Emission Color", "Specular Roughness": "Emission Strength", "Specular Specular": "Emission Color", "Specular Base Color": "Emission Color", "Refraction IOR": "Emission Strength", "Refraction Roughness": "Emission Strength", "Refraction Color": "Emission Color", "Volume Temperature": "Emission Strength", "Volume Blackbody Tint": "Emission Color", "Volume Blackbody Intensity": "Emission Strength", "Volume Emission Color": "Emission Color", "Volume Emission Strength": "Emission Strength", "Volume Absorption Color N": "Emission Color", "Volume Anisotropy": "Emission Strength", "Volume Density": "Emission Strength", "Volume Color": "Emission Color", "Hair Absorption Coefficient": "Emission Color", "Hair Random Color": "Emission Strength", "Hair Tint": "Emission Color", "Hair Melanin Redness": "Emission Strength", "Hair Melanin": "Emission Strength", "Hair Color": "Emission Color", "Hair Aspect Ratio": "Emission Strength", "Hair Secondary Reflection": "Emission Strength", "Hair Coat": "Emission Strength", "Hair Radial Roughness": "Emission Strength", "Hair Random Roughness": "Emission Strength", "Hair Transmission": "Emission Strength", "Hair Reflection": "Emission Strength", "Hair Random": "Emission Strength", "Hair Offset": "Emission Strength", "Hair Roughness": "Emission Strength", "Hair IOR": "Emission Strength", "Hair Tangent N": "Emission Color", "Hair RoughnessV N": "Emission Strength", "Hair RoughnessU N": "Emission Strength", "Hair Offset N": "Emission Strength", "Hair Color N": "Emission Color", "Glossy Tangent": "Emission Color", "Glossy Rotation": "Emission Strength", "Glossy Anisotropy": "Emission Strength", "Glossy Roughness": "Emission Strength", "Glossy Color": "Emission Color", "Glass IOR": "Emission Strength", "Glass Roughness": "Emission Strength", "Glass Color": "Emission Color", "Metallic Extinction": "Emission Color", "Metallic IOR": "Emission Color", "Metallic Edge Tint": "Emission Color", "Metallic Color": "Emission Color", "Metallic Tangent": "Emission Color", "Metallic Rotation": "Emission Strength", "Metallic Anisotropy": "Emission Strength", "Cavity": "Emission Strength", "Thickness": "Emission Strength", "Displacement Height": "Emission Strength", "Displacement Midlevel": "Emission Strength", "Displacement Scale": "Emission Strength", "Tangent": "Emission Color", "Subsurface Radius": "Emission Color", "Subsurface IOR": "Emission Strength", "Alpha": "Emission Strength", "Thin Film IOR": "Emission Strength", "Thin Film Thickness": "Emission Strength", "Sheen Tint": "Emission Color", "Sheen Roughness N": "Emission Strength", "Sheen Roughness": "Emission Strength", "Sheen Weight": "Emission Strength", "Coat Tint": "Emission Color", "Coat IOR": "Emission Strength", "Coat Roughness": "Emission Strength", "Coat Weight": "Emission Strength", "Transmission Weight": "Emission Strength", "Anisotropic Rotation": "Emission Strength", "Anisotropic": "Emission Strength", "Specular Tint": "Emission Color", "Specular IOR Level": "Emission Strength", "Subsurface Anisotropy": "Emission Strength", "Subsurface Scale": "Emission Strength", "Subsurface Weight": "Emission Strength", "Bump Strength": "Emission Strength", "Bump Height": "Emission Strength", "Bump Distance": "Emission Strength", "Metallic": "Emission Strength", "IOR": "Emission Strength"}
    bpy.types.Scene.requiresDefaultValue = {}
    bpy.types.Scene.RequireAfterProcess = {
        "Emission": {"Emission Strength": 1},"Emission N":{"Strength": 1}}
    bpy.types.Scene.ConvertInput={"Displacement Height": "Surface","Displacement Midlevel": "Surface", "Displacement Scale": "Surface","Volume Color": "Surface", "Volume Density": "Surface", "Volume Anisotropy": "Surface", "Volume Absorption Color": "Surface", "Volume Emission Strength": "Surface", "Volume Emission Color": "Surface", "Volume Blackbody Intensity": "Surface", "Volume Blackbody Tint": "Surface", "Volume Temperature": "Surface", "Volume Absorption Color N": "Surface", "Volume Absorption Density": "Surface", "Volume Scatter Color": "Surface", "Volume Scatter Density": "Surface", "Volume Scatter Anisotropy": "Surface", "Volume Scatter IOR": "Surface", "Volume Scatter Backscatter": "Surface", "Volume Scatter Alpha": "Surface", "Volume Scatter Diameter": "Surface"}
    bpy.types.Scene.propertyDependentInput = {
        "Volume Scatter Diameter":{"PropertyAccept": ["MIE"], "Property": "phase", "NodeType": "VOLUME_SCATTER"},
        "Volume Scatter Alpha":{"PropertyAccept": ["DRAINE"], "Property": "phase", "NodeType": "VOLUME_SCATTER"},
        "Volume Scatter Backscatter":{"PropertyAccept": ["FOURNIER_FORAND"], "Property": "phase", "NodeType": "VOLUME_SCATTER"},
        "Volume Scatter IOR":{"PropertyAccept": ["FOURNIER_FORAND"], "Property": "phase", "NodeType": "VOLUME_SCATTER"},
        "Volume Scatter Anisotropy":{"PropertyAccept": ["HENYEY_GREENSTEIN","DRAINE"], "Property": "phase", "NodeType": "VOLUME_SCATTER"},
        "Subsurface Scattering IOR":{"PropertyAccept": ["RANDOM_WALK","RANDOM_WALK_SKIN"], "Property": "falloff", "NodeType": "SUBSURFACE_SCATTERING"},
        "Subsurface Scattering Anisotropy":{"PropertyAccept": ["RANDOM_WALK","RANDOM_WALK_SKIN"], "Property": "falloff", "NodeType": "SUBSURFACE_SCATTERING"},
        "Subsurface Scattering Roughness":{"PropertyAccept": ["RANDOM_WALK"], "Property": "falloff", "NodeType": "SUBSURFACE_SCATTERING"},
        "Hair Absorption Coefficient":{"PropertyAccept": ["ABSORPTION"], "Property": "parametrization", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Coat":{"PropertyAccept": ["CHIANG"], "Property": "model", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Random Color":{"PropertyAccept": ["MELANIN"], "Property": "parametrization", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Tint":{"PropertyAccept": ["MELANIN"], "Property": "parametrization", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Melanin Redness":{"PropertyAccept": ["MELANIN"], "Property": "parametrization", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Melanin":{"PropertyAccept": ["MELANIN"], "Property": "parametrization", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Color":{"PropertyAccept": ["COLOR"], "Property": "parametrization", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Radial Roughness":{"PropertyAccept": ["CHIANG"], "Property": "model", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Aspect Ratio":{"PropertyAccept": ["HUANG"], "Property": "model", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Secondary Reflection":{"PropertyAccept": ["HUANG"], "Property": "model", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Transmission":{"PropertyAccept": ["HUANG"], "Property": "model", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Hair Reflection":{"PropertyAccept": ["HUANG"], "Property": "model", "NodeType": "BSDF_HAIR_PRINCIPLED"},
        "Metallic Extinction":{"PropertyAccept": ["PHYSICAL_CONDUCTOR"], "Property": "fresnel_type", "NodeType": "BSDF_METALLIC"},
        "Metallic IOR":{"PropertyAccept": ["PHYSICAL_CONDUCTOR"], "Property": "fresnel_type", "NodeType": "BSDF_METALLIC"},
        "Metallic Edge Tint":{"PropertyAccept": ["F82"], "Property": "fresnel_type", "NodeType": "BSDF_METALLIC"},
        "Metallic Color":{"PropertyAccept": ["F82"], "Property": "fresnel_type", "NodeType": "BSDF_METALLIC"},
        "Subsurface IOR": {"PropertyAccept": ["RANDOM_WALK_SKIN"],"Property": "subsurface_method", "NodeType": "BSDF_PRINCIPLED"}, 
        "Subsurface Anisotropy": {"PropertyAccept": ["RANDOM_WALK_SKIN", "RANDOM_WALK"], "Property": "subsurface_method", "NodeType": "BSDF_PRINCIPLED"}}
    

    bpy.types.Scene.packObject = []
    bpy.types.Scene.ColorMaps = ["Base Color", "Diffuse Roughness", "Emission Color", "Diffuse Color", "Diffuse Roughness N", "Diffuse Normal", "Metallic Color", "Emission Color N", "Glass Color", "Glossy Color", "Hair Color N", "Hair Color", "Hair Random Color", "Volume Color", "Volume Absorption Color", "Volume Emission Color", "Refraction Color", "Specular Base Color", "Specular Emissive Color", "Subsurface Scattering Color", "Ray Portal Color", "Sheen Color", "Toon Color", "Volume Absorption Color N", "Transparent Color", "Translucent Color", "Volume Scatter Color"]
    bpy.types.Scene.settingsNames = {"UVIslandMargin": "UV Island Margin", "margin": "Texture margin", "rayDistance": "Ray distance", "extrusion": "Extrusion", "height": "height", "width": "width", "AntialiasingScale": "Anti aliasing Scale",  "UseCustomFolderTree": "Use Custom Folder Tree", "ShadeSmooth": "Shade Smooth", "ConvertRoughnessToSmoothness": "Convert Roughness To Smoothness", "FlipnormalY": "Flip normal Y", "BakeRegardless": "Bake Regardless", "BakeMulitpleSlots": "Bake Mulitple Slots", "CheckUVOverLap": "Check UV OverLap", "CheckUVOverBound": "Check UV Over Bound", "GenerateUvRegardLess": "Generate Uv RegardLess",
                                     "BakeMultiple": "Bake Multiple", "UseUdims": "Use Udims", "CopyNodeGroup": "Copy Node Group", "ApplyMaterial": "Apply Material", "ApplyToCopiedAndHideOriginal": "Apply To Copied And Hide Original", "CopyMaterial": "Copy Material", "Device": "Device", "FileFormat": "File format"}
    bpy.types.Scene.flippingInfo = {"Roughness": {0: True, 1: True, 2: True, 3: True}, "Normal": {
        0: False, 1: True, 2: False, 3: False}}
    
    
    bpy.types.Scene.baseNode = {
        "BUMP": {"Output": "Normal", "Give": "BSDF_PRINCIPLED"}}
    bpy.types.Scene.OneInvert=[".exr"]
    bpy.types.Scene.notRequireBakingWhenBakingAll = ["Emission","Emission N"]
    bpy.types.Scene.flippingColorInfo = {"Roughness": "L", "Normal": "RGBA"}
    
    
    bpy.types.Scene.alwaysRequireMultires = [
        "Multires Displacement", "Multires Normal"]
    bpy.types.Scene.miscBake = ["Ambient Occlusion",
                                "Combine", "Thickness", "Cavity", "Multires Normal", "Multires Displacement"]
    bpy.types.Scene.allwaysRequireBaking = ["Ambient Occlusion",
                                            "Combine", "Thickness", "Cavity", "Multires Normal", "Multires Displacement", "Emission","Emission N"]
    bpy.types.Scene.multiResSetup = {
        "Multires Displacement": {"Node": "ShaderNodeDisplacement", "InputOutputName": "Height", "Output": "Displacement", "OriginInput": "Displacement"}, 
        "Multires Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"},
        "Diffuse Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Metallic Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Glass Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Glossy Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Refraction Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Specular Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Specular Clear Coat Normals": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Subsurface Scattering Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Sheen Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}, 
        "Translucent Normal": {"Node": "ShaderNodeNormalMap", "InputOutputName": "Color", "Output": "Normal", "OriginInput": "Normal"}}
    

    bpy.types.Scene.requiresMaterialOutPutConnection = []
    bpy.types.Scene.propertyWithSpecialDefault = {
        "DISPLACEMENT": [{"Scale": 0}]}
    bpy.types.Scene.Blending = {"Ambient Occlusion": {
        "Properties": {"blend_type": "MULTIPLY", "data_type": "RGBA"}, "Inputs": {"Factor": 1}, "Node": "ShaderNodeMix", "OutPutSocket": "Result", "Connection": {"A": "Base Color", "B": "Ambient Occlusion"}}, "Thickness": {
        "Properties": {"blend_type": "MULTIPLY", "data_type": "RGBA"}, "Inputs": {"Factor": 1}, "Node": "ShaderNodeMix", "OutPutSocket": "Result", "Connection": {"A": "Base Color", "B": "Thickness"}}, "Cavity": {
        "Properties": {"blend_type": "MULTIPLY", "data_type": "RGBA"}, "Inputs": {"Factor": 1}, "Node": "ShaderNodeMix", "OutPutSocket": "Result", "Connection": {"A": "Base Color", "B": "Cavity"}}}
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
        name="Base path", default=bpy.path.abspath("//"), description="Base path for saving textures")
    bpy.types.Scene.JsonExport = f"{bpy.context.scene.basePath}MappingFile/"
    bpy.types.Scene.giveInputSocket = {"NORMAL_MAP": "Color"}
    bpy.types.Scene.SavedSettingFolder = "./Setting"
    bpy.types.Scene.SelectedBakeSavedFolder = "./Bake"
    bpy.types.Scene.PackedSavedFolder = "./Packed"

def Unregister():
    del bpy.types.Scene.ConvertInput
    del bpy.types.Scene.requiredChannels
    del bpy.types.Scene.excludedChannels
    del bpy.types.Scene.inputNodeNamesUi
    del bpy.types.Scene.OneInvert
    del bpy.types.Scene.basePath
    del bpy.types.Scene.JsonExport
    del bpy.types.Scene.PackedSavedFolder
    del bpy.types.Scene.SelectedBakeSavedFolder
    del bpy.types.Scene.SavedSettingFolder
    del bpy.types.Scene.BakeNames
    del bpy.types.Scene.settingsNames
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
    del bpy.types.Scene.requiresMaterialOutPutConnection
    del bpy.types.Scene.requiresConnection
    del bpy.types.Scene.requiresDefaultValue
    del bpy.types.Scene.inputNode
    del bpy.types.Scene.inputNodeNames
    del bpy.types.Scene.propertyWithSpecialDefault
    del bpy.types.Scene.Blending
    del bpy.types.Scene.multipleNode
    del bpy.types.Scene.requireAdditionalNode
    del bpy.types.Scene.bakeTypeColorRamp
    del bpy.types.Scene.propertyWithDependants
    del bpy.types.Scene.giveInputSocket


Register()
