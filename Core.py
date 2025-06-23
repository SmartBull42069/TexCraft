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





def GetNeedColorRamp(mats: Material, bakeType, outPutSocket: NodeSocket):
    if (bakeType in bpy.context.scene.bakeTypeColorRamp):
        node = mats.node_tree.nodes.new(type="ShaderNodeValToRGB")
        for position, positionValue in enumerate(bpy.context.scene.bakeTypeColorRamp[bakeType]["Positions"]):
            node.color_ramp.elements[position].position = positionValue
        CreatLink(mats, node, outPutSocket, "Fac")
        return [node.outputs["Color"],node]
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
    return [newNode.outputs[bakeTypeInformation["OutPutSocket"]],newNode]


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
        if (not useUv[mesh] or len(mesh.data.uv_layers)>=8):
            meshListWithUv[mesh]= mesh.data.uv_layers[obj.uv]
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
    
    mat: Material = mesh.material_slots[index].material.copy()
    mesh.material_slots[index].material = mat
    mat.name = GetMaterialName(mesh, mat)
    return mat

def GetMaterialName(mesh, mat):
    name = bpy.context.scene.CopiedMaterialName
    if (name != ""):
        name = name.replace("[mat]", mat.name)
        name = name.replace("[Object]", mesh.name)
        return name
    else:
        return mat.name


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
    if(bpy.context.scene.FileFormat=="jpg"):
        useAlpha=False
    else:
        useAlpha=True
    NewImg: Image = bpy.data.images.new(
        fileName, round(bpy.context.scene.height*bpy.context.scene.AntialiasingScale), round(bpy.context.scene.width*bpy.context.scene.AntialiasingScale), float_buffer=imageObj.float, alpha=useAlpha, tiled=useUdims)
    
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
    imageTexture.image=bakesImage
    for node in mats.node_tree.nodes:
        node.select = False
    imageTexture.select = True
    mats.node_tree.nodes.active = imageTexture
    return imageTexture

def getUnpackedMateria(mats:Material,num,obj:Object,revertMaterials):
    home_area = bpy.context.area.type
    home_ui = bpy.context.area.ui_type
    copiedMat=mats.copy()
    obj.material_slots[num].material = copiedMat
    spaces = [copiedMat]
    numberOfSpaces=0
    copiedMat.name=f"unpackedMat {mats.name} {obj.name} "
    for space in spaces:
        for node in space.node_tree.nodes:
            if node.type == 'GROUP':
                spaces.append(node)
                numberOfSpaces+=1
    bpy.context.area.type = "NODE_EDITOR"
    bpy.context.area.ui_type = "ShaderNodeTree"
    bpy.context.space_data.shader_type = "OBJECT"
    for i in range(numberOfSpaces):
        bpy.ops.node.select_all(action='SELECT')
        bpy.ops.node.group_ungroup()
        bpy.context.view_layer.update()
    bpy.context.area.type = home_area
    bpy.context.area.ui_type = home_ui
    if(revertMaterials):
        obj.material_slots[num].material = mats
    return copiedMat

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


def CreatLink(mats: Material, InputValueNode: Node, OutPutValueNode: NodeSocket, mapTypeOrSocket: str,yes=False):
    if(type(mapTypeOrSocket)==str or type(mapTypeOrSocket)==int):
        inputSocket=InputValueNode.inputs[mapTypeOrSocket]
    else:
        inputSocket=mapTypeOrSocket
    if ((type(OutPutValueNode) == float) or (type(OutPutValueNode) == int)):
        if (inputSocket.is_linked):
            mats.node_tree.links.remove(
                inputSocket.links[0])
        if (type(inputSocket.default_value) == float or type(inputSocket.default_value) == int):
            inputSocket.default_value = OutPutValueNode
        else:
            inputSocket.default_value[:] = (
                OutPutValueNode,)*len(inputSocket.default_value[:])
    elif (type(OutPutValueNode) == tuple):
        if (inputSocket.is_linked):
            mats.node_tree.links.remove(
                inputSocket.links[0])
        if (type(inputSocket.default_value) == float or type(inputSocket.default_value) == int):
            inputSocket.default_value = OutPutValueNode[0]
        else:
            
            for i,value in enumerate(OutPutValueNode):
                inputSocket.default_value[i]=value
    else:
        input: NodeSocket = inputSocket
        mats.node_tree.links.new(input, OutPutValueNode)
        if(yes):
            j=OutPutValueNode.links[0].to_node
            k=OutPutValueNode.links[0].from_node


def GetInputNode(mats: Material, NodeType: str, bakeType) -> Node:
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
        if (node.type in NodeType):
            if(bakeType in  bpy.context.scene.requireAdditionalNode):

                connectToOutNode = GetNodeSocketFromRequire(
                        mats, bpy.context.scene.requireAdditionalNode[bakeType])
                # nodesToDelete[bakeMat].append(connectToOutNode.node)
                newSocket = GetNeedColorRamp(
                        mats, bakeType, connectToOutNode[0])
                if (newSocket != False):
                        connectToOutNode = newSocket[0]
                        # nodesToDelete[bakeMat].append(newSocket.node)
                else:
                    connectToOutNode = connectToOutNode[0]
                return [node, mats,connectToOutNode]
            else :

                value=GetInputValueRaw(bakeType,node)
                return [node, mats, value]    
        elif (type(node) == bpy.types.ShaderNodeGroup):
            nodeGroupsList.append(node)
    for nodeGroup in nodeGroupsList:
        result = GetInputNode(nodeGroup, NodeType, bakeType)
        if (result != False):
            return result
    return False
def GetAllNodeMat(mats: Material, NodeType,bakeType):
    nodeGroupsList: List[Node] = []
    nodeList: List[Node] = []
    nodeList.extend(mats.node_tree.nodes)
    foundNodes = []

    for node in nodeList:
        if (node.type in NodeType):
            if (node.type == "BUMP" and (node.outputs[0].links[0].to_node.type=="BUMP")):
                # here maybe
                continue
            propertyDependentInput = bpy.context.scene.propertyDependentInput
            if (bakeType in propertyDependentInput and propertyDependentInput[bakeType]["NodeType"] == node.type):
                propertyDependInfo = propertyDependentInput[bakeType]
                if (getattr(node, propertyDependInfo["Property"]) not in propertyDependInfo["PropertyAccept"]):
                    # here maybe
                    continue
            foundNodes.append(
            [node, mats])
        elif (type(node) == bpy.types.ShaderNodeGroup):
            nodeGroupsList.append(node)
    for nodeGroup in nodeGroupsList:
        result = GetAllNodeMat(nodeGroup, NodeType, bakeType)
        if (result != False):
            foundNodes.extend(result)
    multipleNodeInfo = bpy.context.scene.multipleNode
    if (foundNodes.__len__() <= 0):
        # here maybe
        return False
    else:
        return foundNodes
def GetAllInputNode(mats: Material, NodeType: str, bakeType) -> Node:
    nodeGroupsList: List[Node] = []
    nodeList: List[Node] = []
    nodeList.extend(mats.node_tree.nodes)
    foundNodes = []

    for node in nodeList:
        if (node.type in NodeType):
            if (node.type == "BUMP" and (node.outputs[0].links[0].to_node.type=="BUMP")):
                # here maybe
                continue
            
            propertyDependentInput = bpy.context.scene.propertyDependentInput
            if (bakeType in propertyDependentInput and propertyDependentInput[bakeType]["NodeType"] == node.type):
                propertyDependInfo = propertyDependentInput[bakeType]
                if (getattr(node, propertyDependInfo["Property"]) not in propertyDependInfo["PropertyAccept"]):
                    # here maybe
                    continue
            if(bakeType in  bpy.context.scene.requireAdditionalNode):
                tempList=foundNodes.copy()
                added=False
                for items in foundNodes:
                    if (items[1] == mats):
                        tempList.append(
                        [node, mats, items[2]])
                    added=True
                foundNodes = tempList
                if(not added):
                    connectToOutNode = GetNodeSocketFromRequire(
                            mats, bpy.context.scene.requireAdditionalNode[bakeType])
                    newSocket = GetNeedColorRamp(
                            mats, bakeType, connectToOutNode[0])
                    if (newSocket != False):
                            connectToOutNode = newSocket[0]
                    else:
                        connectToOutNode = connectToOutNode[0]
                    foundNodes.append(
                        [node, mats, connectToOutNode])
            else :
                value=GetInputValueRaw(bakeType,node)
                foundNodes.append(
                [node, mats, value])
        elif (type(node) == bpy.types.ShaderNodeGroup):
            nodeGroupsList.append(node)
    for nodeGroup in nodeGroupsList:
        result = GetAllInputNode(nodeGroup, NodeType, bakeType)
        if (result != False):
            foundNodes.extend(result)
    if (foundNodes.__len__() <= 0):
        # here maybe
        return False
    else:
        return foundNodes
def GetAllNode(mats: Material, NodeType,excluded=""):
    nodeList: List[Node] = []
    nodeList.extend(mats.node_tree.nodes)
    foundNodes = {}
    for node in nodeList:
        if (node.type in NodeType and node.type not in excluded and node.outputs[0].is_linked):
            foundNodes[node]=mats
    if (foundNodes.__len__() <= 0):
        # here maybe
        return False
    elif (foundNodes.__len__() > 1):
        return foundNodes






def bakeMap(uv: MeshUVLoopLayer, mesh: Object, bakeType: str, useUdims: bool, udimCount: list[int],  imageObj, selected, existingImages=None):
    ImageBakeData = {}
    selectedToActiveDate = {}
    defaultData = {}
    matsTodelete=[]
    allReadyHasImage = {}
    ogMats={}
    imageMat={}
    selectedImageMat={}
    allReadyHasSlectedImage = {}
    inputNodeType = bpy.context.scene.inputNode
    inputNodeName = bpy.context.scene.inputNodeNames
    requiredChannels =bpy.context.scene.requiredChannels
    excludedChannels = bpy.context.scene.excludedChannels.copy()
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
        unpackedMat=getUnpackedMateria(mats,matSlot,mesh,False)
        matsTodelete.append(unpackedMat)
        ogMats[mats]=[matSlot,mesh]
        
        materialOutput = GetInputNode(mats, "OUTPUT_MATERIAL", "Material OutPut Surface")
        ImageBakeData[mats] = None
        selectedToActiveDate[unpackedMat]=[]
        defaultData[mats] = None
        if (selected != None):
            exclusionMat = getUnpackedMateria(selected.data.materials[matSlot],matSlot,mesh,False)
            if(bakeType not in bpy.context.scene.DontMax):
                MaxOutOut(bakeType, exclusionMat)
            exclusionMaterialOutput = GetInputNode(
                exclusionMat, "OUTPUT_MATERIAL", "Material OutPut Surface")
        else:
            exclusionMat = mats
            exclusionMaterialOutput = materialOutput
        if(bakeType not in bpy.context.scene.DontMax):
            MaxOutOut(bakeType, unpackedMat) 
        

        if (mats != None):
            BakeInputNodesUnpacked = GetAllInputNode(
                unpackedMat, inputNodeType[bakeType], bakeType)
            if (BakeInputNodesUnpacked == False):
                continue  # here
            if (materialOutput == False):
                continue   # here
            if (len(BakeInputNodesUnpacked) > 1):
                shoulBake = True
            if (firstBakedImage == None):
                if matSlot in existingImages[bakeType]:
                    existingImage = existingImages[bakeType][matSlot]
                else:
                    existingImage = None
                firstBakedImage = addImageNode(unpackedMat, uv, mesh, useUdims, udimCount, mats, imageObj, existingImage)
                ImageBakeData[mats]=[firstBakedImage, mesh,unpackedMat]
            elif(bpy.context.scene.BakeMulitpleSlots):
                newImageNode=AddRestOfImageNode(firstBakedImage.image,
                                            unpackedMat)
                ImageBakeData[mats]=[newImageNode, mesh,unpackedMat]
            else:
                if matSlot in existingImages[bakeType]:
                    existingImage = existingImages[bakeType][matSlot]
                else:
                    existingImage = None
                newBakeImage = addImageNode(unpackedMat, uv, mesh, useUdims, udimCount, mats, imageObj, existingImage,False)
                ImageBakeData[mats]=[newBakeImage, mesh,unpackedMat]

            
            for BakeInputNodeUnpacked in BakeInputNodesUnpacked:
                bakeNodeToAddUnpacked = BakeInputNodeUnpacked[0]
                if (selected and bpy.context.scene.BakeMultiple and len(bpy.context.scene.my_items) > 1):
                    if(firstBakedImageSelected==None):
                        if (unpackedMat in allReadyHasSlectedImage):
                            selectedToActiveDate[unpackedMat].append([allReadyHasSlectedImage[unpackedMat],
                                                               unpackedMat, bakeNodeToAddUnpacked, mesh])
                        else:
                            firstBakedImageSelected = addImageNode(
                                unpackedMat, uv, mesh, useUdims, udimCount, unpackedMat, imageObj)
                            selectedToActiveDate[unpackedMat].append([firstBakedImageSelected,
                                                            unpackedMat, bakeNodeToAddUnpacked, mesh])
                            allReadyHasSlectedImage[unpackedMat] = firstBakedImageSelected
                            selectedImageMat[unpackedMat]=firstBakedImageSelected
                    elif(bpy.context.scene.BakeMulitpleSlots):
                        if (unpackedMat in allReadyHasSlectedImage):
                            selectedToActiveDate[unpackedMat].append([allReadyHasSlectedImage[unpackedMat],
                                                               unpackedMat, bakeNodeToAddUnpacked, mesh])
                        else:
                            newImageNodeSelected=AddRestOfImageNode(firstBakedImageSelected.image,
                                            unpackedMat)
                            selectedToActiveDate[unpackedMat].append([newImageNodeSelected,
                                                            unpackedMat, bakeNodeToAddUnpacked, mesh])
                            allReadyHasSlectedImage[unpackedMat] = firstBakedImageSelected
                            selectedImageMat[unpackedMat]=newImageNodeSelected
                    else:
                        if (unpackedMat in allReadyHasSlectedImage):
                            selectedToActiveDate[unpackedMat].append([allReadyHasSlectedImage[unpackedMat],
                                                               unpackedMat, bakeNodeToAddUnpacked, mesh])
                        else:
                            newBakedImageSelected = addImageNode(
                                unpackedMat, uv, mesh, useUdims, udimCount, unpackedMat, imageObj)
                            allReadyHasSlectedImage[unpackedMat] = newBakedImageSelected
                            selectedToActiveDate[unpackedMat].append([newBakedImageSelected,
                                                            unpackedMat, bakeNodeToAddUnpacked, mesh])
                            selectedImageMat[unpackedMat]=newBakedImageSelected
                if (shoulBake == False):
                    
                    currentState = PreBakeTypeCheck(
                        bakeNodeToAddUnpacked.inputs[inputNodeName[bakeType]])
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
                            defaultData[mats]=[previouseState[1],mesh,unpackedMat]
                                
        if (not shoulBake and not imageObj.enabled):
            return None
        if (selected != None):
            BakeInputNodesToUse = GetAllInputNode(
                exclusionMat, inputNodeType[bakeType], bakeType)
        else:
            BakeInputNodesToUse = BakeInputNodesUnpacked
        for BakeInputNode in BakeInputNodesToUse:
            bakeMat: Material = BakeInputNode[1]
            if (bakeType in bpy.context.scene.requiresConnection or bakeType in bpy.context.scene.requiresDefaultValue):
                
                value = BakeInputNode[2]
                nodeTocheck = BakeInputNode[0]
                baseBakeInfo = bpy.context.scene.baseNode
                if((BakeInputNode[0].type in baseBakeInfo)):
                    nodeTocheck= BakeInputNode[0].outputs[baseBakeInfo[BakeInputNode[0].type]["Output"]].links[0].to_node
                emissionNode: Node = bakeMat.node_tree.nodes.new(
                    type="ShaderNodeBsdfPrincipled")
                emissionNode.inputs["Emission Strength"].default_value = 1.0
                defaultValue = None
                connecton = None
                if (bakeType in bpy.context.scene.requiresConnection):
                    connecton = bpy.context.scene.requiresConnection[bakeType]

                if (bakeType in bpy.context.scene.requiresDefaultValue):
                    defaultValue = bpy.context.scene.requiresDefaultValue[bakeType]

                

                inputSocket: NodeSocket = nodeTocheck.outputs[0].links[0].to_socket
                excludedNode: Node = nodeTocheck.outputs[0].links[0].to_node
                if (bakeType in bpy.context.scene.ConvertInput):
                    inputSocket=excludedNode.inputs[bpy.context.scene.ConvertInput[bakeType]]
                fromSocket=inputSocket.links[0].from_socket
                if (defaultValue):
                    CreatLink(bakeMat, emissionNode, defaultValue, "Strength")
                if (connecton):
                    CreatLink(bakeMat, emissionNode, value, connecton)
                CreatLink(bakeMat, inputSocket.node, emissionNode.outputs[0], inputSocket)
                if(excludedNode.type=="MIX_SHADER"):
                    if(excludedNode.inputs[1]==inputSocket):
                        if(not excludedNode.inputs[2].is_linked):
                            CreatLink(bakeMat,excludedNode,0,0)
                    elif (not excludedNode.inputs[1].is_linked):
                        CreatLink(bakeMat,excludedNode,1,0)  

            else:
                for excludedChannel in excludedChannels:
                    baseBakeInfo = bpy.context.scene.baseNode
                    if ((excludedChannel == "Material Output") or (excludedChannel == bakeType)):
                        excludedInputNode = False
                    elif (inputNodeType[excludedChannel] == inputNodeType[bakeType]):
                        excludedInputNode = BakeInputNode
                    elif ((BakeInputNode[0].type in baseBakeInfo) and (baseBakeInfo[BakeInputNode[0].type]["Give"] == inputNodeType[excludedChannel])):
                        excludedInputNode = [
                            BakeInputNode[0].outputs[baseBakeInfo[BakeInputNode[0].type]["Output"]].links[0].to_node, BakeInputNode[1]]
                    else:
                        excludedInputNode = False
                    if (excludedChannel in bpy.context.scene.propertyDependentInput and excludedInputNode!= False):
                        dependentPropertyInfo = bpy.context.scene.propertyDependentInput[
                            excludedChannel]

                        if ((excludedInputNode[0].type != dependentPropertyInfo["NodeType"]) or (getattr(excludedInputNode[0], dependentPropertyInfo["Property"]) not in dependentPropertyInfo["PropertyAccept"])):
                            excludedInputNode = False
                    if (excludedInputNode != False):
                        inputName = inputNodeName[excludedChannel]
                        valueExcludedChannel = BreakLink(
                            excludedInputNode[0], excludedInputNode[1], inputName)
    if (selected != None):
        selected.select_set(True)
    mesh.select_set(True)

    bpy.context.view_layer.objects.active = mesh
    if (bpy.context.scene.ShadeSmooth):
        bpy.ops.object.shade_smooth()
    if (shoulBake):
        return [True, ImageBakeData, selectedToActiveDate,ogMats,matsTodelete]
    return [False, defaultData, selectedToActiveDate,ogMats,matsTodelete]

def MaxOutOut(bakeType, unpackedMat):
    toDisconnectShaders=GetAllNode(unpackedMat,bpy.context.scene.shaderNodes,bpy.context.scene.inputNode[bakeType])
    combinationShaders=GetAllNode(unpackedMat,bpy.context.scene.CombinationShader)
    if(toDisconnectShaders):
        tempDictionary={}
        while len(toDisconnectShaders)>=1:
            for shaderNodes in toDisconnectShaders:
                connection:NodeSocket=shaderNodes.outputs[0].links[0].to_socket
                fromNode:Node=connection.node
                if(fromNode.type=="MIX_SHADER"):
                    socketInt=2
                    otherSocket=1
                else:
                    socketInt=0
                    otherSocket=1
                if(fromNode.inputs[1]==connection):
                    temp=socketInt
                    socketInt=otherSocket
                    otherSocket=temp
                value=BreakLink(fromNode,unpackedMat,socketInt)
                if(not fromNode.inputs[otherSocket].is_linked and fromNode not in toDisconnectShaders and fromNode.type!="OUTPUT_MATERIAL"):
                    tempDictionary[fromNode]=unpackedMat
            toDisconnectShaders=tempDictionary.copy()
            tempDictionary.clear()
    if(combinationShaders):
        for combinationShader in combinationShaders:
            if(combinationShader.type=="MIX_SHADER"):
                combinationShader:Node=combinationShader
                if(combinationShader.inputs[1].is_linked):
                    if(not combinationShader.inputs[2].is_linked):
                        CreatLink(combinationShaders[combinationShader],combinationShader,0,0)
                elif(combinationShader.inputs[2].is_linked):
                    if(not combinationShader.inputs[1].is_linked):
                       CreatLink(combinationShaders[combinationShader],combinationShader,1,0)

def GetInputValueRaw(BakeType: str, BakeInputNode: Node):
    NodeSocketValue: NodeSocket = BakeInputNode.inputs[bpy.context.scene.inputNodeNames[
        BakeType]]
    
    if (NodeSocketValue.is_linked):
        Value = NodeSocketValue.links[0].from_socket
        return Value
    if(bpy.context.scene.inputNodeNames[BakeType]=="Surface"):
        return False
    valueToCheck = NodeSocketValue.default_value
    if ((type(valueToCheck) == float) or (type(valueToCheck) == int)):
        Value = valueToCheck
    else:
        Value = valueToCheck[:]
    return Value
def GetInputValue(BakeType: str, BakeInputNode: Node):
    NodeSocketValue: NodeSocket = BakeInputNode[0].inputs[bpy.context.scene.inputNodeNames[
        BakeType]]
    
    if (NodeSocketValue.is_linked):
        Value = NodeSocketValue.links[0].from_socket
        return Value
    valueToCheck = NodeSocketValue.default_value
    if ((type(valueToCheck) == float) or (type(valueToCheck) == int)):
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


def RestoreData(ogMats,matsTodelete,imagesToRemove):
    for images in imagesToRemove:
        bpy.data.images.remove(images)
    for matToDelete in matsTodelete:
        bpy.data.materials.remove(matToDelete)
    for mat in ogMats:
        ogMats[mat][1].material_slots[ogMats[mat][0]].material=mat
    
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
    multiplebake={}
    for obj in bpy.context.scene.my_items:
        for bakeObj in bpy.context.scene.bakingList:
            if ((bakeObj.enabled) or (bpy.context.scene.BakeMulitpleSlots and ((bakeObj.name not in bpy.context.scene.allwaysRequireBaking)) and ((bpy.context.scene.ApplyMaterial or bpy.context.scene.ApplyToCopiedAndHideOriginal)))):
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
            createdImages=[]
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
                items=BakedMap[1][mats]
                if(items==None):
                    continue
                if (mats not in createdMaterial):
                    createdMaterial[mats] = {}
                if (bakeType not in createdMaterial[mats]):
                    createdMaterial[mats][bakeType] = None
                
                if(type(items[0])==ShaderNodeTexImage):
                    createdMaterial[mats][bakeType]=[
                        items[0].image, items[1],bakeObj,"FULL"]
                    multiplebake[items[2]]=items[0]
                    createdImages.append(items[0].image)
                else:
                    createdMaterial[mats][bakeType]=[
                        items[0], items[1],bakeObj,"FULL"]
            
            if (selectedObject != None):
                for mats in BakedMap[2]:
                    if (mats not in tempData):
                        tempData[mats] = {}
                        tempData[mats][bakeType] = []
                    for items in BakedMap[2][mats]:
                        tempData[mats][bakeType].append([
                            items[0], items[1], items[2], items[3], bakeObj])
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
            if(not BakedMap[0]):
                dataToRemoveRestore.append([BakedMap[3],BakedMap[4],createdImages])
            else:
                dataToRemoveRestore.append([BakedMap[3],BakedMap[4],[]])
        if (bpy.context.scene.BakeMultiple):
            bpy.ops.object.select_all(action="DESELECT")
            bpy.context.scene.render.bake.use_selected_to_active = False
            for obj in bpy.context.scene.my_items:
                meshSecond = obj.mesh
                meshSecond.select_set(True)
                bpy.context.view_layer.objects.active = mesh
            TempConnection(tempData)
            for mat in multiplebake:
                for node in mat.node_tree.nodes:
                    node.select = False
                multiplebake[mat].select==True
                mat.node_tree.nodes.active=multiplebake[mat]
            BakeFinal(bakingSelection, bakeType,
                      multiResModifiers, needMultiRes)
        if (bakeType in needMultiRes):
            for multires in multiResModifiers:
                multires.levels = multiResModifiers[multires]
        for data in dataToRemoveRestore:
            RestoreData(data[0],data[1],data[2])

    AntiAlias(createdMaterial)
    return createdMaterial


def TempConnection(createdMaterial):
    tempMat = {}
    for mats in createdMaterial:
        tempMat[mats] = {}
        TempCreateData(createdMaterial, tempMat,mats)
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
                valueNode = createdMaterial[mats][bakeType][0]
                image = None
                if (type(valueNode) == Image):
                    image = valueNode
                    imagePath = None
                    isUdim = False
                if (image):
                    savedDate = saveImage(
                        image, mats, True, bakeType, createdMaterial[mats][bakeType][1])

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
                    loadedImage.colorspace_settings.name = createdMaterial[mats][bakeType][2].space

                    if (isUdim):
                        loadedImage.source = "TILED"
                    createdMaterial[mats][bakeType][0] = loadedImage
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
        print("Issue in restoring setting")


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
        print("issue in setting pre bake")
    return currentEngine, currentDevice, areaTypeOld, mode, extrusion, currentRaydistance, currentMargin


def saveImage(image: Image, mats: Material, isPreBaked: bool, BakeType: str, mesh):
    imageFile = GetFilePath(mats, image.source == "TILED",
                            isPreBaked, BakeType, ".<UDIM>.", mesh, image.name)
    image.filepath_raw=imageFile
    fileFormat=bpy.context.scene.FileFormatBpy[bpy.context.scene.FileFormat]
    image.file_format=fileFormat
    image.save()
    
    if (image.source == "TILED"):
        imagesPath = {}
        for tile in image.tiles:
            imagesPath[tile.number] = GetFilePath(
                mats, True, isPreBaked, BakeType, f".{tile.number}.", mesh, image.name)
        return [image, imagesPath, True]
    else:
        return [image, imageFile, False]


def GetImage(image: Image, mats: Material, isPreBaked: bool, BakeType: str, mesh):
    if (image.source == "TILED"):
        imagesPath = {}
        for tile in image.tiles:
            imagesPath[tile.number] = GetFilePath(
                mats, True, isPreBaked, BakeType, f".{tile.number}.", mesh, image.name)
        return [image, imagesPath, True]
    else:
        imageFile = GetFilePath(mats, image.source == "TILED",
                            isPreBaked, BakeType, ".<UDIM>.", mesh, image.name)
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
        imageFile = f"{pathToUseDir}\\" + \
            f"{fileName}.{tileInfo}.{extension}"
    else:
        imageFile = f"{pathToUseDir}\\" + \
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

def createMat(bakeDate,mats,newCreatedMats):
    imageMatData={}
    newCreatedMats[mats]={}
    for bakeType in bakeDate[mats]:
        if(bakeType not in newCreatedMats[mats]):
            newCreatedMats[mats][bakeType]=[]
        inputs=GetAllNodeMat(mats,bpy.context.scene.inputNode[bakeType],bakeType)
        for input in inputs:
            bakeMat:Material=input[1]
            bakeNode:Node=input[0]
            if(bakeMat not in imageMatData):
                imageMatData[bakeMat]={}
            if(bakeDate[mats][bakeType][0] not in imageMatData[bakeMat]):
                imageMatData[bakeMat][bakeDate[mats][bakeType][0]]={}
                if(type(bakeDate[mats][bakeType][0])==Image):
                    ImageNode:Node=AddRestOfImageNode(bakeDate[mats][bakeType][0],bakeMat)
                    imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["ImageNode"]=ImageNode
                    if(bakeDate[mats][bakeType][3]!="FULL"):
                        seperateNode:Node=bakeMat.node_tree.nodes.new(type="ShaderNodeSeparateColor")
                        CreatLink(bakeMat,seperateNode,ImageNode.outputs["Color"],"Color")
                        imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["SeperateNode"]=seperateNode
                else:
                    j=imageMatData[bakeMat][bakeDate[mats][bakeType][0]]
                    imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["ImageNode"]=bakeDate[mats][bakeType][0]
            if(type(imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["ImageNode"])==ShaderNodeTexImage):
                if(bakeDate[mats][bakeType][3]!="FULL"):
                    if(bakeDate[mats][bakeType][3]!="Alpha"):
                        value=imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["SeperateNode"].outputs[bakeDate[mats][bakeType][3]]
                    else:
                        value=imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["ImageNode"].outputs["Alpha"]
                else:
                    value=imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["ImageNode"].outputs["Color"]
            else:
                value=imageMatData[bakeMat][bakeDate[mats][bakeType][0]]["ImageNode"]
            newCreatedMats[mats][bakeType].append([value,bakeMat,bakeNode,bakeDate[mats][bakeType][1],bakeDate[mats][bakeType][2]])

def Start():
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
        Fliping(bakeDate, bakeDate[mats], mats)
        PackTexture(bakeDate, mats)
        createJson(bakeDate, mats, createdJson)
        createMat(bakeDate,mats,newCreatedMats)
    for mats in bakeDate:
        for finalBakeType in bakeDate[mats]:
            try:
                outputNode= bakeDate[mats][finalBakeType][0]
                if (type(outputNode)==Image):
                    saveImage(outputNode, mats,
                            False, finalBakeType, bakeDate[mats][finalBakeType][1])
            except Exception as e:
                print(f"print issue saving image {e}")
    if (bpy.context.scene.ApplyMaterial or bpy.context.scene.ApplyToCopiedAndHideOriginal):
        ApplyMaterial(newCreatedMats)
    else:
        for mats in newCreatedMats:
            bpy.data.materials.remove(mats)
    jsonExportPath=f"{bpy.context.scene.basePath}MappingFile\\"
    os.makedirs(jsonExportPath, exist_ok=True)
    with open(f"{jsonExportPath}mapping.json", "w") as jsonFile:
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
    if (finalBakeType in requireAdditonSteps):
        tempNode = oldValue.node
        if (tempNode.bl_idname != requireAdditonSteps[finalBakeType]["Node"]):
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
    print(f"{items} sdscsdcsdcsd")
    flippingInfo = {"Red":items[4].Red,"Green":items[4].Green,"Blue":items[4].Blue}
    if (items[4].Invert):
        invertNode = matsTree.node_tree.nodes.new(type="ShaderNodeInvert")
        CreatLink(matsTree, invertNode, items[0],
                    "Color")
        items[0] = invertNode.outputs["Color"]
    elif(items[4].Red or items[4].Green or items[4].Blue):
        seperateColorNode = matsTree.node_tree.nodes.new(
            type="ShaderNodeSeparateColor")
        combineColorNode = matsTree.node_tree.nodes.new(
            type="ShaderNodeCombineColor")

        CreatLink(matsTree, seperateColorNode, items[0],
                    "Color")
        for channel in flippingInfo:
            if (channel != "Alpha"):
                if (flippingInfo[channel]):
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
    for bakeType in bakeTypes:
        obj=bakeDate[mats][bakeType][2]
        if(obj.Red or obj.Green or obj.Blue  or obj.Invert):
            Invert(bakeDate, mats, bakeType)


def Invert(bakeDate, mats, bakeType):
    value = bakeDate[mats][bakeType][0]
    obj=bakeDate[mats][bakeType][2]
    if ((type(value) == int) or (type(value) == float)):
        bakeDate[mats][bakeType][0] = 1-value
    else:
        imagePath = None
        currentImage: Image = bakeDate[mats][bakeType][0]
        savedInfo = saveImage(
            currentImage, mats, True, bakeType, bakeDate[mats][bakeType][1])
        bpy.data.images.remove(currentImage)
        name = GetImageName(
            mats.name, bakeDate[mats][bakeType][1].name, bakeDate[mats][bakeType][2])
        if (savedInfo[2]):
            for tiles in savedInfo[1]:
                imageToInvert = imageio.v3.imread(
                    savedInfo[1][tiles])
                ndim = imageToInvert.ndim
                valueToExclue = 1 if Path(
                    savedInfo[1][tiles]).suffix in bpy.context.scene.OneInvert else 255

                if (ndim == 2):
                    imageToInvert = valueToExclue-imageToInvert

                else:
                    for i in range(ndim):
                        if ((obj.Red and i==0) or (obj.Green and i==1) or (obj.Blue and i==2) or obj.Invert):
                            imageToInvert[:, :, i] = valueToExclue - \
                                imageToInvert[:, :, i]
                savedLocation = GetFilePath(
                    mats, True, True, bakeType, tiles, bakeDate[mats][bakeType][1], name)
                imageio.v3.imwrite(savedLocation, imageToInvert)
                imagePath = savedLocation
        else:
            imageToInvert = imageio.v3.imread(
                savedInfo[1])
            ndim = imageToInvert.ndim
            valueToExclue = 1 if Path(
                savedInfo[1]).suffix in bpy.context.scene.OneInvert else 255

            if (ndim == 2):
                imageToInvert = valueToExclue-imageToInvert

            else:
                for i in range(ndim):
                    if ((obj.Red and i==0) or (obj.Green and i==1) or (obj.Blue and i==2) or obj.Invert):
                        imageToInvert[:, :, i] = valueToExclue - \
                            imageToInvert[:, :, i]
            savedLocation = GetFilePath(
                mats, False, True, bakeType, None, bakeDate[mats][bakeType][1], name)
            imageio.v3.imwrite(savedLocation, imageToInvert)
            imagePath = savedLocation

        image: Image = bpy.data.images.load(
            imagePath, check_existing=True)
        image.name = Path(imagePath).stem
        if (savedInfo[2]):
            image.source = "TILED"
        image.colorspace_settings.name = bakeDate[mats][bakeType][2].space
        bakeDate[mats][bakeType][0] = image


def GetBlendings(newCreatedMats, mats):
    blendingsDate = bpy.context.scene.Blending

    for blendingBakesList in blendingsDate:
        if (blendingBakesList in newCreatedMats[mats]):
            connectionObj = blendingsDate[blendingBakesList]
            properties = connectionObj["Properties"]
            inputs = connectionObj["Inputs"]
            alreadyAdded={}
            deleteNode={}
            for checkingBake in newCreatedMats[mats][blendingBakesList]:
                ColorBake=bpy.context.scene.ColorMapNodeInverse[checkingBake[2].type]
                if(ColorBake not in newCreatedMats[mats]):
                    nodes=GetAllInputNode(mats,checkingBake[2].type,ColorBake)
                    for node in nodes:
                        if(ColorBake not in newCreatedMats[mats]):
                            newCreatedMats[mats][ColorBake]=[]
                        dataToAppend=[node[2],node[1],node[0],checkingBake[3],checkingBake[4]]
                        newCreatedMats[mats][ColorBake].append(dataToAppend)
                    continue
                else:
                    continue
            
            for blendingBake in newCreatedMats[mats][blendingBakesList]:
                for blendTexture in newCreatedMats[mats][bpy.context.scene.ColorMapNodeInverse[blendingBake[2].type]]:
                    if ((blendTexture[1] == blendingBake[1]) and (blendTexture[2] == blendingBake[2])):
                        j=blendTexture[0]
                        if((blendTexture[1] in alreadyAdded) and (blendTexture[2] == alreadyAdded[blendTexture[1]][2])):
                            blendTexture[0]=alreadyAdded[blendTexture[1]][0]
                        else:
                            createdNode = GetMixShader(connectionObj, properties, inputs, blendingBake)
                            CreatLink(blendingBake[1],createdNode,blendTexture[0],"A")
                            CreatLink(blendingBake[1],createdNode,blendingBake[0],"B")
                            mats:Material= blendingBake[1]
                            blendTexture[0]=createdNode.outputs[2]
                            alreadyAdded[blendTexture[1]]=blendTexture

            del newCreatedMats[mats][blendingBakesList]

def GetMixShader(connectionObj, properties, inputs, primaryBake):
    createdNode: Node = primaryBake[1].node_tree.nodes.new(type=connectionObj["Node"])
    for property in properties:
        setattr(createdNode, property,
                            properties[property])
    for input in inputs:
        CreatLink(primaryBake[1], createdNode,
                                inputs[input], input)
                    
    return createdNode

def TempCreateData(newCreatedMats, bakeDate, mats):
    for bakedTextureType in bakeDate[mats]:
        for items in bakeDate[mats][bakedTextureType]:
            if (bakedTextureType not in newCreatedMats[mats]):
                newCreatedMats[mats][bakedTextureType] = []
            if (type(items[0]) == ShaderNodeTexImage):
                outPutToAdd = items[0].outputs["Color"]

            else:
                outPutToAdd = items[0]
            newCreatedMats[mats][bakedTextureType].append([
                outPutToAdd, items[1], items[2], items[3],items[4]])
def createJson(bakeDate, mats, createdJson):
    createdJson[mats.name]={}
    for bakedTextureType in bakeDate[mats]:
        valueData = bakeDate[mats][bakedTextureType][0]
        createdJson[mats.name][bakedTextureType] = {}
        if (type(valueData) ==Image ):
            value = GetImage(valueData, mats, False,
                                bakedTextureType, bakeDate[mats][bakedTextureType][1])
            if (not value[2]):
                valueToAdd = value[1]
                createdJson[mats.name][bakedTextureType]["value"] = valueToAdd
                createdJson[mats.name][bakedTextureType]["Channel"] = bakeDate[mats][bakedTextureType][3]
                createdJson[mats.name][bakedTextureType]["Tiled"] = False
                createdJson[mats.name][bakedTextureType]["Mesh"] = bakeDate[mats][bakedTextureType][1].name
                createdJson[mats.name][bakedTextureType]["Shader"]=bakeDate[mats][bakedTextureType][2].shaderNode
            else:
                createdJson[mats.name][bakedTextureType]["Tiled"] = True
                createdJson[mats.name][bakedTextureType]["Channel"] = bakeDate[mats][bakedTextureType][3]
                createdJson[mats.name][bakedTextureType]["value"] = {}
                createdJson[mats.name][bakedTextureType]["Mesh"] = bakeDate[mats][bakedTextureType][1].name
                createdJson[mats.name][bakedTextureType]["Shader"]=bakeDate[mats][bakedTextureType][2].shaderNode
                for tile in value[1]:
                    valueToAdd = value[1][tile]
                    createdJson[mats.name][bakedTextureType]["value"][tile] = valueToAdd
        else:
            valueToAdd = valueData
            createdJson[mats.name][bakedTextureType]["value"] = valueToAdd
            createdJson[mats.name][bakedTextureType]["Channel"] = bakeDate[mats][bakedTextureType][3]
            createdJson[mats.name][bakedTextureType]["Tiled"] = False
            createdJson[mats.name][bakedTextureType]["Mesh"] = bakeDate[mats][bakedTextureType][1].name
            createdJson[mats.name][bakedTextureType]["Shader"]=bakeDate[mats][bakedTextureType][2].shaderNode


def PackTexture(bakeDate, mats):

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
            mesh = bakeDate[mats][redBakeTexture][1]
        elif (greenChannel[2]):
            mesh = bakeDate[mats][greenBakeTexture][1]
        elif (blueChannel[2]):
            mesh = bakeDate[mats][alphaBakeTexture][1]
        elif (alphaChannel[2]):
            mesh = bakeDate[mats][blueBakeTexture][1]
        else:
            continue
        tiles = list(
            set(blueChannel[3]+alphaChannel[3]+greenChannel[3]+redChannel[3]))
        if (needPacking):
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
            image = bpy.data.images.load(savedFolder, check_existing=True)
            if (useUdim):
                image.source = "TILED"
            image.colorspace_settings.name = packedTexture.space
            image.name = Path(savedFolder).stem
            for channel in ChannelList:
                if (ChannelList[channel][0]):
                    imageToRemove=bakeDate[mats][channel][0]
                    bakeDate[mats][channel][0]=image
                    bakeDate[mats][channel][3]=ChannelList[channel][1]
                    if(type(imageToRemove)==Image):
                        bpy.data.images.remove(imageToRemove)


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
            l=createdMaterial[mats][bakeTexture]
            channelData = createdMaterial[mats][bakeTexture][0]
            needPacking = True

            if (type(channelData) == ShaderNodeTexImage):
                channelData = saveImage(
                    channelData.image, mats, True, bakeTexture, createdMaterial[mats][bakeTexture][1])
                useUdim = channelData[2]
                if (useUdim):
                    tiles = list(channelData[1])
        else:
            channelData = 0
            needPacking = False
    return [channelData, useUdim, needPacking, tiles]



class MAIN_PT_PANEL(bpy.types.Panel):
    bl_label = "Main"
    bl_idname = "SCENE_PT_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Texture Manager"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.operator("Main.now",text="Start")
        
class Main_OT_Now(bpy.types.Operator):
    bl_idname = "main.now"
    bl_label = "main Operator"
    bl_description = "Click Start"
    def execute(self, context):
        if(bpy.context.scene.basePath==""):
            if(bpy.path.abspath("//")!=""):
                bpy.context.scene.basePath=bpy.path.abspath("//")
            else:
                bpy.ops.warning.path()
        else:
            Start()
        return {'FINISHED'}
class Warning_OT_Path(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "warning.path"
    bl_label = "Warning Path Operator"


    def execute(self, context):
        self.report({'ERROR'}, 'Please select texture path')
        return {'FINISHED'}

listOfClass = [Warning_OT_Path,Main_OT_Now, MAIN_PT_PANEL]
class_register, class_unregister = bpy.utils.register_classes_factory(
    listOfClass)


def registerStartTab():
    class_register()

def UnregisterStartTab():
    class_unregister()

