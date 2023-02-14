import maya.cmds as cmds
import os
from copy import deepcopy
def import_gpu(file_Directory="",gpu_name=""):    
    if  "_C_0" in gpu_name:
        strip_name = gpu_name.rstrip("_C_0")
        file_name = "{0}.abc".format(strip_name)
        dir_path = "D:\HeroRiseMan_convert\HeroRiseMan\SET"+"\{0}".format(file_Directory) + "\GPU"
        full_path = os.path.join(dir_path, file_name)
    
        if os.path.exists(full_path):
            print('File {0} Exists : True'.format(full_path))
            createNode = cmds.createNode("gpuCache", name=strip_name) 
            cacheParent = cmds.listRelatives(createNode, p=1, pa=1)    
            cacheParent = cmds.rename(cacheParent, createNode)
            cmds.setAttr("|"+createNode+"|"+createNode+'.cacheFileName',full_path,type='string' )
            return createNode
        if not os.path.exists(full_path):
            print("not exists File : {0}".format(full_path))
    if gpu_name:
        
        file_name = "{0}.abc".format(gpu_name)
        dir_path = "D:\HeroRiseMan_convert\HeroRiseMan\SET"+"\{0}".format(file_Directory) + "\GPU"
        full_path = os.path.join(dir_path, file_name)
        selShapes = cmds.ls(dag=1, leaf=1, shapes=1, long=True, v=1)
        gpuCacheShapes = cmds.ls(selShapes, shortNames=True, type='gpuCache')
        trans_name = cmds.listRelatives(gpuCacheShapes, p=1, pa=1)
        count = []
        if os.path.exists(full_path):
           
            if trans_name==None:
                createNode_shape = cmds.createNode("gpuCache", name="{0}_shape".format(gpu_name)) 
                cacheParent = cmds.listRelatives(createNode_shape, p=1, pa=1)    
                cacheParent = cmds.rename(cacheParent, "{0}_0".format(gpu_name))
                cmds.setAttr("|"+cacheParent+"|"+createNode_shape+'.cacheFileName',full_path,type='string' )

        
            elif len(trans_name)>=1:
                createNode_shape = cmds.createNode("gpuCache", name="{0}_{1}_shape".format(gpu_name,len(trans_name))) 
                cacheParent = cmds.listRelatives(createNode_shape, p=1, pa=1)    
                cacheParent = cmds.rename(cacheParent, "{0}_{1}".format(gpu_name,len(trans_name)))
                cmds.setAttr("|"+cacheParent+"|"+createNode_shape+'.cacheFileName',full_path,type='string' )
            
        return createNode_shape
    else:
        print("not match name")
    return None         

def unreal_refine_file (file_name="" ):
        
    del_list = []
    new_list = []
    BG_folder =  file_name.split("_")[1]
    file_path = "D:\HeroRiseMan_convert\HeroRiseMan\{0}\{1}.t3d".format(BG_folder,file_name)
    
    origin_name = file_path.split("\\")[-1].split(".")[0]
    with open(file_path) as f:
        lines = f.readlines()
    
    for idx, line in enumerate(lines,0):
        if "Begin Object Class=" in line :
            del lines[idx+1]
        if "Begin Object Class=" in line  or  "InstanceComponents" in line or "StaticMeshImportVersion" in line \
            or "bUseDefaultCollision" in line or "bGenerateOverlapEvents" in line or "Mobility=Static" in line or "StaticMeshDerivedDataKey" in line or "BodyInstance" in line \
            or "CustomProperties" in line \
            or  "RootComponent" in line or "StaticMeshComponent=" in line :
            del_list.append(line)


    for idnum, i in enumerate(lines,0):
        if i not in del_list:
            new_list.append(i)


    write_path = "D:\\HeroRiseMan_convert\\HeroRiseMan\\"
    folderName = new_list[0].split("/")[-2]
    refine_file_name = origin_name
    extension = "txt"
    new_file = "{0}{1}\\{2}.{3}".format(write_path,folderName,refine_file_name,extension)
    f= open(new_file,'w')
    for ActorBundle in new_list:
        for i in  ActorBundle:
            f.write(i)
    f.close()
    return refine_file_name

def actor_divide (file_name = ""):

    BG_folder =  file_name.split("_")[1]
    my_file_path = "D:\HeroRiseMan_convert\HeroRiseMan\{0}\{1}.txt".format(BG_folder,file_name)
    
    ActorLineStart = []        
    ActorLineEnd = []
    DivideActor = []
    with open(my_file_path) as my:
        my_lines = my.readlines()

    for LineNum ,LineSplit in enumerate(my_lines):
        if LineSplit.find('Begin Actor Class=') >0:
            cc = LineNum 
            dd = my_lines[cc]
            ActorLineStart.append(cc)
            
    for LineNum ,LineSplit in enumerate(my_lines):
        if LineSplit.find('End Actor') >0:
            cc = LineNum 
            dd = my_lines[cc]
            ActorLineEnd.append(cc)
    SplitPoint = list(zip(ActorLineStart,ActorLineEnd))

    for PartActor in SplitPoint:
        DivideActor.append(my_lines[PartActor[0]:PartActor[1]])
    
    return DivideActor 

def TO_GPU (name = "", folder = ""):
    my_file_path = unreal_refine_file(name)
    DividActor = actor_divide(my_file_path)
    ResultDict = {}
    EtcResultDict = {}
    DictForm = {'translate':[0.000000,0.000000,0.000000], 'Rotation':[0.000000,0.000000,0.000000], 'Scale':[1.000000,1.000000,1.000000]}    
    for Actors in DividActor:
        for nn, aaa in enumerate(Actors):
            if 'Begin Object Name="StaticMeshComponent0"' in aaa:
                
                StartComponent = nn
                
            if "End Object" in aaa:
                bb = Actors[nn-1]
                if  "Begin Object Class=" not in bb and "CreationMethod=Instance" not in bb:
                    
                    EndComponent = nn
                    EtcStartComponent = EndComponent +1
                    EtcEndComponent = len(Actors)-1
        
            if "ActorLabel=" in aaa:
                tempLabelNmae = aaa.split("=")[-1]
                LabelNmae = tempLabelNmae.split('"')[1]
                
        DivideActor=Actors[StartComponent:EndComponent]
        EtcDivideActorA = Actors[:StartComponent]
        EtcDivideActorB = Actors[EndComponent:]
        EtcDivideActor = EtcDivideActorA+EtcDivideActorB
        


        
        


        for idx, line in enumerate(DivideActor,0):
            if line.find("StaticMesh=")>0:
                CurrentName = line.strip()
                Split = CurrentName.split("'") 
                Refine1 = CurrentName.split("'")[-2].replace("'", '').replace('"', '').split('/')[-1]
                Refine2 = Refine1.split('.')[-1]+"-"+LabelNmae
                CurrentName = Refine2
                
                if ResultDict.get(CurrentName):
                    CurrentName=CurrentName+"_"+ LabelNmae
                    
                ResultDict[CurrentName] = deepcopy(DictForm)
                
            if line.find("RelativeLocation=")>0:
                Renewal_trans = line.replace("=", " ").replace("RelativeLocation", " ").replace("X", " ").replace("Y", " ").replace("Z", " ").replace("(","").replace(")","").replace(" ","")
                temp_Renewal_trans = Renewal_trans.split(",")
                Renewal_trans =temp_Renewal_trans
                List_translate = [float(Renewal_trans[0]),float(Renewal_trans[1]),float(Renewal_trans[2])]
                if CurrentName != '':
                    ResultDict[CurrentName]['translate'] = List_translate

            if line.find("RelativeRotation=")>0:
                Renewal_Rota = line.replace("=", " ").replace("RelativeRotation", " ").replace("Pitch", " ").replace("Yaw", " ").replace("Roll", " ").replace("(","").replace(")","").replace(" ","")
                temp_Renewal_Rota = Renewal_Rota.split(",")
                Renewal_Rota =temp_Renewal_Rota
                List_Rota = [float(Renewal_Rota[0]),float(Renewal_Rota[1])*-1,float(Renewal_Rota[2])]
                if CurrentName != '':
                    ResultDict[CurrentName]['Rotation'] = List_Rota

            if line.find("RelativeScale3D=")>0:
                Renewal_scale = line.replace("=", " ").replace("RelativeScale3D", " ").replace("X", " ").replace("Y", " ").replace("Z", " ").replace("(","").replace(")","").replace(" ","")
                temp_Renewal_scale = Renewal_scale.split(",")
                Renewal_scale =temp_Renewal_scale
                List_scale = [float(Renewal_scale[0]),float(Renewal_scale[2]),float(Renewal_scale[1])]
                if CurrentName != '':
                    ResultDict[CurrentName]['Scale'] = List_scale



        for idx, line in enumerate(EtcDivideActor,0):
            
            if line.find("StaticMesh=")>0:
                CurrentName = line.strip()
                Split = CurrentName.split("'") 
                Refine1 = CurrentName.split("'")[-2].replace("'", '').replace('"', '').split('/')[-1]
                Refine2 = Refine1.split('.')[-1]+"-"+LabelNmae
                CurrentName = Refine2
                
                if EtcResultDict.get(CurrentName):
                    CurrentName=CurrentName+"-"+ str(idx)
                    
                EtcResultDict[CurrentName] = deepcopy(DictForm)
                
            if line.find("RelativeLocation=")>0:
                Renewal_trans = line.replace("=", " ").replace("RelativeLocation", " ").replace("X", " ").replace("Y", " ").replace("Z", " ").replace("(","").replace(")","").replace(" ","")
                temp_Renewal_trans = Renewal_trans.split(",")
                Renewal_trans =temp_Renewal_trans
                List_translate = [float(Renewal_trans[0]),float(Renewal_trans[1]),float(Renewal_trans[2])]
                if CurrentName != '':
                    EtcResultDict[CurrentName]['translate'] = List_translate

            if line.find("RelativeRotation=")>0:
                Renewal_Rota = line.replace("=", " ").replace("RelativeRotation", " ").replace("Pitch", " ").replace("Yaw", " ").replace("Roll", " ").replace("(","").replace(")","").replace(" ","")
                temp_Renewal_Rota = Renewal_Rota.split(",")
                Renewal_Rota =temp_Renewal_Rota
                List_Rota = [float(Renewal_Rota[0]),float(Renewal_Rota[1])*-1,float(Renewal_Rota[2])]
                if CurrentName != '':
                    EtcResultDict[CurrentName]['Rotation'] = List_Rota

            if line.find("RelativeScale3D=")>0:
                Renewal_scale = line.replace("=", " ").replace("RelativeScale3D", " ").replace("X", " ").replace("Y", " ").replace("Z", " ").replace("(","").replace(")","").replace(" ","")
                temp_Renewal_scale = Renewal_scale.split(",")
                Renewal_scale =temp_Renewal_scale
                List_scale = [float(Renewal_scale[0]),float(Renewal_scale[2]),float(Renewal_scale[1])]
                if CurrentName != '':
                    EtcResultDict[CurrentName]['Scale'] = List_scale

            

    for key, value in ResultDict.items():
        import_name = key.split("-")[0]
        actor_name = key.split("-")[1]
        # create_grp= cmds.group(n="{0}_grp".format(import_name),em=1)
        GPU_asset=import_gpu(folder,import_name)
        # cmds.select(GPU_asset, r=1)
        selobj = cmds.ls( sl=1 ,s=1 )
        origin_name = cmds.listRelatives(selobj, p=1)
        
        transX = ResultDict[key].get("translate")[0]
        transY = ResultDict[key].get("translate")[2]
        transZ = ResultDict[key].get("translate")[1]
        roX = ResultDict[key].get("Rotation")[0]
        roY = ResultDict[key].get("Rotation")[1]
        roZ = ResultDict[key].get("Rotation")[2]
        scX = ResultDict[key].get("Scale")[0]
        scY = ResultDict[key].get("Scale")[1]
        scZ = ResultDict[key].get("Scale")[2]
        
        
        cmds.setAttr("{0}.translate".format(origin_name[0]),transX,transY,transZ)
        cmds.setAttr("{0}.rotate".format(origin_name[0]),ResultDict[key].get("Rotation")[2],ResultDict[key].get("Rotation")[1],ResultDict[key].get("Rotation")[0])
        cmds.setAttr("{0}.scale".format(origin_name[0]),ResultDict[key].get("Scale")[0],ResultDict[key].get("Scale")[1],ResultDict[key].get("Scale")[2])
        cmds.setAttr(origin_name[0]+".rotateOrder", 3)

        for key, value in EtcResultDict.items():
            
            Etc_import = key.split("-")[0]
            Etc_actor = key.split("-")[1]
            Etc_num = key.split("-")[-1]
            
            if Etc_actor == actor_name and Etc_import == import_name :
                
                duplicate_asset = cmds.instance(selobj, name = '{0}#'.format(selobj))[0]
                cmds.parent(duplicate_asset,selobj,absolute=0)
                cmds.select(duplicate_asset, r=1)
                aa = cmds.ls(sl=1)
                
                cmds.setAttr ("{0}.translate".format(aa[0]),EtcResultDict[key].get("translate")[0], EtcResultDict[key].get("translate")[2], EtcResultDict[key].get("translate")[1])
                cmds.parent(aa,world=1)
                cmds.setAttr ("{0}.rotate".format(aa[0]),(EtcResultDict[key].get("Rotation")[2]+roZ), ((EtcResultDict[key].get("Rotation")[1])+roY),(EtcResultDict[key].get("Rotation")[0]+roX) )
                # if  cmds.getAttr ("{0}.rotateY".format(aa[0]))<0:
                #     cmds.setAttr ("{0}.rotate".format(aa[0]),(EtcResultDict[key].get("Rotation")[2]+roZ), ((EtcResultDict[key].get("Rotation")[1])+roY),(-1*(EtcResultDict[key].get("Rotation")[0]+roX)) )
                
                cmds.setAttr ("{0}.scale".format(aa[0]),EtcResultDict[key].get("Scale")[0]*scX, EtcResultDict[key].get("Scale")[1]*scY, EtcResultDict[key].get("Scale")[2]*scZ)
                cmds.setAttr(aa[0]+".rotateOrder", 3)
                cmds.parent(duplicate_asset,selobj,absolute=0)

            elif Etc_actor == actor_name and Etc_import != import_name :
                # print("{0}::{1}".format(Etc_actor, value))
                Etc_GPU_asset=import_gpu(folder,Etc_import)
                # cmds.select(Etc_GPU_asset, r=1)
                test_name = cmds.listRelatives(Etc_GPU_asset, p=1)
                

                # print("aa:{0}".format(test_name))
                cmds.parent(test_name,selobj, absolute=0)
                
                bb = cmds.ls(sl=1)
                cmds.setAttr ("{0}.translate".format(test_name[0]),EtcResultDict[key].get("translate")[0], EtcResultDict[key].get("translate")[2], EtcResultDict[key].get("translate")[1])
                cmds.parent(Etc_GPU_asset,world=1)
                cmds.setAttr ("{0}.rotate".format(test_name[0]),EtcResultDict[key].get("Rotation")[0]+roX, EtcResultDict[key].get("Rotation")[1]+roY, EtcResultDict[key].get("Rotation")[2]+roZ)
                cmds.setAttr ("{0}.scale".format(test_name[0]),EtcResultDict[key].get("Scale")[0]*scX, EtcResultDict[key].get("Scale")[1]*scY, EtcResultDict[key].get("Scale")[2]*scZ)
                cmds.setAttr(test_name[0]+".rotateOrder", 3)
                cmds.parent(test_name,selobj, absolute=0)




    
    return ResultDict

            
print(TO_GPU("BG_VolcanoMountain_moutain","Prop")            )