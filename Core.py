import bpy
from typing import List
from bpy.types import Object, ShaderNodeSeparateColor, UVLoopLayers, Material, Node, NodeSocket, ShaderNodeTexImage, Image,  MeshUVLoopLayer, bpy_prop_array, NodeSocketShader
import mathutils
import math
import os
import itertools
import json
from pathlib import Path
import numpy
import cv2
import imageio


os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"


def GetNeedColorRamp(mats: Material, bakeType, outPutSocket: NodeSocket):
    if (bakeType in bpy.context.scene.bakeTypeColorRamp):
        node = mats.node_tree.nodes.new(type="ShaderNodeValToRGB")
        for position, positionValue in enumerate(bpy.context.scene.bakeTypeColorRamp[bakeType]["Positions"]):
            node.color_ramp.elements[position].position = positionValue
        CreatLink(mats, node, outPutSocket, "Fac")
        return node.outputs["Color"]
    return False


def GetNodeSocketFromRequire(mat: Material, bakeTypeInformation: str) -> NodeSocket:
    newNode = mat.node_tree.nodes.new(type=bakeTypeInformation["Node"])
    for properties, inputs in itertools.zip_longest(bakeTypeInformation["Properties"], bakeTypeInformation["Inputs"], fillvalue="Empty"):
        if (properties != "Empty"):
            setattr(newNode, properties,
                    bakeTypeInformation["Properties"][properties])
        if (inputs != "Empty"):
            CreatLink(mat, newNode,
                      bakeTypeInformation["Inputs"][inputs], inputs)
    return newNode.outputs[bakeTypeInformation["OutPutSocket"]]


def PreBakeTypeCheck(input: NodeSocket):

    inputSocketToCheck: NodeSocket = input
    nodeTocheck: Node = input.node
    returnDefaultZero: bool = False
    if (input.is_linked):
        nodeTocheck: Node = input.links[0].from_node
        inputNodeSocketInfor = bpy.context.scene.giveInputSocket
        if (nodeTocheck.type in inputNodeSocketInfor):
            inputSocketToCheck = nodeTocheck.inputs[inputNodeSocketInfor[
                nodeTocheck.type]]
    dependantProperty = bpy.context.scene.propertyWithDependants
    if ((nodeTocheck.type in dependantProperty) and (inputSocketToCheck.name in dependantProperty[nodeTocheck.type])):
        for propertyObject in dependantProperty[nodeTocheck.type][inputSocketToCheck.name]:
            for propertyKey in propertyObject:
                if (type(nodeTocheck.inputs[propertyKey].default_value) == bpy_prop_array):
                    if ((nodeTocheck.inputs[propertyKey].default_value[:] == propertyObject[propertyKey]) and (nodeTocheck.inputs[propertyKey].is_linked == False)):
                        returnDefaultZero = True
                else:
                    if ((nodeTocheck.inputs[propertyKey].default_value == propertyObject[propertyKey]) and (nodeTocheck.inputs[propertyKey].is_linked == False)):
                        returnDefaultZero = True
    if (returnDefaultZero):
        value = input.node.inputs[input.name].default_value
        if (type(value) == bpy_prop_array):
            return [3, (0,)*len((input.node.inputs[input.name].default_value[:]))]
        else:
            return [3, 0]
    return BakeType(inputSocketToCheck)


def BakeType(input: NodeSocket):

    value = input.node.inputs[input.name].default_value
    if (input.is_linked == False):
        if (input.type == "VECTOR"):
            return [0]
        elif (type(value) == bpy_prop_array):
            return [3, (input.node.inputs[input.name].default_value[:])]
        else:
            return [3, input.node.inputs[input.name].default_value]
    ConnectedNode = input.links[0].from_node
    if (ConnectedNode.type == "TEX_IMAGE"):
        if (ConnectedNode.inputs["Vector"].is_linked):
            return [1]
        else:
            if (ConnectedNode.image == None):
                if (type(value) == bpy_prop_array):

                    return [3, (0,)*len((input.node.inputs[input.name].default_value[:]))]
                else:
                    return [3, 0]
            else:
                return [2, ConnectedNode]
    else:
        return [1]


def CombineUvCheck(uvPointRound: int):
    bpy.ops.object.select_all(action="DESELECT")
    udimIds = {}
    useUdim = {}
    useUv = {}
    for obj in bpy.context.scene.my_items:
        mesh = obj.mesh
        useUdim[mesh] = False
        if (bpy.context.scene.GenerateUvRegardLess):
            useUv[mesh] = True
        else:
            useUv[mesh] = False
        tempUdims = []
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = mesh
        uv = mesh.data.uv_layers.active
        if ((bpy.context.scene.UseUdims) and (useUv == False)):
            for i in uv.data:
                vector: mathutils.Vector = i.uv
                if (bpy.context.scene.CheckUVOverBound):
                    if ((0 > round(vector.x, uvPointRound)) or (0 > round(vector.y, uvPointRound))):

                        useUv[mesh] = True
                        break
                if ((vector.x >= 0) and (vector.y >= 0)):
                    xCor = math.ceil(round(vector.x, uvPointRound))-1
                    yCor = (math.ceil(round(vector.y, uvPointRound))-1)*10
                    if (xCor < 1):
                        xCor = 0
                    if (yCor < 1):
                        yCor = 0
                    udimToAdd = 1001+yCor+xCor
                    if (udimToAdd != 1001):
                        useUdim[mesh] = True
                    tempUdims.append(udimToAdd)
        if ((bpy.context.scene.CheckUVOverBound) and (bpy.context.scene.UseUdims == False)):

            for i in uv.data:
                vector: mathutils.Vector = i.uv
                if ((0 > round(vector.x, uvPointRound)) or (round(vector.x, uvPointRound) > 1) or (0 > round(vector.y, uvPointRound)) or (round(vector.y, uvPointRound) > 1)):
                    useUv[mesh] = True
        udimIds[mesh] = list(set(tempUdims))
        if (not bpy.context.scene.BakeMultiple):
            bpy.ops.object.select_all(action="DESELECT")
    if (bpy.context.scene.CheckUVOverLap):
        if (bpy.context.scene.BakeMultiple):

            for obj in bpy.context.scene.my_items:
                mesh = obj.mesh
                mesh.select_set(True)
                bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.scene.tool_settings.use_uv_select_sync = True
            bpy.ops.uv.select_overlap()
            for obj in bpy.context.scene.my_items:
                mesh = obj.mesh
                if (mesh.data.total_face_sel > 0):
                    useUv[mesh] = True
        else:
            for obj in bpy.context.scene.my_items:
                mesh = obj.mesh
                mesh.select_set(True)
                bpy.context.view_layer.objects.active = mesh
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.context.scene.tool_settings.use_uv_select_sync = True
                bpy.ops.uv.select_overlap()
                if (mesh.data.total_face_sel > 0):
                    useUv[mesh] = True
        bpy.ops.object.mode_set(mode="OBJECT")
    return [useUdim, udimIds, useUv]


def CreateUv(useUv: bool) -> List[MeshUVLoopLayer]:
    meshListWithUv = {}
    bpy.ops.object.select_all(action="DESELECT")

    for obj in bpy.context.scene.my_items:
        mesh: Object = obj.mesh
        if (not useUv[mesh]):
            meshListWithUv[mesh] = mesh.data.uv_layers.active
        else:
            New_Uv_map: MeshUVLoopLayer = mesh.data.uv_layers.new(
                name=f"{mesh.name}_UV")
            mesh.data.uv_layers[New_Uv_map.name].active = True
            mesh.data.uv_layers[New_Uv_map.name].active_render = True
            bpy.context.view_layer.objects.active = mesh
            mesh.select_set(True)
            meshListWithUv[mesh] = New_Uv_map
            if (not (bpy.context.scene.BakeMultiple and any(list(useUv.values())))):
                GenerateUv(meshListWithUv)
                bpy.ops.object.select_all(action="DESELECT")
    if (bpy.context.scene.BakeMultiple and any(list(useUv.values()))):
        GenerateUv(meshListWithUv)

    return meshListWithUv


def GenerateUv(meshListWithUv):
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    angleLimit: int = 66
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(
        angleLimit), island_margin=bpy.context.scene.UVIslandMargin)

    for mesh in meshListWithUv:
        mesh.data.uv_layers[meshListWithUv[mesh].name].active = True
        mesh.data.uv_layers[meshListWithUv[mesh].name].active_render = True
    bpy.context.scene.tool_settings.use_uv_select_sync = False
    bpy.ops.object.mode_set(mode="OBJECT")


def removeAndSetUv(mesh: Object, uvMap: MeshUVLoopLayer) -> None:
    uvs: List[UVLoopLayers] = [
        uv.name for uv in mesh.data.uv_layers if uv.name != uvMap.name]
    if (mesh.data.uv_layers[uvMap.name].active_render != True):
        mesh.data.uv_layers[uvMap.name].active_render = True
    if (mesh.data.uv_layers.active != uvMap):
        mesh.data.uv_layers[uvMap.name].active = True
    for uv in uvs:
        mesh.data.uv_layers.remove(
            mesh.data.uv_layers.get(uv))


def CopySetMaterial(mesh: Object, index: int) -> Material:
    name = bpy.context.scene.CopiedMaterialName
    mat: Material = mesh.material_slots[index].material.copy()
    mesh.material_slots[index].material = mat
    if (name != ""):
        name = name.replace("[mat]", mat.name)
        name = name.replace("[Object]", mesh.name)
        mat.name = name
    return mat


def addImageNode(mats: Material, uvMap: MeshUVLoopLayer, mesh: Object, useUdims: bool, udimCount: int, actMat, imageObj, exisitingImage=None) -> Image:
    imageTexture: ShaderNodeTexImage = mats.node_tree.nodes.new(
        type="ShaderNodeTexImage")
    if (exisitingImage == None):
        NewImg = GetNewImage(actMat.name, useUdims,
                             udimCount, mesh.name, imageObj)
    else:
        NewImg = exisitingImage
    mesh.data.uv_layers[uvMap.name].active = True
    mesh.data.uv_layers[uvMap.name].active_render = True

    imageTexture.image = NewImg
    for node in mats.node_tree.nodes:
        node.select = False

    imageTexture.select = True
    mats.node_tree.nodes.active = imageTexture

    return imageTexture


def GetNewImage(mats, useUdims, udimCount, mesh, imageObj):
    fileName = GetImageName(mats, mesh, imageObj)
    NewImg: Image = bpy.data.images.new(
        fileName, round(bpy.context.scene.height*bpy.context.scene.AntialiasingScale), round(bpy.context.scene.width*bpy.context.scene.AntialiasingScale), float_buffer=imageObj.float, alpha=True, tiled=useUdims)
    NewImg.colorspace_settings.name = imageObj.space
    if (useUdims and len(udimCount) > 0):
        NewImg.source = "TILED"
    if (useUdims):
        areaTypeOld = bpy.context.area.ui_type
        bpy.context.area.ui_type = "IMAGE_EDITOR"
        bpy.context.space_data.image = NewImg
        for i in udimCount:
            bpy.ops.image.tile_add(
                number=i, generated_type="BLANK", alpha=True, float=True, fill=True)
        bpy.context.area.ui_type = areaTypeOld
    return NewImg


def AddRestOfImageNode(bakesImage: ShaderNodeTexImage, mats: Material):
    imageTexture: ShaderNodeTexImage = mats.node_tree.nodes.new(
        type="ShaderNodeTexImage")
    imageTexture.image = bakesImage.image
    for node in mats.node_tree.nodes:
        node.select = False
    imageTexture.select = True
    mats.node_tree.nodes.active = imageTexture


def BreakLink(ConnectionNode: Node, mats: Material, mapType: str):

    input: NodeSocket = ConnectionNode.inputs[mapType]
    hasLinks: bool = False

    if (input.is_linked):
        hasLinks = True
        FromSocket: Node = input.links[0].from_socket
        mats.node_tree.links.remove(input.links[0])
    if (type(input) == NodeSocketShader):
        if (hasLinks):
            return FromSocket
        else:
            return None
    tempNode = mats.node_tree.nodes.new(type=ConnectionNode.bl_idname)
    defaultValue = tempNode.inputs[mapType]

    if (type(input.default_value) == bpy_prop_array):
        breakedInputValue = input.default_value[:]
    else:
        breakedInputValue = input.default_value
    if (type(input.default_value) == float or type(input.default_value) == int):
        input.default_value = defaultValue.default_value
    elif (type(input.default_value) == bpy_prop_array):
        input.default_value = defaultValue.default_value[:]
    mats.node_tree.nodes.remove(tempNode)
    if (hasLinks):
        return FromSocket
    else:
        return breakedInputValue


def CreatLink(mats: Material, InputValueNode: Node, OutPutValueNode: NodeSocket, mapType: str):
    if ((type(OutPutValueNode) == float) or (type(OutPutValueNode) == int)):
        if (InputValueNode.inputs[mapType].is_linked):
            mats.node_tree.links.remove(
                InputValueNode.inputs[mapType].links[0])
        if (type(InputValueNode.inputs[mapType].default_value) == float or type(InputValueNode.inputs[mapType].default_value) == int):
            InputValueNode.inputs[mapType].default_value = OutPutValueNode
        else:
            InputValueNode.inputs[mapType].default_value[:] = (
                OutPutValueNode,)*len(InputValueNode.inputs[mapType].default_value[:])
    elif (type(OutPutValueNode) == tuple):
        if (InputValueNode.inputs[mapType].is_linked):
            mats.node_tree.links.remove(
                InputValueNode.inputs[mapType].links[0])
        if (type(InputValueNode.inputs[mapType].default_value) == float or type(InputValueNode.inputs[mapType].default_value) == int):
            InputValueNode.inputs[mapType].default_value = OutPutValueNode[0]
        else:
            InputValueNode.inputs[mapType].default_value[:] = OutPutValueNode
    else:
        input: NodeSocket = InputValueNode.inputs[mapType]
        mats.node_tree.links.new(input, OutPutValueNode)


def GetInputNode(mats: Material, NodeType: str, bakeType=None) -> Node:
    nodeGroupsList: List[Node] = []
    nodeList: List[Node] = []
    nodeList.extend(mats.node_tree.nodes)
    for node in nodeList:
        propertyDependentInput = bpy.context.scene.propertyDependentInput
        if (bakeType in propertyDependentInput and propertyDependentInput[bakeType]["NodeType"] == NodeType):
            propertyDependInfo = propertyDependentInput[bakeType]
            if (getattr(node, propertyDependInfo["Property"]) not in propertyDependInfo["PropertyAccept"]):
                # here maybe
                continue
        if (node.type == NodeType):
            return [node, mats]
        elif (type(node) == bpy.types.ShaderNodeGroup):
            nodeGroupsList.append(node)
    for nodeGroup in nodeGroupsList:
        result = GetInputNode(nodeGroup, NodeType, bakeType)
        if (result != False):
            return result
    return False


def GetAllInputNode(mats: Material, NodeType: str, bakeType: str = None) -> Node:
    nodeGroupsList: List[Node] = []
    nodeList: List[Node] = []
    nodeList.extend(mats.node_tree.nodes)
    foundNodes = []

    for node in nodeList:
        if (node.type == NodeType):
            if (node.type == "BUMP" and (node.inputs["Normal"].is_linked)):
                # here maybe
                continue
            inputName = bpy.context.scene.inputNodeNames[bakeType]
            propertyDependentInput = bpy.context.scene.propertyDependentInput
            if (bakeType in propertyDependentInput and propertyDependentInput[bakeType]["NodeType"] == NodeType):
                propertyDependInfo = propertyDependentInput[bakeType]
                if (getattr(node, propertyDependInfo["Property"]) not in propertyDependInfo["PropertyAccept"]):
                    # here maybe
                    continue
            if (node.inputs[inputName].is_linked):
                foundNodes.append(
                    [node, mats, node.inputs[inputName].links[0].from_socket])
            else:
                if (type(node.inputs[inputName].default_value) == int or type(node.inputs[inputName].default_value) == float):
                    foundNodes.append(
                        [node, mats, node.inputs[inputName].default_value])
                else:
                    foundNodes.append(
                        [node, mats, node.inputs[inputName].default_value[:]])
        elif (type(node) == bpy.types.ShaderNodeGroup):
            nodeGroupsList.append(node)
    for nodeGroup in nodeGroupsList:
        result = GetAllInputNode(nodeGroup, NodeType, bakeType)
        if (type(result) != List):
            foundNodes.extend(result)
    multipleNodeInfo = bpy.context.scene.multipleNode
    if (foundNodes.__len__() <= 0):
        # here maybe
        return [False, f"No {NodeType} node found in {mats.name}"]
    elif ((foundNodes.__len__() > 1) and (multipleNodeInfo[NodeType][0] == True)):
        return foundNodes
    elif ((foundNodes.__len__() > 1) and (multipleNodeInfo[NodeType][0] == False)):
        return [False, f"Multiple {NodeType} node found in {mats.name}"]
    else:
        return foundNodes


def GetRequiredChannels():
    requiredChannels = {"Emission": ["Emission Color", "Emission Strength"]}
    return requiredChannels


def bakeMap(uv: MeshUVLoopLayer, mesh: Object, bakeType: str, useUdims: bool, udimCount: list[int],  imageObj, selected, existingImages=None):
    ImageBakeData = {}
    selectedToActiveDate = {}
    defaultData = {}
    nodesToDelete = {}
    allReadyHasImage = {}
    allReadyHasSlectedImage = {}
    inputNodeType = bpy.context.scene.inputNode
    inputNodeName = bpy.context.scene.inputNodeNames
    requiredChannels = GetRequiredChannels()
    excludedChannels = {"Subsurface IOR": [], "Thin Film IOR": [], "Thin Film Thickness": [], "Sheen Tint": [], "Sheen Roughness": [], "Sheen Weight": [], "Coat Tint": [], "Coat IOR": [], "Coat Roughness": [], "Coat Weight": [], "Transmission Weight": [], "Anisotropic Rotation": [], "Anisotropic": [], "Specular Tint": [], "Specular IOR Level": [], "Subsurface Anisotropy": [], "Subsurface Scale": [], "Subsurface Weight": [], "Alpha": [], "Base Color": [],
                        "Metallic": [], "Emission Color": [], "Roughness": [], "Emission Strength": [], "Displacement Height": [], "Displacement Scale": [], "Displacement Midlevel": [], "Material Output": [], "IOR": [], "Normal": []}
    if (bakeType in requiredChannels):
        for channels in requiredChannels[bakeType]:
            if (channels in excludedChannels):
                excludedChannels.pop(channels)
    firstBakedImage: Image = None
    firstBakedImageSelected: Image = None
    previouseState = None

    shoulBake = (bpy.context.scene.BakeRegardless and imageObj.enabled) or (
        bakeType in bpy.context.scene.allwaysRequireBaking) or selected != None
    matLen = mesh.data.materials.__len__()
    for matSlot in range(matLen):
        mats = mesh.data.materials[matSlot]
        materialOutput = GetInputNode(mats, "OUTPUT_MATERIAL", bakeType)
        ImageBakeData[mats] = []
        selectedToActiveDate[mats] = []
        defaultData[mats] = []
        if (selected != None):
            exclusionMat = selected.data.materials[matSlot]
            exclusionMaterialOutput = GetInputNode(
                exclusionMat, "OUTPUT_MATERIAL", bakeType)
        else:
            exclusionMat = mats
            exclusionMaterialOutput = materialOutput
        if (mats != None):

            BakeInputNodes = GetAllInputNode(
                mats, inputNodeType[bakeType], bakeType)

            if (BakeInputNodes[0] == False):

                continue  # here

            if (materialOutput == False):
                continue   # here
            if (len(BakeInputNodes) > 1):
                shoulBake = True
            for bakeInputNode in BakeInputNodes:

                bakeNodeToAdd = bakeInputNode[0]
                bakeMatToAdd = bakeInputNode[1]
                nodesToDelete[bakeMatToAdd] = []

                if (firstBakedImage == None):
                    if (bakeMatToAdd in allReadyHasImage):
                        ImageBakeData[mats].append(
                            [allReadyHasImage[bakeMatToAdd], bakeMatToAdd, bakeNodeToAdd, mesh])
                    else:
                        if matSlot in existingImages[bakeType]:
                            existingImage = existingImages[bakeType][matSlot]
                        else:
                            existingImage = None
                        firstBakedImage = addImageNode(
                            bakeMatToAdd, uv, mesh, useUdims, udimCount, mats, imageObj, existingImage)
                        allReadyHasImage[bakeMatToAdd] = firstBakedImage
                        ImageBakeData[mats].append([firstBakedImage,
                                                    bakeMatToAdd, bakeNodeToAdd, mesh])

                    if (selected and bpy.context.scene.BakeMultiple and len(bpy.context.scene.my_items) > 1):
                        if (bakeMatToAdd in allReadyHasSlectedImage):
                            selectedToActiveDate[mats].append([allReadyHasSlectedImage[bakeMatToAdd],
                                                               bakeMatToAdd, bakeNodeToAdd, mesh])
                        else:
                            firstBakedImageSelected = addImageNode(
                                bakeMatToAdd, uv, mesh, useUdims, udimCount, mats, imageObj)
                            selectedToActiveDate[mats].append([firstBakedImageSelected,
                                                               bakeMatToAdd, bakeNodeToAdd, mesh])
                            allReadyHasSlectedImage[bakeMatToAdd] = firstBakedImageSelected
                            nodesToDelete[bakeMatToAdd].append(
                                firstBakedImageSelected)

                elif (bpy.context.scene.BakeMulitpleSlots):
                    if (bakeMatToAdd in allReadyHasImage):
                        ImageBakeData[mats].append([allReadyHasImage[bakeMatToAdd],
                                                    bakeMatToAdd, bakeNodeToAdd, mesh])
                    else:
                        AddRestOfImageNode(firstBakedImage,
                                           bakeMatToAdd)
                        ImageBakeData[mats].append([firstBakedImage,
                                                    bakeMatToAdd, bakeNodeToAdd, mesh])
                        allReadyHasImage[bakeMatToAdd] = firstBakedImage

                    if (firstBakedImageSelected and bpy.context.scene.BakeMultiple and len(bpy.context.scene.my_items) > 1):
                        if (bakeMatToAdd in allReadyHasSlectedImage):
                            selectedToActiveDate[mats].append([allReadyHasSlectedImage[bakeMatToAdd],
                                                               bakeMatToAdd, bakeNodeToAdd, mesh])
                        else:
                            AddRestOfImageNode(firstBakedImageSelected,
                                               bakeMatToAdd)
                            selectedToActiveDate[mats].append([firstBakedImageSelected,
                                                               bakeMatToAdd, bakeNodeToAdd, mesh])
                            allReadyHasSlectedImage[bakeMatToAdd] = firstBakedImageSelected
                            nodesToDelete[bakeMatToAdd].append(
                                firstBakedImageSelected)

                else:
                    if (bakeMatToAdd in allReadyHasImage):
                        ImageBakeData[mats].append([allReadyHasImage[bakeMatToAdd],
                                                    bakeMatToAdd, bakeNodeToAdd, mesh])
                    else:
                        if matSlot in existingImages[bakeType]:
                            existingImage = existingImages[bakeType][matSlot]
                        else:
                            existingImage = None
                        newBakedImage = addImageNode(
                            bakeMatToAdd, uv, mesh, useUdims, udimCount, mats, imageObj, existingImage)
                        allReadyHasImage[bakeMatToAdd] = newBakedImage
                        ImageBakeData[mats].append([newBakedImage,
                                                    bakeMatToAdd, bakeNodeToAdd, mesh])

                    if (selected and bpy.context.scene.BakeMultiple and len(bpy.context.scene.my_items) > 1):
                        if (bakeMatToAdd in allReadyHasSlectedImage):
                            selectedToActiveDate[mats].append([allReadyHasSlectedImage[bakeMatToAdd],
                                                               bakeMatToAdd, bakeNodeToAdd, mesh])
                        else:
                            newBakedImageSelected = addImageNode(
                                bakeMatToAdd, uv, mesh, useUdims, udimCount, mats, imageObj)
                            allReadyHasSlectedImage[bakeMatToAdd] = newBakedImageSelected
                            selectedToActiveDate[mats].append([newBakedImageSelected,
                                                               bakeMatToAdd, bakeNodeToAdd, mesh])

                            nodesToDelete[bakeMatToAdd].append(
                                newBakedImageSelected)

                if (shoulBake == False):

                    currentState = PreBakeTypeCheck(
                        bakeNodeToAdd.inputs[inputNodeName[bakeType]])
                    if (currentState[0] == 0):
                        continue
                    if (currentState[0] == 1):
                        shoulBake = True
                    if (shoulBake == False):
                        if (previouseState == None):
                            previouseState = currentState
                        else:
                            if (((previouseState[0] == 3) and (currentState[0] == 3)) and ((previouseState[1] == currentState[1]))):
                                shoulBake = False
                            elif (((previouseState[0] == 2) and (currentState[0] == 2)) and ((previouseState[1].image == currentState[1].image))):
                                shoulBake = False
                            else:
                                shoulBake = True

                        if (shoulBake == False):
                            defaultData[mats].append([previouseState[1],
                                                      bakeMatToAdd, bakeNodeToAdd, mesh])

        if (not shoulBake and not imageObj.enabled):
            return None
        if (selected != None):
            BakeInputNodesToUse = GetAllInputNode(
                exclusionMat, inputNodeType[bakeType], bakeType)
        else:
            BakeInputNodesToUse = BakeInputNodes
        for BakeInputNode in BakeInputNodesToUse:
            bakeMat: Material = BakeInputNode[1]
            if (bakeMat not in nodesToDelete):
                nodesToDelete[bakeMat] = []

            if ((bakeType in bpy.context.scene.requiresMaterialOutPutConnection)):

                requireNodeInfo = bpy.context.scene.requireAdditionalNode
                if (bakeType in requireNodeInfo):
                    connectToOutNode = GetNodeSocketFromRequire(
                        bakeMat, requireNodeInfo[bakeType])
                    nodesToDelete[bakeMat].append(connectToOutNode.node)
                    newSocket = GetNeedColorRamp(
                        bakeMat, bakeType, connectToOutNode)
                    if (newSocket != False):
                        connectToOutNode = newSocket
                        nodesToDelete[bakeMat].append(newSocket.node)
                else:
                    connectToOutNode: Node = GetInputValue(
                        bakeType, BakeInputNode)
                for input in exclusionMaterialOutput[0].inputs:
                    valueExcluded = BreakLink(
                        exclusionMaterialOutput[0], exclusionMaterialOutput[1], input.name)
                    if (valueExcluded):
                        excludedChannels["Material Output"].append(
                            ["ShaderNodeOutputMaterial", valueExcluded, exclusionMaterialOutput[1], input.name])
                exclusionMaterialOutput[1].node_tree.nodes.remove(
                    exclusionMaterialOutput[0])
                materialOutputNew = BakeInputNode[1].node_tree.nodes.new(
                    type="ShaderNodeOutputMaterial")
                CreatLink(BakeInputNode[1], materialOutputNew,
                          connectToOutNode, "Surface")
                nodesToDelete[bakeMat].append(materialOutputNew)
                break
            elif (bakeType in bpy.context.scene.requiresConnection or bakeType in bpy.context.scene.requiresDefaultValue):
                value = BakeInputNode[2]
                emissionNode: Node = bakeMat.node_tree.nodes.new(
                    type="ShaderNodeEmission")
                defaultValue = None
                connecton = None
                if (bakeType in bpy.context.scene.requiresConnection):
                    connecton = bpy.context.scene.requiresConnection[bakeType]

                if (bakeType in bpy.context.scene.requiresDefaultValue):
                    defaultValue = bpy.context.scene.requiresDefaultValue[bakeType]
                if (BakeInputNode[0].bl_idname in bpy.context.scene.ShaderNodes):
                    nodeTocheck = BakeInputNode[0]
                else:
                    nodeTocheck = BakeInputNode[0].outputs[0].links[0].to_node
                inputSocket: NodeSocket = nodeTocheck.outputs[0].links[0].to_socket
                fromSocket: NodeSocket = nodeTocheck.outputs[0]
                excludedNode: Node = nodeTocheck.outputs[0].links[0].to_node

                nodesToDelete[bakeMat].append(emissionNode)
                if (defaultValue):
                    for input in defaultValue:
                        emissionNode.inputs[input] = defaultValue[input]
                if (connecton):
                    CreatLink(bakeMat, emissionNode, value, connecton)
                excludedChannels[inputSocket.name] = []
                excludedChannels[inputSocket.name].append(
                    [excludedNode, fromSocket, bakeMat, inputSocket.name])
                bakeMat.node_tree.links.new(inputSocket,
                                            emissionNode.outputs[0])

            else:
                for excludedChannel in excludedChannels:
                    baseBakeInfo = bpy.context.scene.baseNode
                    if ((excludedChannel == "Material Output") or (bakeType not in bpy.context.scene.alwaysExcludedChannels and excludedChannel == bakeType)):
                        excludedInputNode = False
                    elif (inputNodeType[excludedChannel] == inputNodeType[bakeType]):
                        excludedInputNode = BakeInputNode
                    elif ((BakeInputNode[0].type in baseBakeInfo) and (baseBakeInfo[BakeInputNode[0].type]["Give"] == inputNodeType[excludedChannel])):
                        excludedInputNode = [
                            BakeInputNode[0].outputs[baseBakeInfo[BakeInputNode[0].type]["Output"]].links[0].to_node, BakeInputNode[1]]
                    else:
                        excludedInputNode = False
                    if (excludedChannel in bpy.context.scene.propertyDependentInput):
                        dependentPropertyInfo = bpy.context.scene.propertyDependentInput[
                            excludedChannel]

                        if ((excludedInputNode[0].type != dependentPropertyInfo["NodeType"]) or (getattr(excludedInputNode[0], dependentPropertyInfo["Property"]) not in dependentPropertyInfo["PropertyAccept"])):
                            excludedInputNode = False
                    if (excludedInputNode != False):

                        inputName = inputNodeName[excludedChannel]
                        valueExcludedChannel = BreakLink(
                            excludedInputNode[0], excludedInputNode[1], inputName)
                        if (valueExcludedChannel != None):
                            excludedChannels[excludedChannel].append([
                                excludedInputNode[0], valueExcludedChannel, excludedInputNode[1], inputName])
    if (selected != None):
        selected.select_set(True)
    mesh.select_set(True)

    bpy.context.view_layer.objects.active = mesh
    if (bpy.context.scene.ShadeSmooth):
        bpy.ops.object.shade_smooth()
    if (shoulBake):
        return [True, ImageBakeData, excludedChannels, nodesToDelete, selectedToActiveDate]
    for mats in ImageBakeData:
        nodeMat: Material = ImageBakeData[mats]
        for items in nodeMat:
            node: ShaderNodeTexImage = items[0]
            nodesToDelete[nodeMat].append(node)

    return [False, defaultData, excludedChannels, nodesToDelete]


def GetInputValue(BakeType: str, BakeInputNode: Node):
    NodeSocketValue: NodeSocket = BakeInputNode[0].inputs[bpy.context.scene.inputNodeNames[
        BakeType]]
    valueToCheck = NodeSocketValue.default_value
    if (NodeSocketValue.is_linked):
        Value = NodeSocketValue.links[0].from_socket
    elif ((type(valueToCheck) == float) or (type(valueToCheck) == int)):
        connectToOutNode: Node = BakeInputNode[1].node_tree.nodes.new(
            type="ShaderNodeValue")
        connectToOutNode.outputs[0].default_value = valueToCheck
        Value = connectToOutNode.outputs["Value"]
    else:
        connectToOutNode: Node = BakeInputNode[1].node_tree.nodes.new(
            type="ShaderNodeRGB")
        connectToOutNode.outputs[0].default_value[:
                                                  ] = valueToCheck[:]
        Value = connectToOutNode.outputs["Color"]
    return Value


def RestoreData(BakeType, excludedChannels, nodesToDelete):
    createdOne = {}
    for nodeMat in nodesToDelete:
        for node in nodesToDelete[nodeMat]:
            try:
                if (type(node) == ShaderNodeTexImage):
                    if (node.image):
                        bpy.data.images.remove(node.image)
                nodeMat.node_tree.nodes.remove(node)
            except:
                pass
    for excludedChannel in excludedChannels:
        for excludedPairs in excludedChannels[excludedChannel]:
            if ((excludedChannel != BakeType) or (BakeType in bpy.context.scene.alwaysExcludedChannels)):
                if (type(excludedPairs[0]) == str):
                    if (not any(True for mat in createdOne if (excludedPairs[2] == mat) and (excludedPairs[0] == createdOne[mat].bl_idname))):
                        excludedPairs[0] = excludedPairs[2].node_tree.nodes.new(
                            type=excludedPairs[0])
                        createdOne[excludedPairs[2]] = excludedPairs[0]
                    else:
                        excludedPairs[0] = createdOne[excludedPairs[2]]
                CreatLink(excludedPairs[2],
                          excludedPairs[0], excludedPairs[1], excludedPairs[3])


def copyNodeGroup(Mats: Material):
    nodeGroup = []
    for node in Mats.node_tree.nodes:
        if (type(node) == bpy.types.ShaderNodeGroup):
            group = node.node_tree
            copied = group.copy()
            node.node_tree = copied
            nodeGroup.append(node)
    for groups in nodeGroup:
        copyNodeGroup(groups)


def bakeNow():
    bakingSelection = bpy.context.scene.BakingSelection
    createdMaterial = {}
    tempData = {}
    uvPointRound = 4
    existingImages = {}
    maxMultipleBakeImageSlot = 0
    SelectedUv = None
    bakeObjectList = {}
    allMeshName = ""
    allMatName = ""

    uvFullCheck = CombineUvCheck(uvPointRound)
    useUv = uvFullCheck[2]
    useUdims = uvFullCheck[0]
    uvTiles = uvFullCheck[1]
    uvList = CreateUv(useUv)

    for obj in bpy.context.scene.my_items:
        for bakeObj in bpy.context.scene.bakingList:
            if ((bakeObj.enabled) or (bpy.context.scene.BakeMulitpleSlots and ((bakeObj.name not in bpy.context.scene.miscBake) and (bakeObj.name not in bpy.context.scene.notRequireBakingWhenBakingAll)) and ((bpy.context.scene.ApplyMaterial or bpy.context.scene.ApplyToCopiedAndHideOriginal)))):
                if (bakeObj not in bakeObjectList):
                    bakeObjectList[bakeObj] = []
                bakeObjectList[bakeObj].append(obj)
    if (bpy.context.scene.BakeMultiple or bpy.context.scene.BakeMulitpleSlots):
        if (bpy.context.scene.BakeMulitpleSlots):
            maxMultipleBakeImageSlot = 1
        else:
            for obj in bpy.context.scene.my_items:
                mesh: Object = obj.mesh
                allMeshName += "_"+mesh.name
                if ((len(mesh.data.materials) > maxMultipleBakeImageSlot)):
                    maxMultipleBakeImageSlot = len(mesh.data.materials)
                for mats in mesh.data.materials:
                    allMatName += "_"+mats.name

    for bakeObj in bakeObjectList:
        bakeType = bakeObj.name
        dataToRemoveRestore = []
        multiResModifiers = {}
        for MeshObj in bakeObjectList[bakeObj]:
            mesh = MeshObj.mesh
            if (bakeType not in existingImages):
                existingImages[bakeType] = {}
            selectCageInfo = [MeshObj.selected, MeshObj.cage]
            selectCageLocation = {}
            selectCageRotation = {}
            selectedObject = MeshObj.selected
            cageObject = MeshObj.cage
            for objectsSelectCage in selectCageInfo:
                if (objectsSelectCage):
                    selectCageLocation[objectsSelectCage] = objectsSelectCage.location[:]
                    selectCageRotation[objectsSelectCage] = objectsSelectCage.rotation_euler[:]
            needMultiRes = bpy.context.scene.alwaysRequireMultires
            if (bakeType in needMultiRes):
                for modifiers in mesh.modifiers:
                    if (modifiers.type == "MULTIRES"):
                        multiResModifiers[modifiers] = modifiers.levels
                if (len(multiResModifiers) == 0):
                    continue
            bpy.ops.object.select_all(action="DESELECT")
            if (bpy.context.scene.BakeMultiple):
                tilesToUse = list(
                    set(item for sublist in uvTiles.values() for item in sublist))
                needUdims = any(list(useUdims.values()))
            else:
                tilesToUse = uvTiles[mesh]
                needUdims = useUdims[mesh]
            SelectedUv = uvList[mesh]
            if (len(existingImages[bakeType]) == 0):
                for i in range(maxMultipleBakeImageSlot):
                    existingImages[bakeType][i] = GetNewImage(
                        allMatName, needUdims, tilesToUse, allMeshName, bakeObj)
            SelectedUv = uvList[mesh]
            BakedMap = bakeMap(SelectedUv, mesh, bakeType,
                               needUdims, tilesToUse, bakeObj, selectedObject, existingImages)

            if (type(BakedMap) == str or BakedMap == None):
                continue  # here too
            for mats in BakedMap[1]:
                if (mats not in createdMaterial):
                    createdMaterial[mats] = {}
                if (bakeType not in createdMaterial[mats]):
                    createdMaterial[mats][bakeType] = []
                for items in BakedMap[1][mats]:
                    createdMaterial[mats][bakeType].append([
                        items[0], items[1], items[2], mesh, bakeObj])
            if (selectedObject != None):
                for mats in BakedMap[4]:
                    if (mats not in tempData):
                        tempData[mats] = {}
                        tempData[mats][bakeType] = []
                    for items in BakedMap[4][mats]:
                        tempData[mats][bakeType].append([
                            items[0], items[1], items[2], mesh, bakeObj])
            if (BakedMap[0]):
                for objectsSelectCage in selectCageInfo:
                    if (objectsSelectCage):
                        objectsSelectCage.location = mesh.location
                        objectsSelectCage.rotation_euler = mesh.rotation_euler
                bpy.context.scene.render.bake.use_selected_to_active = selectedObject != None
                bpy.context.scene.render.bake.use_cage = cageObject != None
                if (bpy.context.scene.render.bake.use_cage):
                    bpy.context.scene.render.bake.cage_object = cageObject
                if ((bpy.context.scene.BakeMultiple == False) or (selectedObject != None)):
                    BakeFinal(bakingSelection, bakeType,
                              multiResModifiers, needMultiRes)
                for objectsSelectCage in selectCageInfo:
                    if (objectsSelectCage):
                        objectsSelectCage.location = selectCageLocation[objectsSelectCage]
                        objectsSelectCage.rotation_euler = selectCageRotation[objectsSelectCage]
            dataToRemoveRestore.append(
                [bakeType, BakedMap[2], BakedMap[3]])

        if (bpy.context.scene.BakeMultiple):
            bpy.context.scene.render.bake.use_selected_to_active = False
            for obj in bpy.context.scene.my_items:
                meshSecond = obj.mesh
                meshSecond.select_set(True)
                bpy.context.view_layer.objects.active = mesh
            TempConnection(tempData)
            for mats in createdMaterial:
                for bakeType in createdMaterial[mats]:
                    for items in createdMaterial[mats][bakeType]:
                        if (type(items[0]) == ShaderNodeTexImage):
                            for node in createdMaterial[mats][bakeType][1].node_tree.nodes:
                                node.select = False
                            items[0].select = True
                            items[1].node_tree.nodes.active = items[0]
            BakeFinal(bakingSelection, bakeType,
                      multiResModifiers, needMultiRes)
        if (bakeType in needMultiRes):
            for multires in multiResModifiers:
                multires.levels = multiResModifiers[multires]
        for data in dataToRemoveRestore:
            RestoreData(data[0], data[1], data[2])

    AntiAlias(createdMaterial)
    return createdMaterial


def TempConnection(createdMaterial):
    tempMat = {}
    for mats in createdMaterial:
        tempMat[mats] = {}
        createNewMatsData(
            tempMat, createdMaterial, mats, None, False)
    ApplyMaterial(tempMat)


def BakeFinal(bakingSelection, bakeType, multiResModifiers, needMultiRes):
    if (bakeType in needMultiRes):
        for multires in multiResModifiers:
            multires.levels = 0
        bpy.context.scene.render.use_bake_multires = True
        bpy.context.scene.render.bake_type = bakingSelection[bakeType]
        bpy.ops.object.bake_image()
    elif (bakingSelection[bakeType] == "DIFFUSE"):
        bpy.ops.object.bake(type="DIFFUSE", pass_filter={"COLOR"})
    else:
        bpy.ops.object.bake(type=bakingSelection[bakeType])


def AntiAlias(createdMaterial):
    if (bpy.context.scene.AntialiasingScale != 1):
        for mats in createdMaterial:
            for bakeType in createdMaterial[mats]:
                for items in createdMaterial[mats][bakeType]:
                    valueNode = items[0]
                    image = None
                    if (type(valueNode) == ShaderNodeTexImage):
                        image = valueNode.image
                        imagePath = None
                        isUdim = False
                    if (image):
                        savedDate = saveImage(
                            image, mats, True, bakeType, items[3])

                        if (savedDate[2]):
                            isUdim = True
                            for tile in savedDate[1]:
                                imageNew = imageio.v3.imread(
                                    savedDate[1][tile])
                                resizedImage = cv2.resize(imageNew,
                                                          (bpy.context.scene.width, bpy.context.scene.height), interpolation=cv2.INTER_LANCZOS4)
                                imageio.v3.imwrite(
                                    savedDate[1][tile], resizedImage)
                                imagePath = savedDate[1][tile]
                        else:
                            imageNew = imageio.v3.imread(savedDate[1])
                            resizedImage = cv2.resize(imageNew,
                                                      (bpy.context.scene.width, bpy.context.scene.height), interpolation=cv2.INTER_LANCZOS4)
                            imageio.v3.imwrite(savedDate[1], resizedImage)
                            imagePath = savedDate[1]
                        bpy.data.images.remove(image)
                        loadedImage = bpy.data.images.load(
                            imagePath, check_existing=True)
                        loadedImage.colorspace_settings.name = items[4].space

                        if (isUdim):
                            loadedImage.source = "TILED"
                        valueNode.image = loadedImage
                        loadedImage.name = Path(imagePath).stem


def RestoreSetting(currentEngine, currentDevice, previousState, modePrev, extrusion, rayDistance, margin):
    bpy.context.scene.render.bake.cage_extrusion = extrusion
    bpy.context.scene.render.bake.margin = margin
    bpy.context.scene.render.bake.max_ray_distance = rayDistance
    bpy.context.scene.render.engine = currentEngine
    bpy.context.scene.cycles.device = currentDevice
    bpy.context.area.ui_type = previousState
    try:
        bpy.ops.object.mode_set(mode=modePrev)
    except:
        pass


def BakingSetUp():
    for obj in bpy.context.scene.my_items:
        mesh = obj.mesh
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = mesh
        bpy.ops.object.material_slot_remove_unused()
        bpy.ops.object.select_all(action="DESELECT")
    mode = bpy.context.mode
    areaTypeOld = bpy.context.area.ui_type
    bpy.context.area.ui_type = "VIEW_3D"
    currentEngine = bpy.context.scene.render.engine
    currentDevice = bpy.context.scene.cycles.device
    extrusion = bpy.context.scene.render.bake.cage_extrusion
    currentRaydistance = bpy.context.scene.render.bake.max_ray_distance
    currentMargin = bpy.context.scene.render.bake.margin
    bpy.context.scene.render.bake.max_ray_distance = bpy.context.scene.rayDistance
    bpy.context.scene.cycles.device = bpy.context.scene.Device
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.render.bake.cage_extrusion = bpy.context.scene.extrusion
    bpy.context.scene.render.bake.margin = bpy.context.scene.margin
    try:
        bpy.ops.object.mode_set(mode="OBJECT")
    except:
        pass
    return currentEngine, currentDevice, areaTypeOld, mode, extrusion, currentRaydistance, currentMargin


def saveImage(image: Image, mats: Material, isPreBaked: bool, BakeType: str, mesh):
    imageFile = GetFilePath(mats, image.source == "TILED",
                            isPreBaked, BakeType, ".<UDIM>.", mesh, image.name)

    image.save(filepath=imageFile)
    if (image.source == "TILED"):
        imagesPath = {}
        for tile in image.tiles:
            imagesPath[tile.number] = GetFilePath(
                mats, True, isPreBaked, BakeType, f".{tile.number}.", mesh, image.name)
        return [image, imagesPath, True]
    else:
        return [image, imageFile, False]


def GetImage(image: Image, mats: Material, isPreBaked: bool, BakeType: str, mesh):
    imageFile = GetFilePath(mats, image.source == "TILED",
                            isPreBaked, BakeType, ".<UDIM>.", mesh, image.name)

    if (image.source == "TILED"):
        imagesPath = {}
        for tile in image.tiles:
            imagesPath[tile.number] = GetFilePath(
                mats, True, isPreBaked, BakeType, f".{tile.number}.", mesh, image.name)
        return [image, imagesPath, True]
    else:
        return [image, imageFile, False]


def GetFilePath(mats: Material, isUdim: bool, isPreBaked: bool, BakeType: str, tileInfo, mesh: Object, fileName):
    subFolder: str = bpy.context.scene.FolderTree
    if (subFolder[0] != "\\"):
        subFolder = "\\"+subFolder
    subFolder = subFolder.replace("[mat]", mats.name)
    subFolder = subFolder.replace("[bakeType]", BakeType)
    subFolder = subFolder.replace("[Object]", mesh.name)
    filePath = bpy.context.scene.basePath + \
        bpy.context.scene.BakedImagesFilePath
    preBakedFilePath = bpy.context.scene.basePath + \
        bpy.context.scene.PreBakedFilePath

    if (isPreBaked):
        pathToUseDir = preBakedFilePath + subFolder
    else:
        pathToUseDir = filePath + subFolder

    extension = bpy.context.scene.FileFormat

    if (isUdim):
        imageFile = f"{pathToUseDir}/" + \
            f"{fileName}.{tileInfo}.{extension}"
    else:
        imageFile = f"{pathToUseDir}/" + \
            f"{fileName}.{extension}"
    return imageFile


def GetImageName(mats, mesh, imageObj):
    fileName: str = imageObj.naming
    fileName = fileName.replace("[mat]", mats)
    fileName = fileName.replace("[Object]", mesh)
    fileName = fileName.replace("[Num]", "")
    origianlName = fileName
    num = 1

    while (bpy.data.images.get(fileName, None) != None):
        if ("[Num]" in origianlName):
            fileName = origianlName.replace("[Num]", f"{num}")
        else:
            fileName = f"{origianlName}{num}"
        num += 1
    return fileName


def checkIfRequireAll(Mesh: Object):
    inputNodes = bpy.context.scene.inputNodeNames

    for BakeType in bpy.context.scene.BakeTypes:
        if (bpy.context.scene.inputNode[BakeType] == "BSDF_PRINCIPLED"):
            for mats in Mesh.data.materials:
                result = GetAllInputNode(
                    mats, "BSDF_PRINCIPLED", inputNodes[BakeType])
                if (result != False):
                    if (len(result) > 1):
                        if (result[0] != False):
                            return True
    return False


def GetColor(udimCount: int, channel, useUdim: bool):
    multiplier = 255 if not bpy.context.scene.FileFormat in bpy.context.scene.OneInvert else 1
    if (type(channel) == list):
        if (useUdim):
            if (udimCount in channel[1]):

                channelImage = imageio.v3.imread(channel[1][udimCount])
            else:
                channelImage = numpy.zeros(
                    (bpy.context.scene.width, bpy.context.scene.height), dtype=numpy.float64)
        else:
            channelImage = imageio.v3.imread(channel[1])

    if ((type(channel) == float) or (type(channel) == int)):
        channelImage = numpy.full(
            (bpy.context.scene.width, bpy.context.scene.height), channel*multiplier, dtype=numpy.float64)
    if (channelImage.ndim == 3):
        channelImage = channelImage[:, :, 0]
    return channelImage


def bake():
    newCreatedMats = {}
    createdJson = {}
    previousMatDate = {}
    originalObjects = bpy.context.selected_objects
    if (bpy.context.scene.ApplyToCopiedAndHideOriginal == True):
        for obs in bpy.context.scene.my_items:
            obs.mesh.select_set(True)
            bpy.context.view_layer.objects.active = obs
        bpy.ops.object.duplicate()

    currentEngine, currentDevice, previousState, mode, extrusion, rayDistance, margin = BakingSetUp(
    )
    if (len(bpy.context.scene.my_items) == 0):
        return "No valid object selected or Object with materials"  # here
    else:
        for obj in bpy.context.scene.my_items:
            filteredMesh = obj.mesh
            for matsNum in range(filteredMesh.data.materials.__len__()):
                if (filteredMesh not in previousMatDate):
                    previousMatDate[filteredMesh] = []
                previousMatDate[filteredMesh].append([
                    filteredMesh.data.materials[matsNum], matsNum])
                if (bpy.context.scene.CopyMaterial):
                    returedMat = CopySetMaterial(filteredMesh, matsNum)
                else:
                    returedMat = filteredMesh.data.materials[matsNum]
                if (bpy.context.scene.CopyNodeGroup):
                    copyNodeGroup(returedMat)
    bakeDate = bakeNow()
    for mats in bakeDate:
        newCreatedMats[mats] = {}
        createdJson[mats.name] = {}
        Fliping(bakeDate, bakeDate[mats], mats)
        PackTexture(newCreatedMats, bakeDate, mats, createdJson)
        createNewMatsData(newCreatedMats, bakeDate, mats, createdJson, True)
    for mats in newCreatedMats:
        for finalBakeType in newCreatedMats[mats]:
            try:
                outputNode = newCreatedMats[mats][finalBakeType][0].node
                if (outputNode.type == "TEX_IMAGE"):
                    saveImage(outputNode.image, mats,
                              False, finalBakeType, newCreatedMats[mats][finalBakeType][3])
            except:
                pass
    if (bpy.context.scene.ApplyMaterial or bpy.context.scene.ApplyToCopiedAndHideOriginal):
        ApplyMaterial(newCreatedMats)
    os.makedirs(bpy.context.scene.JsonExport, exist_ok=True)
    with open(f"{bpy.context.scene.JsonExport}mapping.json", "w") as jsonFile:
        try:
            data = json.load(jsonFile)
            data.update(createdJson)
            json.dump(data, jsonFile)
        except:
            json.dump(createdJson, jsonFile)
    if (bpy.context.scene.BakeMulitpleSlots and (bpy.context.scene.ApplyMaterial or bpy.context.scene.ApplyToCopiedAndHideOriginal)):
        for obj in bpy.context.scene.my_items:
            mesh = obj.mesh
            if (len(mesh.data.materials) > 1):
                mesh.data.materials[0].name = f"CombineMat{mesh.name}"
                for slotsNum in range(1, len(mesh.data.materials)):
                    bpy.data.materials.remove(mesh.data.materials[slotsNum])
                    bpy.context.object.active_material_index = slotsNum
                    bpy.ops.object.material_slot_remove()

    if ((bpy.context.scene.ApplyMaterial == False) and (bpy.context.scene.ApplyToCopiedAndHideOriginal == False)):
        for filteredMesh in previousMatDate:
            for data in previousMatDate[filteredMesh]:
                filteredMesh.data.materials[data[1]
                                            ] = data[0]
    if (bpy.context.scene.ApplyToCopiedAndHideOriginal):
        for objs in originalObjects:
            objs.hide_render = True
            objs.hide_viewport = True

    RestoreSetting(currentEngine, currentDevice,
                   previousState, mode, extrusion, rayDistance, margin)


def ApplyMaterial(newCreatedMats):
    for mats in newCreatedMats:
        GetBlendings(newCreatedMats, mats)
        for finalBakeType in newCreatedMats[mats]:
            for items in newCreatedMats[mats][finalBakeType]:
                matsTree: Material = items[1]
                FlipSocket(items, finalBakeType, matsTree)
                CheckAddionStep(items, finalBakeType, matsTree)
                outputNode: Node = items[0]
                socketName = bpy.context.scene.inputNodeNames[finalBakeType]
                inputNode: Node = items[2]
                CreatLink(matsTree, inputNode,
                          outputNode, socketName)

                afterBake = bpy.context.scene.RequireAfterProcess
                if (finalBakeType in afterBake):
                    for afterInputs in afterBake[finalBakeType]:
                        CreatLink(mats, inputNode,
                                  afterBake[finalBakeType][afterInputs], afterInputs)


def CheckAddionStep(items, finalBakeType, matsTree):
    requireAdditonSteps = bpy.context.scene.multiResSetup
    oldValue: NodeSocket = items[0]
    goForward = True
    try:
        tempNode = oldValue.node
        if (tempNode.bl_idname == requireAdditonSteps[finalBakeType]["Node"]):
            goForward = False
    except:
        pass
    if (finalBakeType in requireAdditonSteps and goForward):
        value = None
        if (((type(oldValue) == float) or (type(oldValue) == int))):
            value = oldValue
        else:
            value = requireAdditonSteps[finalBakeType]["InputOutputName"]

        try:
            node = oldValue.node
            if (node.inputs[requireAdditonSteps[finalBakeType]["OriginInput"]].is_linked):
                newNode = node.inputs[requireAdditonSteps[finalBakeType]
                                      ["OriginInput"]].links[0].from_node
        except:
            newNode = matsTree.node_tree.nodes.new(
                type=requireAdditonSteps[finalBakeType]["Node"])
        CreatLink(matsTree, newNode,
                  oldValue, value)
        items[0] = newNode.outputs[requireAdditonSteps[finalBakeType]["Output"]]


def FlipSocket(items, finalBakeType, matsTree):
    if ((finalBakeType == "Normal" and bpy.context.scene.FlipnormalY) or (finalBakeType == "Roughness" and bpy.context.scene.ConvertRoughnessToSmoothness)):
        flippingInfo = bpy.context.scene.flippingInfo
        isAll = all(list(flippingInfo[finalBakeType].values()))
        if (isAll):
            invertNode = matsTree.node_tree.nodes.new(type="ShaderNodeInvert")
            CreatLink(matsTree, invertNode, items[0],
                      "Color")
            items[0] = invertNode.outputs["Color"]
        else:
            seperateColorNode = matsTree.node_tree.nodes.new(
                type="ShaderNodeSeparateColor")
            combineColorNode = matsTree.node_tree.nodes.new(
                type="ShaderNodeCombineColor")

            CreatLink(matsTree, seperateColorNode, items[0],
                      "Color")
            for channel in flippingInfo[finalBakeType]:
                if (channel != "Alpha"):
                    if (flippingInfo[finalBakeType][channel]):
                        invertNode = matsTree.node_tree.nodes.new(
                            type="ShaderNodeInvert")
                        CreatLink(matsTree,
                                  invertNode, seperateColorNode.outputs[channel], "Color")
                        CreatLink(matsTree, combineColorNode,
                                  invertNode.outputs["Color"], channel)
                    else:
                        CreatLink(matsTree, combineColorNode,
                                  seperateColorNode.outputs[channel], channel)
            items[0] = combineColorNode.outputs["Color"]


def Fliping(bakeDate, bakeTypes, mats):
    if (bpy.context.scene.FlipnormalY or bpy.context.scene.ConvertRoughnessToSmoothness):
        for bakeType in bakeTypes:
            if (bpy.context.scene.FlipnormalY and bakeType == "Normal"):
                Invert(bakeDate, mats, bakeType)
            if (bpy.context.scene.ConvertRoughnessToSmoothness and bakeType == "Roughness"):
                Invert(bakeDate, mats, bakeType)


def Invert(bakeDate, mats, bakeType):
    value = bakeDate[mats][bakeType][0]
    if ((type(value) == int) or (type(value) == float)):
        bakeDate[mats][bakeType][0] = 1-value
    else:
        imagePath = None
        currentImage: Image = bakeDate[mats][bakeType][0].image
        savedInfo = saveImage(
            currentImage, mats, True, bakeType, bakeDate[mats][bakeType][3])
        bpy.data.images.remove(currentImage)
        name = GetImageName(
            mats.name, bakeDate[mats][bakeType][3].name, bakeDate[mats][bakeType][4])
        if (savedInfo[2]):
            for tiles in savedInfo[1]:
                imageToInvert = imageio.v3.imread(
                    savedInfo[1][tiles])
                ndim = imageToInvert.ndim
                valueToExclue = 1 if Path(
                    savedInfo[1][tiles]).suffix in bpy.context.scene.OneInvert else 255
                flippingInfo = bpy.context.scene.flippingInfo[bakeType]

                if (ndim == 2):
                    imageToInvert = valueToExclue-imageToInvert

                else:
                    for i in range(ndim):
                        if (flippingInfo[i]):
                            imageToInvert[:, :, i] = valueToExclue - \
                                imageToInvert[:, :, i]
                savedLocation = GetFilePath(
                    mats, True, True, bakeType, tiles, bakeDate[mats][bakeType][3], name)
                imageio.v3.imwrite(savedLocation, imageToInvert)
                imagePath = savedLocation
        else:
            imageToInvert = imageio.v3.imread(
                savedInfo[1])
            ndim = imageToInvert.ndim
            valueToExclue = 1 if Path(
                savedInfo[1]).suffix in bpy.context.scene.OneInvert else 255
            flippingInfo = bpy.context.scene.flippingInfo[bakeType]

            if (ndim == 2):
                imageToInvert = valueToExclue-imageToInvert

            else:
                for i in range(ndim):
                    if (flippingInfo[i]):
                        imageToInvert[:, :, i] = valueToExclue - \
                            imageToInvert[:, :, i]
            savedLocation = GetFilePath(
                mats, False, True, bakeType, None, bakeDate[mats][bakeType][3], name)
            imageio.v3.imwrite(savedLocation, imageToInvert)
            imagePath = savedLocation

        image: Image = bpy.data.images.load(
            imagePath, check_existing=True)
        image.name = Path(imagePath).stem
        if (savedInfo[2]):
            image.source = "TILED"
        image.colorspace_settings.name = bakeDate[mats][bakeType][4].space
        bakeDate[mats][bakeType][0].image = image


def GetBlendings(newCreatedMats, mats):
    blendingsDate = bpy.context.scene.Blending
    alreadyHasValue = {}
    alreadyAdded = {}
    for blendingBakesList in blendingsDate:
        if (blendingsDate[blendingBakesList]["requirements"]):
            hasRequiredBakeType = True
            connectionObj = blendingsDate[blendingBakesList]["Connection"]
            availableOnes = blendingsDate[blendingBakesList]["UsuallyAvailable"]
            notAvailableBake = []
            firstAvailableOne = None
            for connection in connectionObj:
                if (connectionObj[connection] not in newCreatedMats[mats]):
                    hasRequiredBakeType = False
                    notAvailableBake.append(connectionObj[connection])
                elif ((firstAvailableOne == None) and (connectionObj[connection] not in availableOnes)):
                    firstAvailableOne = []
                    for items in newCreatedMats[mats][connectionObj[connection]]:
                        firstAvailableOne.append(items.copy())
            if ((firstAvailableOne != None) and (hasRequiredBakeType == False)):
                for bakes in notAvailableBake:
                    newCreatedMats[mats][bakes] = firstAvailableOne
                    for index, items in enumerate(newCreatedMats[mats][bakes]):
                        if (items[1] in alreadyHasValue):
                            newCreatedMats[mats][bakes][index] = alreadyHasValue[items[1]]
                        else:
                            value = GetInputValue(
                                bakes, [items[2], items[1]])
                            newCreatedMats[mats][bakes][index] = value
                            alreadyHasValue[items[1]] = value
                    hasRequiredBakeType = True
            if (hasRequiredBakeType):
                connectNode = blendingsDate[blendingBakesList]["Node"]
                outputSocketName = blendingsDate[blendingBakesList]["OutPutSocket"]

                properties = blendingsDate[blendingBakesList]["Properties"]
                inputs = blendingsDate[blendingBakesList]["Inputs"]
                for items in newCreatedMats[mats]["Base Color"]:
                    if (items[1] in alreadyAdded):
                        items[0] = alreadyAdded[items[1]]
                    else:
                        createdNode: Node = items[1].node_tree.nodes.new(
                            type=connectNode)
                        for property in properties:
                            setattr(createdNode, property,
                                    properties[property])
                        for input in inputs:
                            CreatLink(items[1], createdNode,
                                      inputs[input], input)

                        for connection in connectionObj:
                            for newItems in newCreatedMats[mats][connectionObj[connection]]:
                                if (items[1] == newItems[1]):
                                    CreatLink(items[1], createdNode,
                                              newItems[0], connection)
                                    newItems[0] = createdNode.outputs[outputSocketName]
                                    alreadyAdded[items[1]] = newItems[0]
    for connection in connectionObj:
        if (connectionObj[connection] != "Base Color"):
            if (connectionObj[connection] in newCreatedMats[mats]):
                del newCreatedMats[mats][connectionObj[connection]]


def createNewMatsData(newCreatedMats, bakeDate, mats, createdJson, createJson):
    for bakedTextureType in bakeDate[mats]:
        for items in bakeDate[mats][bakedTextureType]:
            if (bakedTextureType not in newCreatedMats[mats]):
                newCreatedMats[mats][bakedTextureType] = []
            if (type(items[0]) == ShaderNodeTexImage):
                outPutToAdd = items[0].outputs["Color"]

            else:
                outPutToAdd = items[0]
            valueData = items[0]
            if (createJson):
                createdJson[mats.name][bakedTextureType] = {}
                if (type(valueData) == ShaderNodeTexImage):
                    value = GetImage(valueData.image, mats, False,
                                     bakedTextureType, items[3])
                    if (not value[2]):
                        valueToAdd = value[1]
                        createdJson[mats.name][bakedTextureType]["value"] = valueToAdd
                        createdJson[mats.name][bakedTextureType]["Channel"] = "FULL"
                        createdJson[mats.name][bakedTextureType]["Tiled"] = False
                        createdJson[mats.name][bakedTextureType]["Mesh"] = items[3].name
                    else:
                        createdJson[mats.name][bakedTextureType]["Tiled"] = True
                        createdJson[mats.name][bakedTextureType]["Channel"] = "FULL"
                        createdJson[mats.name][bakedTextureType]["value"] = {}
                        createdJson[mats.name][bakedTextureType]["Mesh"] = items[3].name
                        for tile in value[1]:
                            valueToAdd = value[1][tile]
                            createdJson[mats.name][bakedTextureType]["value"][tile] = valueToAdd
                else:
                    valueToAdd = valueData
                    createdJson[mats.name][bakedTextureType]["value"] = valueToAdd
                    createdJson[mats.name][bakedTextureType]["Channel"] = "FULL"
                    createdJson[mats.name][bakedTextureType]["Tiled"] = False
                    createdJson[mats.name][bakedTextureType]["Mesh"] = items[3].name
            newCreatedMats[mats][bakedTextureType].append([
                outPutToAdd, items[1], items[2], items[3]])


def PackTexture(newCreatedMats, bakeDate, mats, createdJson):

    for packedTexture in bpy.context.scene.my_Packed_Object:
        tiles = []
        redBakeTexture = packedTexture.Red
        greenBakeTexture = packedTexture.Green
        blueBakeTexture = packedTexture.Blue
        alphaBakeTexture = packedTexture.Alpha
        if (redBakeTexture == "None"):
            redBakeTexture = None
        if (greenBakeTexture == "None"):
            greenBakeTexture = None
        if (blueBakeTexture == "None"):
            blueBakeTexture = None
        if (alphaBakeTexture == "None"):
            alphaBakeTexture = None
        redChannel = GetChannel(mats, redBakeTexture,
                                bakeDate)
        greenChannel = GetChannel(
            mats, greenBakeTexture, bakeDate)
        blueChannel = GetChannel(
            mats, blueBakeTexture, bakeDate)
        alphaChannel = GetChannel(
            mats, alphaBakeTexture, bakeDate)
        useUdim = redChannel[1] or greenChannel[1] or blueChannel[1] or alphaChannel[1]
        needPacking = redChannel[2] or greenChannel[2] or blueChannel[2] or alphaChannel[2]
        ChannelList = {redBakeTexture: [redChannel[2], "Red"], greenBakeTexture: [
            greenChannel[2], "Green"], blueBakeTexture: [blueChannel[2], "Blue"], alphaBakeTexture: [alphaChannel[2], "Alpha"]}
        if (redChannel[2]):
            mesh = bakeDate[mats][redBakeTexture][0][3]
        elif (greenChannel[2]):
            mesh = bakeDate[mats][greenBakeTexture][0][3]
        elif (blueChannel[2]):
            mesh = bakeDate[mats][alphaBakeTexture][0][3]
        elif (alphaChannel[2]):
            mesh = bakeDate[mats][blueBakeTexture][0][3]
        else:
            continue
        tiles = list(
            set(blueChannel[3]+alphaChannel[3]+greenChannel[3]+redChannel[3]))
        if (needPacking):
            matColorSepNod = {}
            image = None
            if (useUdim):
                for tile in tiles:

                    redCurrentColor = GetColor(
                        tile, redChannel[0], redChannel[1])
                    greenCurrentColor = GetColor(
                        tile, greenChannel[0], greenChannel[1])
                    blueCurrentColor = GetColor(
                        tile, blueChannel[0], blueChannel[1])
                    alphaCurrentColor = GetColor(
                        tile, alphaChannel[0], alphaChannel[1])
                    savedFolder = createPackedImage(
                        alphaCurrentColor, alphaChannel[2], redCurrentColor, greenCurrentColor, blueCurrentColor, mats, True, f".{tile}.", mesh, packedTexture)
                    for channel in ChannelList:

                        if (ChannelList[channel][0]):
                            createdJson[mats.name][channel] = {}

                            for item in bakeDate[mats][channel]:
                                if (type(item[0]) != int and type(item[0]) != float and item[0].bl_idname == "ShaderNodeTexImage"):
                                    if (item[0].image):
                                        bpy.data.images.remove(item[0].image)
                                    bakeDate[mats][channel][1].node_tree.nodes.remove(
                                        item[0])
                                if (item[1] not in matColorSepNod):

                                    imageTexture: ShaderNodeTexImage = item[1].node_tree.nodes.new(
                                        type="ShaderNodeTexImage")
                                    seperateColor: ShaderNodeSeparateColor = item[1].node_tree.nodes.new(
                                        type="ShaderNodeSeparateColor")
                                    matColorSepNod[item[1]] = [
                                        imageTexture, seperateColor]
                                    CreatLink(item[1], seperateColor,
                                              imageTexture.outputs["Color"], "Color")

                                if (ChannelList[channel][1] == "Alpha"):
                                    outPutToAdd = matColorSepNod[item[1]
                                                                 ][0].outputs["Alpha"]
                                else:
                                    outPutToAdd = matColorSepNod[item[1]
                                                                 ][1].outputs[ChannelList[channel][1]]
                                if (channel not in newCreatedMats[mats]):
                                    newCreatedMats[mats][channel] = []
                                newCreatedMats[mats][channel].append([
                                    outPutToAdd, bakeDate[mats][channel][1], bakeDate[mats][channel][2], mesh])
                            createdJson[mats.name][channel]["Channel"] = ChannelList[channel][1]
                            createdJson[mats.name][channel]["Tiled"] = True
                            createdJson[mats.name][channel]["value"] = {}
                            createdJson[mats.name][channel]["value"][tile] = savedFolder
                            createdJson[mats.name][channel]["Mesh"] = mesh.name

            else:
                redCurrentColor = GetColor(
                    None, redChannel[0], redChannel[1])
                greenCurrentColor = GetColor(
                    None, greenChannel[0], greenChannel[1])
                blueCurrentColor = GetColor(
                    None, blueChannel[0], blueChannel[1])
                alphaCurrentColor = GetColor(
                    None, alphaChannel[0], alphaChannel[1])
                savedFolder = createPackedImage(alphaCurrentColor, alphaChannel[2],
                                                redCurrentColor, greenCurrentColor, blueCurrentColor, mats, False, None, mesh, packedTexture)

                for channel in ChannelList:
                    if (ChannelList[channel][0]):
                        createdJson[mats.name][channel] = {}
                        for items in bakeDate[mats][channel]:
                            if (type(items[0]) != int and type(items[0]) != float and items[0].bl_idname == "ShaderNodeTexImage"):
                                if (items[0].image):
                                    bpy.data.images.remove(items[0].image)
                                items[1].node_tree.nodes.remove(
                                    items[0])

                            if (items[1] not in matColorSepNod):
                                imageTexture: ShaderNodeTexImage = items[1].node_tree.nodes.new(
                                    type="ShaderNodeTexImage")
                                seperateColor: ShaderNodeSeparateColor = items[1].node_tree.nodes.new(
                                    type="ShaderNodeSeparateColor")
                                CreatLink(items[1], seperateColor,
                                          imageTexture.outputs["Color"], "Color")
                                matColorSepNod[items[1]] = [
                                    imageTexture, seperateColor]

                            if (ChannelList[channel][1] == "Alpha"):
                                outPutToAdd = matColorSepNod[items[1]
                                                             ][0].outputs["Alpha"]
                            else:
                                outPutToAdd = matColorSepNod[items[1]
                                                             ][1].outputs[ChannelList[channel][1]]
                            if (channel not in newCreatedMats[mats]):
                                newCreatedMats[mats][channel] = []
                            newCreatedMats[mats][channel].append(
                                [outPutToAdd, items[1], items[2], mesh])
                        createdJson[mats.name][channel]["Channel"] = ChannelList[channel][1]
                        createdJson[mats.name][channel]["Tiled"] = False
                        createdJson[mats.name][channel]["value"] = savedFolder
                        createdJson[mats.name][channel]["Mesh"] = mesh.name
            image = bpy.data.images.load(savedFolder, check_existing=True)
            if (useUdim):
                image.source = "TILED"
            image.colorspace_settings.name = packedTexture.space
            image.name = Path(savedFolder).stem
            imageTexture.image = image


def createPackedImage(alphaCurrentColor, alphaExist, redCurrentColor, greenCurrentColor, blueCurrentColor,  mats, UseUdims, tile, mesh, imageObj):
    name = GetImageName(mats.name, mesh.name, imageObj)
    savedFile = GetFilePath(
        mats, UseUdims, False, imageObj.name, tile, mesh, name)
    if (alphaExist):
        packedImage = numpy.stack(
            (redCurrentColor, greenCurrentColor, blueCurrentColor, alphaCurrentColor), axis=-1).astype(numpy.uint8)
        os.makedirs(os.path.dirname(savedFile), exist_ok=True)
        imageio.v3.imwrite(savedFile, packedImage)

    else:

        packedImage = numpy.stack(
            (redCurrentColor, greenCurrentColor, blueCurrentColor), axis=-1).astype(numpy.uint8)
        os.makedirs(os.path.dirname(savedFile), exist_ok=True)
        imageio.v3.imwrite(savedFile, packedImage)
    return savedFile


def GetChannel(mats, bakeTexture, createdMaterial):
    useUdim = False
    needPacking = False
    tiles = []
    if (bakeTexture == None):
        channelData = 0
        needPacking = False
    else:
        if (bakeTexture in createdMaterial[mats]):
            channelData = createdMaterial[mats][bakeTexture][0][0]
            needPacking = True

            if (type(channelData) == ShaderNodeTexImage):
                channelData = saveImage(
                    channelData.image, mats, True, bakeTexture, createdMaterial[mats][bakeTexture][0][3])
                useUdim = channelData[2]
                if (useUdim):
                    tiles = list(channelData[1])
        else:
            channelData = 0
            needPacking = False
    return [channelData, useUdim, needPacking, tiles]


bake()
objectMats = bpy.context.object.data.materials[0].node_tree.nodes

testList = []
